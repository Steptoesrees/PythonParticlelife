#include <cmath>
#include <vector>
#include <cstdint>

extern "C" {

// Helper for index calculation
#define IDX(i, j, n) ((i)*(n)+(j))

void update_particles(
    float* xpos, float* ypos, float* xvel, float* yvel, int* colours,
    int particle_num, float* matrix, int colour_num,
    float beta, float max_radius, float force_factor, float friction_factor
) {
    for (int i = 0; i < particle_num; ++i) {
        float total_force_x = 0.0f;
        float total_force_y = 0.0f;
        int ci = colours[i];
        for (int j = 0; j < particle_num; ++j) {
            if (i == j) continue;
            float dx = xpos[j] - xpos[i];
            float dy = ypos[j] - ypos[i];
            // Wrap distances
            if (fabs(dx) > 0.5f) dx -= copysignf(1.0f, dx);
            if (fabs(dy) > 0.5f) dy -= copysignf(1.0f, dy);
            float radius = sqrtf(dx*dx + dy*dy);
            if (radius > 0.0f && radius < max_radius) {
                int cj = colours[j];
                float a = matrix[IDX(ci, cj, colour_num)];
                float r = radius / max_radius;
                float f = 0.0f;
                if (r < beta) f = (r / beta) - 1.0f;
                else if (r < 1.0f) f = a * (1.0f - fabsf(-(2*r-2)/(1-beta)-1));
                // else f = 0
                total_force_x += dx / radius * f;
                total_force_y += dy / radius * f;
            }
        }
        total_force_x *= max_radius * force_factor;
        total_force_y *= max_radius * force_factor;
        xvel[i] *= friction_factor;
        yvel[i] *= friction_factor;
        xvel[i] += total_force_x * 0.01f;
        yvel[i] += total_force_y * 0.01f;
        xpos[i] += xvel[i] * 0.01f;
        ypos[i] += yvel[i] * 0.01f;
    }
}

}