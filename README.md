# 3D Vector Renderer

An interactive 3D vector graphics editor built with Python and Pygame. Create and manipulate 3D wireframe meshes in real-time with an intuitive mouse-driven interface.

## Features

- **Interactive 3D Mesh Creation**: Click to place vertices and draw edges between them
- **Real-time 3D Rotation**: Rotate the view around X and Y axes using mouse movement
- **Vertex Manipulation**: Move vertices in 3D space while maintaining proper perspective
- **Visual Feedback**: Hover highlighting for vertices and edges
- **Edge Management**: Create, delete, and auto-connect edges
- **Perspective Projection**: Accurate 3D-to-2D projection with configurable field of view

## Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher
- NumPy (automatically installed with Pygame dependencies)

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pygame numpy
   ```

## Usage

### Running the Application

```bash
python main.py
```

A window will open (800x600 pixels) with a dark background. You can immediately start creating 3D meshes.

### Controls

#### Mouse Controls

- **Left Click (Empty Space)**: Create a new vertex at the cursor position in 3D space
- **Left Click (On Vertex)**: Start drawing an edge from that vertex
- **Left Click + Drag (From Vertex)**: Draw a preview line while dragging
- **Left Click Release (On Vertex)**: Complete an edge between two vertices
- **Left Click Release (Empty Space)**: Create a new vertex and connect it to the starting vertex
- **Right Click (On Vertex)**: Select vertex for movement
- **Right Click + Drag**: Move the selected vertex in 3D space (follows cursor with proper perspective)
- **Mouse Movement (While Holding R)**: Rotate the view around the active axis

#### Keyboard Controls

- **R Key (Hold)**: Enable rotation mode
  - Move mouse horizontally to rotate around Y-axis (yaw)
  - Move mouse vertically to rotate around X-axis (pitch)
- **Tab Key**: Toggle active rotation axis (X or Y)
  - Active axis is highlighted in green in the UI
- **D Key**: Delete selected element
  - If hovering over a vertex: Delete that vertex and all connected edges
  - If hovering over an edge: Delete that edge only
- **C Key**: Clear the entire mesh and reset rotation
- **Space Key**: Auto-loop - automatically connect all vertices in order to form a closed loop
- **ESC or Close Window**: Exit the application

### Visual Indicators

- **White Circles**: Regular vertices (2px radius)
- **Red Circles**: Hovered vertex (4px radius)
- **Yellow Circles**: Currently moving vertex
- **Blue Lines**: Regular edges
- **Yellow Lines**: Hovered edge
- **Green Line**: Preview line while drawing an edge
- **Top-left Display**: Shows current rotation angles in degrees
  - Green text: Active rotation axis
  - Gray text: Inactive rotation axis

### Creating Your First Mesh

1. **Start Simple**: Click anywhere to place your first vertex
2. **Add More Vertices**: Click in different locations to add more vertices
3. **Connect Vertices**: 
   - Click on a vertex, then click on another vertex to create an edge
   - Or click and drag from a vertex to see a preview line
4. **Rotate the View**: Hold **R** and move your mouse to see your mesh from different angles
5. **Move Vertices**: Right-click on a vertex, then drag to reposition it in 3D space
6. **Create a Loop**: Press **Space** to automatically connect all vertices in sequence

### Tips and Tricks

- **3D Perspective**: Remember that you're working in 3D space. Vertices may appear to overlap in 2D but are actually at different depths
- **Rotation Axis**: Use **Tab** to switch between X and Y rotation axes for more precise control
- **Vertex Movement**: When moving a vertex, it follows your cursor in 3D space, maintaining proper perspective projection
- **Edge Drawing**: You can draw edges between any two vertices, creating complex wireframe structures
- **Clean Slate**: Use **C** to quickly clear everything and start over

## Technical Details

### Architecture

The application is structured into three main modules:

1. **`main.py`**: Main application loop, event handling, and rendering
2. **`math_engine.py`**: 3D mathematics including rotation matrices and perspective projection
3. **`mesh_data.py`**: Data structure for storing vertices and edges

### Rendering Pipeline

1. **Vertex Transformation**: Apply rotation matrices to 3D vertices
2. **Perspective Projection**: Project 3D coordinates to 2D screen space
3. **Edge Rendering**: Draw lines between projected vertex pairs
4. **Vertex Rendering**: Draw circles at projected vertex positions

### Projection Parameters

- **FOV (Field of View)**: 600 pixels - controls the perspective scaling
- **Viewer Distance**: 500 units - distance of the projection plane from the camera
- **Screen Size**: 800x600 pixels

These values can be adjusted in `main.py` to change the viewing behavior.

### Coordinate System

- **Origin**: Center of the screen
- **X-axis**: Right (positive) / Left (negative)
- **Y-axis**: Up (positive) / Down (negative) in 3D, but inverted on screen
- **Z-axis**: Toward viewer (positive) / Away from viewer (negative)

## Project Structure

```
3D Vector Renderer/
├── main.py              # Main application and event loop
├── math_engine.py       # 3D mathematics (rotation, projection)
├── mesh_data.py         # Mesh data structure (vertices, edges)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── ARCHITECTURE.md     # Detailed technical documentation
```

## Troubleshooting

### Window doesn't open
- Ensure Pygame is properly installed: `pip install pygame`
- Check that you're using Python 3.7 or higher: `python --version`

### Performance issues
- The application runs at 60 FPS by default
- If experiencing lag, reduce the number of vertices/edges
- Close other applications to free up system resources

### Controls not responding
- Make sure the application window has focus (click on it)
- Check that you're using the correct mouse buttons (left for drawing, right for moving)
- Ensure the R key is held down for rotation mode

## Future Enhancements

Potential features for future versions:
- Face/polygon support with fill rendering
- Save/load mesh files
- Multiple mesh objects
- Undo/redo functionality
- Grid and snap-to-grid
- Different rendering modes (wireframe, solid, etc.)

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

Built as an educational project to demonstrate:
- 3D graphics mathematics (matrices, projection)
- Interactive user interfaces
- Real-time rendering techniques
- Software architecture and code organization

For detailed technical documentation, see `ARCHITECTURE.md`.
