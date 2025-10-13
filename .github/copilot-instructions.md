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
  ## AI guidance — PythonParticlelife (concise)

  This repo implements a small particle-interaction simulator using PyGame. The goal of this file is to give an AI agent the exact, discoverable knowledge needed to be productive: where to change behavior, how data flows, and project-specific conventions.

  - Run: `python particle_Life_OOP/Main.py` (Main initializes PyGame, FPS lock ~31).
  - Main components:
    - `particle_Life_OOP/physicsEngine.py` (CPU physics) and `physicsEngine_copy.py` (OpenCL + numpy). Use the `_copy` file to see GPU/OpenCL implementation details and buffer layout.
    - `particle_Life_OOP/Main.py` — main loop, event routing, calls `physics_engine.interactions()` and draws via `Camera.drawParticles()`.
    - UI: `Menu.py`, `matrixView.py`, `forceGraph.py`, `saveLoad.py`, `Button.py`, `Slider.py`. `Taskbar` (in `Menu.py`) handles top-level buttons (M, +, -, R, Pause, exit).

  - Important data & conventions:
    - Particle coordinates are normalized to [0.0, 1.0] and use periodic boundary wrapping (see `PhysicsEngine.force` and OpenCL kernel in `physicsEngine_copy.py`).
    - Physics parameters: `max_Radius`, `beta`, `force_Factor`, `friction_Factor`. These appear in `PhysicsEngine` and are wired to UI sliders in `Menu.py`.
    - Force matrix: 3x3 list of floats (one row per particle colour). The JSON saved format is a list of objects: `{ "name": "...", "matrix": [[..],[..],[..]] }` stored in `SavedMatrix.json` (see `saveLoad.py`). Note `saveLoad.py` attempts two relative paths: `SavedMatrix.json` and `particle_Life_OOP//SavedMatrix.json`.

  - OpenCL notes (what to watch for):
    - `physicsEngine_copy.py` builds a kernel expecting flattened matrix (row-major) and float32 buffers for positions/velocities. It falls back to CPU if OpenCL fails. If you modify the kernel, update host buffer shapes and types accordingly.
    - The code uses `pyopencl` and `pyopencl.array` — include `numpy` float32 arrays when creating buffers.

  - UI & event patterns worth copying:
    - `Menu.input_event(event)` forwards events to sliders and `matrix_view.input_event`.
    - Buttons are instantiated with a callback and drawn on a `Surface`. Click handling computes relative mouse coords before calling `Button.click()` (see `saveLoad.event_handler`, `Menu.Taskbar.click_buttons`).
    - Camera is a square `Surface` (`Camera.cam_size`) and uses `zoomIn/zoomOut` which adjust `cam_x/cam_y` to keep the mouse focal point stable.

  - Quick change targets (where to edit for common tasks):
    - Change physics logic: `particle_Life_OOP/physicsEngine.py` (or GPU variant `physicsEngine_copy.py`).
    - Add UI controls: `particle_Life_OOP/Menu.py` and `Button.py` / `Slider.py`.
    - Save/load matrices: `particle_Life_OOP/saveLoad.py` and `SavedMatrix.json` format.

  - Tests & build: no test harness present. To run locally you need Python with `pygame` installed; for GPU run add `pyopencl` and `numpy`. The repository uses no packaging; rely on a virtualenv and `pip install pygame numpy pyopencl` as needed.

  If anything here is unclear or you want more detail about a specific file (for example, the OpenCL kernel args or the exact JSON read/write fallback logic in `saveLoad.py`), tell me which area and I will expand that section.
### Modifying Force Rules
