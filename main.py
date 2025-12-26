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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Use a slightly smaller font for the minimalistic feel
font = pygame.font.SysFont("Consolas", 14)
clock = pygame.time.Clock()

mesh = Mesh(); FOV, DIST = 600, 500
INITIAL_FOV = FOV  # Store initial FOV as zoom out cap
MAX_ZOOM_IN = 2000  # Maximum zoom in limit
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
    
    mouse_dx = mouse_pos[0] - last_mouse_pos[0]
    mouse_dy = mouse_pos[1] - last_mouse_pos[1]
    last_mouse_pos = mouse_pos

    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]

    hover_v = None; hover_e = None
    for i, p in enumerate(projected):
        if math.hypot(mouse_pos[0]-p[0], mouse_pos[1]-p[1]) < 10:
            hover_v = i; break
    if hover_v is None:
        for i, (s, e) in enumerate(mesh.edges):
            if line_dist(mouse_pos, projected[s], projected[e]) < 5:
                hover_e = i; break

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if hover_v is not None: drag_start_idx = hover_v
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST)
                    drag_start_idx = mesh.add_vertex(world_v)
                    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]
            elif event.button == 3:
                if hover_v is not None: moving_v_idx = hover_v

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drag_start_idx is not None:
                if hover_v is not None: mesh.add_edge(drag_start_idx, hover_v)
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST)
                    new_idx = mesh.add_vertex(world_v)
                    mesh.add_edge(drag_start_idx, new_idx)
                    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST) for v in mesh.vertices]
                drag_start_idx = None
            elif event.button == 3: moving_v_idx = None
            
        if event.type == pygame.MOUSEWHEEL:
            # Zoom in/out by adjusting FOV
            zoom_factor = 50  # Amount to change FOV per scroll
            if event.y > 0:  # Scroll up - zoom in
                FOV = min(FOV + zoom_factor, MAX_ZOOM_IN)
            else:  # Scroll down - zoom out
                FOV = max(FOV - zoom_factor, INITIAL_FOV)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB: active_axis = "X" if active_axis == "Y" else "Y"
            if event.key == pygame.K_d:
                if hover_v is not None: mesh.remove_vertex(hover_v)
                elif hover_e is not None: mesh.remove_edge(hover_e)
            if event.key == pygame.K_c: 
                mesh.clear()
                angle_x = angle_y = 0
            if event.key == pygame.K_SPACE: mesh.auto_loop()

    if moving_v_idx is not None:
        scale = DIST / FOV
        move_vec_screen = np.array([mouse_dx * scale, -mouse_dy * scale, 0])
        move_vec_world = rot_mat.T @ move_vec_screen
        mesh.vertices[moving_v_idx] += move_vec_world

    if keys[pygame.K_r]:
        rel_x, rel_y = pygame.mouse.get_rel()
        if active_axis == "Y": angle_y += rel_x * 0.005
        else: angle_x += rel_y * 0.005
    else:
        pygame.mouse.get_rel()

    # --- RENDER ---
    for i, (s, e) in enumerate(mesh.edges):
        if s < len(projected) and e < len(projected):
            color = (255, 0, 0) if i == hover_e else (128, 0, 128)
            pygame.draw.line(screen, color, projected[s], projected[e], 1)
        
    if drag_start_idx is not None and drag_start_idx < len(projected):
        pygame.draw.line(screen, (50, 150, 50), projected[drag_start_idx], mouse_pos, 1)
        
    for i, p in enumerate(projected):
        color = (255, 255, 255)
        if i == hover_v: color = (220, 50, 50)
        if i == moving_v_idx: color = (220, 220, 50)
        pygame.draw.circle(screen, color, p, 3 if i == hover_v else 2)

    # --- MINIMAL UI ---
    deg_x, deg_y = int(math.degrees(angle_x)) % 360, int(math.degrees(angle_y)) % 360
    
    # Top-Left: Angles
    screen.blit(font.render(f"AXIS-{active_axis}", True, (100, 255, 100)), (10, 10))
    screen.blit(font.render(f"X: {deg_x}°", True, (150, 150, 150)), (10, 25))
    screen.blit(font.render(f"Y: {deg_y}°", True, (150, 150, 150)), (10, 40))

    # Bottom-Left: Legend
    shortcuts = ["R: Rotate", "TAB: Axis", "SPACE: Poly", "D: Del", "C: Clear"]
    for i, text in enumerate(shortcuts):
        screen.blit(font.render(text, True, (80, 80, 80)), (10, HEIGHT - 20 * (len(shortcuts) - i)))

    # Top-Right: Status
    status = "ROTATING" if keys[pygame.K_r] else "EDITING"
    status_col = (200, 200, 50) if status == "ROTATING" else (100, 100, 100)
    status_surface = font.render(status, True, status_col)
    screen.blit(status_surface, (WIDTH - status_surface.get_width() - 10, 10))

    pygame.display.flip(); clock.tick(60)
pygame.quit()