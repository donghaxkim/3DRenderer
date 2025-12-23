"""
math_engine.py
Transformation pipeline with rotation matrices and perspective projection.
"""

import numpy as np
from typing import Tuple


class MathEngine:
    """Handles 3D transformations and projections."""
    
    def __init__(self, screen_width: int, screen_height: int, fov: float = 500.0):
        """
        Initialize the math engine.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            fov: Field of view factor for perspective projection
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fov = fov
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
    
    @staticmethod
    def rotation_matrix_x(angle: float) -> np.ndarray:
        """
        Create a rotation matrix around the X-axis.
        
        Args:
            angle: Rotation angle in radians
        
        Returns:
            4x4 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ])
    
    @staticmethod
    def rotation_matrix_y(angle: float) -> np.ndarray:
        """
        Create a rotation matrix around the Y-axis.
        
        Args:
            angle: Rotation angle in radians
        
        Returns:
            4x4 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ])
    
    @staticmethod
    def rotation_matrix_z(angle: float) -> np.ndarray:
        """
        Create a rotation matrix around the Z-axis.
        
        Args:
            angle: Rotation angle in radians
        
        Returns:
            4x4 rotation matrix
        """
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])
    
    def apply_transformation(self, vertices: np.ndarray, transform_matrix: np.ndarray) -> np.ndarray:
        """
        Apply a transformation matrix to a set of vertices.
        
        Args:
            vertices: Array of shape (N, 4) containing vertex positions
            transform_matrix: 4x4 transformation matrix
        
        Returns:
            Transformed vertices array of shape (N, 4)
        """
        if vertices.size == 0:
            return vertices
        return (transform_matrix @ vertices.T).T
    
    def perspective_project(self, vertices: np.ndarray) -> np.ndarray:
        """
        Project 3D vertices onto 2D screen using perspective projection.
        Uses the formula: x_screen = (x * fov) / (z + fov), y_screen = (y * fov) / (z + fov)
        
        Args:
            vertices: Array of shape (N, 4) containing 3D vertex positions
        
        Returns:
            Array of shape (N, 2) containing 2D screen coordinates
        """
        if vertices.size == 0:
            return np.empty((0, 2))
        
        projected = []
        for vertex in vertices:
            x, y, z, _ = vertex
            
            # Add an offset to prevent division by zero and ensure proper depth
            z_offset = z + self.fov
            
            # Avoid division by very small numbers
            if abs(z_offset) < 0.1:
                z_offset = 0.1 if z_offset >= 0 else -0.1
            
            # Perspective projection: divide by z
            x_proj = (x * self.fov) / z_offset
            y_proj = (y * self.fov) / z_offset
            
            # Convert to screen coordinates (center of screen is origin)
            screen_x = x_proj + self.center_x
            screen_y = -y_proj + self.center_y  # Negative because screen Y increases downward
            
            projected.append([screen_x, screen_y])
        
        return np.array(projected)
    
    def screen_to_3d(self, screen_x: int, screen_y: int, z: float = 0.0) -> Tuple[float, float, float]:
        """
        Convert screen coordinates to 3D coordinates at a given Z depth.
        
        Args:
            screen_x: X coordinate on screen
            screen_y: Y coordinate on screen
            z: Z coordinate in 3D space
        
        Returns:
            Tuple of (x, y, z) in 3D space
        """
        # Reverse the perspective projection
        z_offset = z + self.fov
        
        # Convert screen coordinates back to centered coordinates
        x_centered = screen_x - self.center_x
        y_centered = -(screen_y - self.center_y)  # Negative because screen Y is inverted
        
        # Reverse the projection
        x = (x_centered * z_offset) / self.fov
        y = (y_centered * z_offset) / self.fov
        
        return (x, y, z)

