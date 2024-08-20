# Orbital-Mechanics

## Overview
This project provides a suite of tools for simulating, analyzing, and visualizing spacecraft trajectories. It is designed for aerospace engineers, researchers, and students who want to study orbital mechanics and spacecraft motion.

## Features
- **Spacecraft Class**: The core of the project, this class allows users to create spacecraft objects with either:
  - A set of Keplerian orbital elements (e.g., semi-major axis, eccentricity, inclination)
  - An initial state vector (position and velocity)

- **Trajectory Propagation**: Once a spacecraft object is defined, its trajectory can be propagated over time using numerical integration methods.

- **Visualization**: The project includes methods to plot and visualize spacecraft trajectories in 2D and 3D, including:
  - Orbit plots
  - Ground tracks
  - State vectors (position and velocity) over time

- **Analysis Tools**: Additional methods allow for the analysis of orbital elements, state vectors, and other parameters critical to mission design and spacecraft operations.

## Development Status
This project is currently under active development. Future updates will include the ability to add perturbations such as:
- **Aerodynamic Drag**: Simulate the effects of atmospheric drag on low Earth orbit spacecraft.
- **Solar Radiation Pressure**: Model the influence of solar radiation on spacecraft trajectories, particularly in high-altitude orbits.

Stay tuned for these and other enhancements!

## Getting Started
### Prerequisites
- Python 3.x
- Required Python libraries: `numpy`, `matplotlib`, `scipy`, etc.

### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/Orbital-Mechanics.git
