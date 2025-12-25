import pygame
import numpy as np

# import logic from other files
from mesh_data import Mesh
from math_engine import get_rotation_matrix, project

# setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Vector Renderer ")
clock = pygame.time.Clock()
FPS = 60

# initialize mesh
mesh = Mesh()

# initial rotation angles
angle_x = 0
angle_y = 0

# variable to remember the ID of the last point we clicked
last_vertex_idx = None

# main game loop
running = True
while running:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # capture mouse click location
            mx, my = pygame.mouse.get_pos()

            # convert to screen coordinates
            screen_x = mx - WIDTH / 2
            screen_y = -(my - HEIGHT / 2)

            # add the point to the mesh and get the ID
            new_idx = mesh.add_vertex(screen_x, screen_y, 0)

            # if there was a prev point, connect them with an edge
            if last_vertex_idx is not None:
                mesh.add_edge(last_vertex_idx, new_idx)
            
            # update last clicked point
            last_vertex_idx = new_idx


    # rotation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle_x += 0.05
    if keys[pygame.K_RIGHT]:
        angle_x -= 0.05
    if keys[pygame.K_UP]:
        angle_y += 0.05
    if keys[pygame.K_DOWN]:
        angle_y -= 0.05

    # render pipline
    # get current rotation matrix from the math engine
    rot_mat = get_rotation_matrix(angle_x, angle_y)

    # temporary list to store the 2D projected vertices
    projected_vertices = []
    
    # transform and project each vertex to mesh
    for v in mesh.vertices:
        # rotate the 3D point
        rotated_v = rot_mat @ v
        # Project the rotated point to 2D
        p_2d = project(rotated_v, WIDTH, HEIGHT, 600, 500)
        projected_vertices.append(p_2d)

    # draw the edges
    for edge in mesh.edges:
        # edge is a tuple like (0, 1)
        p1 = projected_vertices[edge[0]]
        p2 = projected_vertices[edge[1]]
        pygame.draw.line(screen, (255, 255, 255), p1, p2, 2)

    # refresh screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()








