# AI Development Guide for Python Particle Life

This is a Python implementation of Particle Life, a simulation where particles interact according to attraction/repulsion rules defined in a force matrix. Below are the key aspects AI agents should understand to work effectively with this codebase.

## Architecture Overview

The simulation is built with a Model-View-Controller pattern:

### Core Components
- `PhysicsEngine.py` - Model: Handles particle physics and interactions
  - Uses a force matrix (3x3) to define interactions between 3 particle types (R,G,B)
  - Supports both CPU and GPU (OpenCL) implementations
  - Key parameters: max_radius, friction_factor, force_factor, beta

- `Main.py` - Controller: Main loop and event handling
  - Initializes PyGame and core components
  - Handles user input and window management
  - Target frame rate: 31 FPS
  
- View Components:
  - `Camera.py` - Handles view transformation and zooming
  - `Menu.py` - UI controls for simulation parameters
  - `forceGraph.py` - Visualizes force relationships
  - `matrixView.py` - Matrix editor interface

### Data Flow
1. User input → Main.py
2. Parameter updates via Menu/UI → PhysicsEngine 
3. PhysicsEngine calculates particle positions
4. Camera transforms coordinates for display
5. PyGame renders frame

## Key Workflows

### Running the Simulation
```bash
python particle_Life_OOP/Main.py
```

### Controls
- Space: Pause/Resume simulation
- Mouse wheel: Zoom in/out
- Mouse drag: Pan camera
- 'M' button: Toggle menu
- '+/-' buttons: Add/Remove particles
- 'R' button: Randomize force matrix

### Modifying Force Rules
1. Use Matrix View ('G/M' button to toggle)
2. Edit values in range [-1.0, 1.0]
3. Save/Load matrices via JSON

## Project-Specific Patterns

### Particle Interactions
- Normalized coordinate space (0.0-1.0)
- Periodic boundary conditions (wrapping)
- Force calculation:
  ```python
  if r < beta:
      return (r/beta) - 1  # Repulsion
  elif beta < r < 1:
      return a * (1-abs(-(2*r-2)/(1-beta)-1))  # Attraction/Repulsion
  else:
      return 0  # No effect
  ```

### Performance Optimization
- GPU acceleration via OpenCL when available
- Fallback to CPU implementation
- Configurable particle count (recommended: 200-5000)

### UI Components
- Button.py: Generic button class with callbacks
- Slider.py: Value adjustment with input box
- Common styling: segoeui font, dark theme colors

## Integration Points

### Matrix File Format
```json
[{
    "name": "matrix1",
    "matrix": [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]
}]
```

### Key Files for Common Tasks
- Add new UI controls: Menu.py
- Modify physics: PhysicsEngine.py
- Adjust visualization: Camera.py
- Change saved states: SavedMatrix.json
