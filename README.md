# 3D Vector Renderer

An interactive wireframe 3D engine built with Python, Pygame, and NumPy. Create 3D "exoskeletons" from scratch by clicking to place vertices and watch them connect automatically. Rotate your creation in real-time using arrow keys!

## Features

- **Interactive Vertex Placement**: Click anywhere on the screen to place vertices in 3D space at z=0
- **Automatic Edge Creation**: Consecutive vertices are automatically connected with edges
- **Real-time 3D Rotation**: Use arrow keys to rotate your wireframe around all three axes
- **Perspective Projection**: Proper 3D-to-2D projection using perspective division (dividing by Z)
- **Modular Architecture**: Clean separation into mesh data, math engine, and rendering components

## Project Structure

```
3D Vector Renderer/
├── mesh_data.py      # Vertex, Edge, and Mesh classes for 3D structure storage
├── math_engine.py    # Rotation matrices and perspective projection pipeline
├── main.py           # Interactive Pygame loop and rendering
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

### File Descriptions

- **mesh_data.py**: Defines the data structures for storing 3D wireframe geometry
  - `Vertex`: Represents a point in 3D space with homogeneous coordinates
  - `Edge`: Represents a connection between two vertices
  - `Mesh`: Container for vertices and edges with management methods

- **math_engine.py**: Handles all 3D transformations and projections
  - Rotation matrices for X, Y, and Z axes
  - Perspective projection using Z-division
  - Screen-to-3D coordinate conversion
  - Transformation application to vertex arrays

- **main.py**: Main application with Pygame rendering loop
  - Interactive vertex placement via mouse clicks
  - Real-time rotation controls
  - Wireframe rendering with perspective projection
  - Visual feedback and grid overlay

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pygame numpy
   ```

## Usage

Run the main application:

```bash
python main.py
```

### Controls

| Input | Action |
|-------|--------|
| **Left Click** | Place a vertex at z=0 (automatically connects to previous vertex) |
| **Arrow Keys** | Rotate the 3D object |
| **↑/↓** | Rotate around X-axis (pitch) |
| **←/→** | Rotate around Y-axis (yaw) |
| **Q/E** | Rotate around Z-axis (roll) |
| **C** | Clear all vertices and edges |
| **R** | Reset rotation to default view |
| **ESC** | Quit the application |

## How It Works

### 1. Mesh Data System
The `Mesh` class stores vertices as 3D points using homogeneous coordinates (x, y, z, 1) and edges as index pairs. This allows for efficient matrix transformations.

### 2. Transformation Pipeline
The math engine applies rotation matrices to transform vertices:
- **Rotation Matrices**: 4×4 matrices for rotating around X, Y, and Z axes
- **Matrix Composition**: Multiple rotations are combined by matrix multiplication
- **Homogeneous Coordinates**: Enable translation and rotation in a unified system

### 3. Perspective Projection
3D coordinates are projected to 2D screen space using:
```
x_screen = (x * fov) / (z + fov) + center_x
y_screen = -(y * fov) / (z + fov) + center_y
```

This creates realistic depth perception where objects farther away appear smaller.

### 4. Interactive Loop
The Pygame loop:
1. Captures mouse clicks to add vertices at z=0
2. Automatically creates edges between consecutive vertices
3. Applies rotation based on arrow key input
4. Projects and renders the wireframe every frame

## Mathematical Concepts

### Rotation Matrices

**X-axis rotation** (pitch):
```
[1    0       0    0]
[0  cos(θ) -sin(θ) 0]
[0  sin(θ)  cos(θ) 0]
[0    0       0    1]
```

**Y-axis rotation** (yaw):
```
[ cos(θ)  0  sin(θ)  0]
[   0     1    0     0]
[-sin(θ)  0  cos(θ)  0]
[   0     0    0     1]
```

**Z-axis rotation** (roll):
```
[cos(θ) -sin(θ)  0  0]
[sin(θ)  cos(θ)  0  0]
[  0       0     1  0]
[  0       0     0  1]
```

### Perspective Projection

The perspective projection simulates how the human eye perceives depth by dividing x and y coordinates by the z-coordinate (with offset):

- Objects further away (larger z) appear smaller
- Objects closer (smaller z) appear larger
- The field of view (fov) parameter controls the perspective strength

## Examples

Try creating:
- **Simple Square**: Click 4 points in a square pattern, then rotate
- **Star Pattern**: Click points in a star shape and watch it rotate
- **3D Spiral**: Although clicks are at z=0, rotation reveals the 2D to 3D transformation
- **Connect the Dots**: Create any pattern and explore it from different angles

## Extending the Project

Potential enhancements:
- Add face/polygon rendering with z-buffering
- Implement depth-based vertex coloring
- Add z-axis control for vertex placement
- Support for loading/saving mesh data
- Camera movement (translation)
- Multiple mesh objects
- Lighting and shading

## Requirements

- Python 3.7+
- Pygame 2.5.0+
- NumPy 1.24.0+

## License

This project is free to use for educational purposes.

---

**Enjoy building your 3D wireframes!** 🎨✨

