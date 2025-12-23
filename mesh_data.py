"""
mesh_data.py
A system to store vertices (3D points) and edges (connections) in a custom Mesh class.
"""

import numpy as np
from typing import List, Tuple


class Vertex:
    """Represents a point in 3D space."""
    
    def __init__(self, x: float, y: float, z: float):
        """
        Initialize a vertex with 3D coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        """
        self.position = np.array([x, y, z, 1.0])  # Homogeneous coordinates for transformations
    
    def get_3d(self) -> np.ndarray:
        """Return the 3D position as [x, y, z]."""
        return self.position[:3]
    
    def __repr__(self):
        return f"Vertex({self.position[0]:.2f}, {self.position[1]:.2f}, {self.position[2]:.2f})"


class Edge:
    """Represents a connection between two vertices."""
    
    def __init__(self, start_index: int, end_index: int):
        """
        Initialize an edge connecting two vertices.
        
        Args:
            start_index: Index of the starting vertex in the mesh
            end_index: Index of the ending vertex in the mesh
        """
        self.start = start_index
        self.end = end_index
    
    def __repr__(self):
        return f"Edge({self.start} -> {self.end})"


class Mesh:
    """
    A collection of vertices and edges that defines a 3D wireframe structure.
    """
    
    def __init__(self):
        """Initialize an empty mesh."""
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
    
    def add_vertex(self, x: float, y: float, z: float) -> int:
        """
        Add a vertex to the mesh.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        
        Returns:
            The index of the newly added vertex
        """
        vertex = Vertex(x, y, z)
        self.vertices.append(vertex)
        return len(self.vertices) - 1
    
    def add_edge(self, start_index: int, end_index: int):
        """
        Add an edge connecting two vertices.
        
        Args:
            start_index: Index of the starting vertex
            end_index: Index of the ending vertex
        """
        if 0 <= start_index < len(self.vertices) and 0 <= end_index < len(self.vertices):
            edge = Edge(start_index, end_index)
            self.edges.append(edge)
        else:
            raise IndexError("Vertex indices out of range")
    
    def get_vertex_positions(self) -> np.ndarray:
        """
        Get all vertex positions as a numpy array.
        
        Returns:
            Array of shape (N, 4) where N is the number of vertices (homogeneous coordinates)
        """
        if not self.vertices:
            return np.empty((0, 4))
        return np.array([v.position for v in self.vertices])
    
    def update_vertex_positions(self, positions: np.ndarray):
        """
        Update all vertex positions from a numpy array.
        
        Args:
            positions: Array of shape (N, 4) containing new positions
        """
        for i, pos in enumerate(positions):
            if i < len(self.vertices):
                self.vertices[i].position = pos
    
    def clear(self):
        """Remove all vertices and edges from the mesh."""
        self.vertices.clear()
        self.edges.clear()
    
    def __repr__(self):
        return f"Mesh(vertices={len(self.vertices)}, edges={len(self.edges)})"


