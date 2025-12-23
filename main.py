"""
main.py
Interactive 3D wireframe renderer with Pygame.
Click to place vertices, arrow keys to rotate the 3D object.
"""

import pygame
import numpy as np
from mesh_data import Mesh
from math_engine import MathEngine


class VectorRenderer:
    """Main application class for the 3D Vector Renderer."""
    
    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize the renderer.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        pygame.init()
        
        # Screen setup
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Vector Renderer - Click to add vertices, Arrow keys to rotate")
        
        # Core components
        self.mesh = Mesh()
        self.math_engine = MathEngine(width, height, fov=500.0)
        
        # Rotation angles
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0
        
        # Rotation speed
        self.rotation_speed = 0.05
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.vertex_color = (100, 200, 255)
        self.edge_color = (255, 255, 255)
        self.grid_color = (50, 50, 60)
        
        # Vertex size
        self.vertex_radius = 5
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Running flag
        self.running = True
    
    def draw_grid(self):
        """Draw a reference grid on the screen."""
        # Vertical lines
        for x in range(0, self.width, 50):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height), 1)
        
        # Horizontal lines
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y), 1)
        
        # Center crosshair
        center_x = self.width // 2
        center_y = self.height // 2
        pygame.draw.line(self.screen, (80, 80, 90), (center_x - 20, center_y), (center_x + 20, center_y), 2)
        pygame.draw.line(self.screen, (80, 80, 90), (center_x, center_y - 20), (center_x, center_y + 20), 2)
    
    def handle_events(self):
        """Process user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.add_vertex_at_mouse(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_c:
                    # Clear the mesh
                    self.mesh.clear()
                    print("Mesh cleared!")
                
                elif event.key == pygame.K_r:
                    # Reset rotation
                    self.rotation_x = 0.0
                    self.rotation_y = 0.0
                    self.rotation_z = 0.0
                    print("Rotation reset!")
        
        # Handle continuous key presses for rotation
        keys = pygame.key.get_pressed()
        
        # Arrow keys for Y and X rotation
        if keys[pygame.K_LEFT]:
            self.rotation_y -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.rotation_y += self.rotation_speed
        if keys[pygame.K_UP]:
            self.rotation_x -= self.rotation_speed
        if keys[pygame.K_DOWN]:
            self.rotation_x += self.rotation_speed
        
        # Q/E for Z rotation
        if keys[pygame.K_q]:
            self.rotation_z -= self.rotation_speed
        if keys[pygame.K_e]:
            self.rotation_z += self.rotation_speed
    
    def add_vertex_at_mouse(self, pos: tuple):
        """
        Add a vertex at the mouse position.
        
        Args:
            pos: Tuple of (x, y) screen coordinates
        """
        # Convert screen coordinates to 3D coordinates at z=0
        x, y, z = self.math_engine.screen_to_3d(pos[0], pos[1], z=0.0)
        
        # Add vertex to mesh
        vertex_index = self.mesh.add_vertex(x, y, z)
        
        # If this is not the first vertex, create an edge from the previous vertex
        if len(self.mesh.vertices) > 1:
            self.mesh.add_edge(vertex_index - 1, vertex_index)
        
        print(f"Added vertex {vertex_index}: ({x:.2f}, {y:.2f}, {z:.2f})")
    
    def render(self):
        """Render the mesh to the screen."""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw grid
        self.draw_grid()
        
        # If there are no vertices, display instructions
        if len(self.mesh.vertices) == 0:
            self.draw_instructions()
            return
        
        # Get vertex positions
        vertices = self.mesh.get_vertex_positions()
        
        # Apply rotations
        rot_x = self.math_engine.rotation_matrix_x(self.rotation_x)
        rot_y = self.math_engine.rotation_matrix_y(self.rotation_y)
        rot_z = self.math_engine.rotation_matrix_z(self.rotation_z)
        
        # Combined rotation matrix
        combined_rotation = rot_z @ rot_y @ rot_x
        
        # Transform vertices
        transformed_vertices = self.math_engine.apply_transformation(vertices, combined_rotation)
        
        # Project to 2D
        projected_vertices = self.math_engine.perspective_project(transformed_vertices)
        
        # Draw edges
        for edge in self.mesh.edges:
            start_pos = projected_vertices[edge.start]
            end_pos = projected_vertices[edge.end]
            
            # Check if both points are on screen
            if self.is_on_screen(start_pos) or self.is_on_screen(end_pos):
                pygame.draw.line(
                    self.screen,
                    self.edge_color,
                    (int(start_pos[0]), int(start_pos[1])),
                    (int(end_pos[0]), int(end_pos[1])),
                    2
                )
        
        # Draw vertices
        for vertex_2d in projected_vertices:
            if self.is_on_screen(vertex_2d):
                pygame.draw.circle(
                    self.screen,
                    self.vertex_color,
                    (int(vertex_2d[0]), int(vertex_2d[1])),
                    self.vertex_radius
                )
        
        # Draw info
        self.draw_info()
    
    def is_on_screen(self, pos: np.ndarray, margin: int = 100) -> bool:
        """
        Check if a point is visible on screen (with margin for off-screen drawing).
        
        Args:
            pos: 2D position array
            margin: Extra margin around screen bounds
        
        Returns:
            True if position is within screen bounds (plus margin)
        """
        return (-margin <= pos[0] <= self.width + margin and
                -margin <= pos[1] <= self.height + margin)
    
    def draw_instructions(self):
        """Draw instructions when no vertices exist."""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        title = font.render("3D Vector Renderer", True, (255, 255, 255))
        inst1 = small_font.render("Click anywhere to place vertices", True, (200, 200, 200))
        inst2 = small_font.render("Arrow keys to rotate", True, (200, 200, 200))
        inst3 = small_font.render("Q/E to rotate on Z-axis", True, (200, 200, 200))
        inst4 = small_font.render("C to clear, R to reset rotation, ESC to quit", True, (200, 200, 200))
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 80))
        self.screen.blit(inst1, (self.width // 2 - inst1.get_width() // 2, self.height // 2 - 20))
        self.screen.blit(inst2, (self.width // 2 - inst2.get_width() // 2, self.height // 2 + 10))
        self.screen.blit(inst3, (self.width // 2 - inst3.get_width() // 2, self.height // 2 + 40))
        self.screen.blit(inst4, (self.width // 2 - inst4.get_width() // 2, self.height // 2 + 70))
    
    def draw_info(self):
        """Draw information overlay."""
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            f"Vertices: {len(self.mesh.vertices)}",
            f"Edges: {len(self.mesh.edges)}",
            f"Rotation: X={self.rotation_x:.2f} Y={self.rotation_y:.2f} Z={self.rotation_z:.2f}",
        ]
        
        y_offset = 10
        for line in info_lines:
            text = font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def run(self):
        """Main application loop."""
        print("3D Vector Renderer Started!")
        print("Controls:")
        print("  - Click to place vertices at z=0")
        print("  - Arrow keys: Rotate around X and Y axes")
        print("  - Q/E: Rotate around Z axis")
        print("  - C: Clear mesh")
        print("  - R: Reset rotation")
        print("  - ESC: Quit")
        
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
        print("Renderer closed.")


def main():
    """Entry point for the application."""
    renderer = VectorRenderer(width=800, height=600)
    renderer.run()


if __name__ == "__main__":
    main()

