import math
import random
import pygame
from Particle import Particle
import numpy
import pyopencl as cl
import pyopencl.array as cl_array

class PhysicsEngine():
    #Handles the particle interactions
    def __init__(self):
        self.particles = []
        self.max_Radius = 0.25
        self.friction_Factor = math.pow(0.5, 0.01 / 0.040)
        self.force_Factor = 10
        self.matrix = [[],[],[]]
        self.beta = 0.15
        self.randomMatrix()
        self.paused = False

        self.simarea = pygame.Surface((800,800))

        # --- OpenCL Setup ---
        self.ctx = None
        try:
            self.platform = cl.get_platforms()[0]
            self.device = self.platform.get_devices(device_type=cl.device_type.GPU)[0]
            self.ctx = cl.Context([self.device])
            self.queue = cl.CommandQueue(self.ctx)
            print("OpenCL initialized on GPU:", self.device.name)
        except (cl.Error, IndexError) as e:
            print(f"Could not initialize OpenCL on GPU: {e}. Falling back to CPU.")
            try:
                self.platform = cl.get_platforms()[0]
                self.device = self.platform.get_devices(device_type=cl.device_type.CPU)[0]
                self.ctx = cl.Context([self.device])
                self.queue = cl.CommandQueue(self.ctx)
                print("OpenCL initialized on CPU:", self.device.name)
            except Exception as e_cpu:
                print(f"Fatal: Could not initialize OpenCL on CPU either: {e_cpu}")
                self.ctx = None # Flag that OpenCL is not available
                return

        kernel_code = """
        __kernel void interactions(
            __global const float2* positions,
            __global const int* color_ids,
            __global const float* matrix,
            __global float2* out_velocities,
            __global float2* out_positions,
            const float max_radius,
            const float beta,
            const float force_factor,
            const float friction_factor,
            const int num_particles)
        {
            int i = get_global_id(0);
            if (i >= num_particles) return;

            float2 pos_i = positions[i];
            // The original velocities are not needed on the GPU, we calculate the new ones from scratch
            float2 vel_i = (float2)(0.0f, 0.0f); 
            int color_id_i = color_ids[i];

            float total_force_x = 0.0f;
            float total_force_y = 0.0f;

            for (int j = 0; j < num_particles; ++j) {
                if (i == j) continue;

                float2 pos_j = positions[j];
                int color_id_j = color_ids[j];

                float dx = pos_j.x - pos_i.x;
                float dy = pos_j.y - pos_i.y;

                // Periodic boundary conditions
                if (dx > 0.5f) dx -= 1.0f;
                if (dx < -0.5f) dx += 1.0f;
                if (dy > 0.5f) dy -= 1.0f;
                if (dy < -0.5f) dy += 1.0f;

                float radius = hypot(dx, dy);

                if (radius > 0 && radius < max_radius) {
                    float r_norm = radius / max_radius;
                    float a = matrix[color_id_i * 3 * color_id_j];
                    float f = 0.0f;

                    if (r_norm < beta) {
                        f = (r_norm / beta) - 1.0f;
                    } else if (r_norm < 1.0f) {
                        f = a * (1.0f - fabs(-(2.0f * r_norm + 2.0f) / (1.0f - beta) - 1.0f));
                    }
                    
                    // Normalize dx and dy to get direction vector
                    float inv_radius = 1.0f / radius;
                    total_force_x += dx * inv_radius * f;
                    total_force_y += dy * inv_radius * f;
                }
            }

            total_force_x *= max_radius * force_factor;
            total_force_y *= max_radius * force_factor;

            // Update velocity
            vel_i.x = out_velocities[i].x * friction_factor + total_force_x * 0.01f;
            vel_i.y = out_velocities[i].y * friction_factor + total_force_y * 0.01f;

            // Update position
            pos_i.x += vel_i.x * 0.01f;
            pos_i.y += vel_i.y * 0.01f;

            // Wrap position
            pos_i.x = fmod(pos_i.x + 1.0f, 1.0f);
            pos_i.y = fmod(pos_i.y + 1.0f, 1.0f);

            out_velocities[i] = vel_i;
            out_positions[i] = pos_i;
        }
        """
        self.prg = cl.Program(self.ctx, kernel_code).build()


    def addParticle(self):
        self.particles.append(Particle())
        
    def removeParticle(self):
        if len(self.particles) > 0:
            self.particles.pop()

    def changeParticleCount(self, amount):
        if amount > len(self.particles)+1:
            for i in range(amount-len(self.particles)):
                self.addParticle()
        elif amount < len(self.particles)+1:
            for i in range(len(self.particles)-amount):
                self.removeParticle()
    
    def randomMatrix(self): 
        rows = [] 
        for i in range(0,3): 
            row = [] 
            for j in range(0,3): 
                row.append(round((random.uniform(0, 1) * 2 - 1),3)) 
            rows.append(row) 
        self.matrix = rows
    

    def force(self, r, a):
        #Force Function (Numpy version, kept for potential fallback)
        force = numpy.zeros_like(r)
        
        # Mask for r < self.beta
        mask1 = r < self.beta
        force[mask1] = (r[mask1] / self.beta) - 1
        
        # Mask for self.beta < r < 1
        mask2 = (self.beta < r) & (r < 1)
        force[mask2] = a[mask2] * (1 - abs(-(2 * r[mask2] - 2) / (1 - self.beta) - 1))
        
        return force
        
    
    
    def interactions(self): 
        if self.paused or not self.ctx:
            # Fallback to numpy or do nothing if OpenCL is not available
            # For simplicity, we'll just return. You could implement the numpy version here as a fallback.
            return
        
        num_particles = len(self.particles)
        if num_particles == 0:
            return

        # --- Prepare data for OpenCL ---
        # Using float32 is crucial for OpenCL compatibility
        positions = numpy.array([[p.pos_x, p.pos_y] for p in self.particles], dtype=numpy.float32)
        velocities = numpy.array([[p.vel_x, p.vel_y] for p in self.particles], dtype=numpy.float32)
        color_ids = numpy.array([p.colour_ID for p in self.particles], dtype=numpy.int32)
        matrix_flat = numpy.array(self.matrix, dtype=numpy.float32).flatten()

        # --- Create OpenCL buffers ---
        mf = cl.mem_flags
        pos_buf = cl_array.to_device(self.queue, positions)
        vel_buf = cl_array.to_device(self.queue, velocities) # This will be an in/out buffer
        color_ids_buf = cl_array.to_device(self.queue, color_ids)
        matrix_buf = cl_array.to_device(self.queue, matrix_flat)
        
        # Output buffer for positions
        out_pos_buf = cl_array.empty_like(pos_buf)

        # --- Execute Kernel ---
        self.prg.interactions(
            self.queue, (num_particles,), None,
            pos_buf.data,
            color_ids_buf.data,
            matrix_buf.data,
            vel_buf.data, # Pass velocities as an in/out buffer
            out_pos_buf.data,
            numpy.float32(self.max_Radius),
            numpy.float32(self.beta),
            numpy.float32(self.force_Factor),
            numpy.float32(self.friction_Factor),
            numpy.int32(num_particles)
        )
        self.queue.finish()

        # --- Retrieve results ---
        updated_positions = out_pos_buf.get()
        updated_velocities = vel_buf.get()

        # --- Update particle objects ---
        for i, p in enumerate(self.particles):
            p.pos_x = float(updated_positions[i][0])
            p.pos_y = float(updated_positions[i][1])
            p.vel_x = float(updated_velocities[i][0])
            p.vel_y = float(updated_velocities[i][1])



