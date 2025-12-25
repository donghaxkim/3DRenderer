import numpy as np

class Mesh:
    def __init__(self):
        self.vertices = [] 
        self.edges = []    

    def add_vertex(self, vec):
        self.vertices.append(vec)
        return len(self.vertices) - 1

    def add_edge(self, start_idx, end_idx):
        if start_idx == end_idx: return
        edge = tuple(sorted((start_idx, end_idx)))
        if edge not in self.edges:
            self.edges.append(edge)

    def remove_vertex(self, index):
        if 0 <= index < len(self.vertices):
            self.vertices.pop(index)
            self.edges = [(s-1 if s > index else s, e-1 if e > index else e) 
                          for s, e in self.edges if s != index and e != index]

    def remove_edge(self, index):
        if 0 <= index < len(self.edges):
            self.edges.pop(index)

    def auto_loop(self):
        count = len(self.vertices)
        if count < 2: return
        for i in range(count):
            self.add_edge(i, (i + 1) % count)

    def clear(self):
        self.vertices = []
        self.edges = []