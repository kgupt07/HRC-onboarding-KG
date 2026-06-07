# Quadruped Locomotion in MuJoCo

![Walking quadruped demo](dog.gif)

A MuJoCo simulation of a four-legged robot dog with motor actuators, a joint-level PD controller, and an open-loop trotting gait for forward locomotion.

## What this project does

1. **Robot model** — A quadruped defined in `xml/dog.xml` with hip and knee motors on each leg (torque-controlled, no position actuators).
2. **Simulation loop** — Loads the model into MuJoCo's interactive viewer and steps physics in real time.
3. **PD control** — Tracks desired joint angles using proportional–derivative feedback on position and velocity.
4. **Walking** — Time-varying joint targets with diagonal leg pairing (trot-style) to produce forward motion.

## Requirements

- Python 3.10+
- [MuJoCo](https://mujoco.org/) with the Python bindings
- NumPy
- Linux, macOS, or WSL (recommended for the MuJoCo viewer)

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install mujoco numpy
```

## Running the simulation

Run these from the project root:

| Script | Description |
|--------|-------------|
| `python visualize_dog.py` | Basic simulation — dog loaded in the viewer with gravity |
| `python visualize_gait1.py` | PD controller holding a static standing pose |
| `python visualize_gait2.py` | Open-loop walking gait with PD tracking |

Each script opens a MuJoCo viewer window. Close the window or press Ctrl+C to exit.

## Project structure

```
.
├── README.md
├── dog.gif                  # Demo recording
├── visualize_dog.py         # Basic sim loop
├── visualize_gait1.py       # PD controller (static pose)
├── visualize_gait2.py       # PD controller + walking gait
└── xml/
    └── dog.xml              # Quadruped model and scene
```

## Acknowledgements

The simulation scene setup in `xml/dog.xml` (checker floor plane, skybox, and lighting) was adapted from starter materials provided by [Purdue Humanoid Robotics Club (HRC)](https://github.com/humanoid-purdue/onboarding-fall25). All robot modeling, control, and locomotion logic is my own work.
