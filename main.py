import pygame
import numpy as np
import math
from mesh_data import Mesh
from math_engine import get_rotation_matrix, project, screen_to_world

def line_dist(p, a, b):
    px, py = p; ax, ay = a; bx, by = b
    dist_sq = (ax-bx)**2 + (ay-by)**2
    if dist_sq == 0: return math.hypot(px-ax, py-ay)
    t = max(0, min(1, ((px-ax)*(bx-ax) + (py-ay)*(by-ay)) / dist_sq))
    return math.hypot(px - (ax + t*(bx-ax)), py - (ay + t*(by-ay)))

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # This defines 'screen'
font = pygame.font.SysFont("Consolas", 18)
clock = pygame.time.Clock()

mesh = Mesh(); FOV, DIST = 600, 500
angle_x = 0; angle_y = 0
active_axis = "Y" 
drag_start_idx = None
moving_v_idx = None 
last_mouse_pos = (0, 0)

running = True
while running:
    screen.fill((10, 10, 10))
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    rot_mat = get_rotation_matrix(angle_x, angle_y)
    
    # Delta for smooth movement
    mouse_dx = mouse_pos[0] - last_mouse_pos[0]
    mouse_dy = mouse_pos[1] - last_mouse_pos[1]
    last_mouse_pos = mouse_pos

    # 1. Pipeline: Project
    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]

    # 2. Interaction: Hover
    hover_v = None; hover_e = None
    for i, p in enumerate(projected):
        if math.hypot(mouse_pos[0]-p[0], mouse_pos[1]-p[1]) < 10:
            hover_v = i; break
    if hover_v is None:
        for i, (s, e) in enumerate(mesh.edges):
            if line_dist(mouse_pos, projected[s], projected[e]) < 5:
                hover_e = i; break

    # 3. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left: Draw
                if hover_v is not None: 
                    drag_start_idx = hover_v
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST)
                    drag_start_idx = mesh.add_vertex(world_v)
                    # Sync check
                    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]
            elif event.button == 3: # Right: Move
                if hover_v is not None:
                    moving_v_idx = hover_v

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drag_start_idx is not None:
                if hover_v is not None: 
                    mesh.add_edge(drag_start_idx, hover_v)
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST)
                    new_idx = mesh.add_vertex(world_v)
                    mesh.add_edge(drag_start_idx, new_idx)
                    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]
                drag_start_idx = None
            elif event.button == 3:
                moving_v_idx = None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB: active_axis = "X" if active_axis == "Y" else "Y"
            if event.key == pygame.K_d:
                if hover_v is not None: mesh.remove_vertex(hover_v)
                elif hover_e is not None: mesh.remove_edge(hover_e)
            if event.key == pygame.K_c: 
                mesh.clear()
                angle_x = angle_y = 0
            if event.key == pygame.K_SPACE: mesh.auto_loop()

    # 4. Movement: Smart Transform Delta
    if moving_v_idx is not None:
        scale = DIST / FOV
        move_vec_screen = np.array([mouse_dx * scale, -mouse_dy * scale, 0])
        # Un-rotate the delta based on camera angle
        move_vec_world = rot_mat.T @ move_vec_screen
        mesh.vertices[moving_v_idx] += move_vec_world

    # 5. Rotation: (Right increases both X and Y)
    if keys[pygame.K_r]:
        rel_x, rel_y = pygame.mouse.get_rel()
        if active_axis == "Y": angle_y += rel_x * 0.005
        else: angle_x += rel_y * 0.005
    else:
        pygame.mouse.get_rel()

    # 6. DRAWING
    for i, (s, e) in enumerate(mesh.edges):
        if s < len(projected) and e < len(projected):
            color = (255, 255, 0) if i == hover_e else (70, 70, 255)
            pygame.draw.line(screen, color, projected[s], projected[e], 2)
        
    if drag_start_idx is not None and drag_start_idx < len(projected):
        pygame.draw.line(screen, (0, 255, 0), projected[drag_start_idx], mouse_pos, 1)
        
    for i, p in enumerate(projected):
        color = (255, 255, 255)
        if i == hover_v: color = (255, 50, 50)
        if i == moving_v_idx: color = (255, 255, 0)
        pygame.draw.circle(screen, color, p, 4 if i == hover_v else 2)

    # UI
    deg_x, deg_y = int(math.degrees(angle_x)) % 360, int(math.degrees(angle_y)) % 360
    screen.blit(font.render(f"X: {deg_x}°", True, (0, 255, 0) if active_axis == "X" else (150, 150, 150)), (10, 10))
    screen.blit(font.render(f"Y: {deg_y}°", True, (0, 255, 0) if active_axis == "Y" else (150, 150, 150)), (10, 30))

    pygame.display.flip(); clock.tick(60)
pygame.quit()