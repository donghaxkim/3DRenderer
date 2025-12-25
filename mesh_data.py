import numpy as np

class Mesh:
    def __init__(self):
        # holds 3D coordinates as NumPy array [x, y, z]
        self.vertices = []
        # this list stores the connections betwen points,
        # instead of storing coordinates, it stores 'ID' of the points
        # Example: (0, 1) means a connection between vertex 0 and vertex 1
        self.edges = []

    def add_vertex(self, x, y, z):
        # add a new vertex to the mesh
        # now we wrap the coords into a NumPy array and so we can do math on it
        new_point = np.array([x, y, z], dtype=float)

        self.vertices.append(new_point)

        # We return the Index of this point so the caller knows the ID
        # If this is the first point, it will be 0, if the second point, it will be 1, and so on
        return len(self.vertices) - 1

    def add_edge(self, start_idx, end_idx):
        # This creates a link betwen two points using their IDs
        # We store this as a tuple (start_idx, end_idx)
        connection = (start_idx, end_idx)

        self.edges.append(connection)

    def get_vertex(self, index):
        # This is a helper to grab a specific point's 3D coords using its ID
        return self.vertices[index]

    def get_transformed_vertices(self, matrix):
        # This takes a rotation/translation matrix and applies it to every point in the mesh at once
        # We use NumPy's @ operator to multiply the matrix
        return [matrix @ v for v in self.vertices]
    
    