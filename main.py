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

# initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Consolas", 14)
clock = pygame.time.Clock()

mesh = Mesh(); FOV, DIST = 600, 500
angle_x = 0; angle_y = 0
pan_x = 0; pan_y = 0 
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

    # pipeline: project vertices (grid removed)
    projected = [project(rot_mat @ v, WIDTH, HEIGHT, FOV, DIST, pan_x, pan_y) for v in mesh.vertices]

    # hover detection
    hover_v = None; hover_e = None
    for i, p in enumerate(projected):
        if math.hypot(mouse_pos[0]-p[0], mouse_pos[1]-p[1]) < 10:
            hover_v = i; break
    if hover_v is None:
        for i, (s, e) in enumerate(mesh.edges):
            if line_dist(mouse_pos, projected[s], projected[e]) < 5:
                hover_e = i; break

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if hover_v is not None: drag_start_idx = hover_v
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST, pan_x, pan_y)
                    drag_start_idx = mesh.add_vertex(world_v)
            elif event.button == 3:
                if hover_v is not None: moving_v_idx = hover_v

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drag_start_idx is not None:
                if hover_v is not None: mesh.add_edge(drag_start_idx, hover_v)
                else:
                    world_v = screen_to_world(mouse_pos, WIDTH, HEIGHT, rot_mat, FOV, DIST, pan_x, pan_y)
                    mesh.add_edge(drag_start_idx, mesh.add_vertex(world_v))
                drag_start_idx = None
            elif event.button == 3: moving_v_idx = None
            
        if event.type == pygame.MOUSEWHEEL:
            zoom_speed = 0.1
            old_fov = FOV
            if event.y > 0: FOV *= (1 + zoom_speed)
            else: FOV *= (1 - zoom_speed)
            
            FOV = max(200, min(FOV, 5000))
            multiplier = (FOV / old_fov) - 1
            pan_x -= (mouse_pos[0] - WIDTH/2 - pan_x) * multiplier
            pan_y -= (mouse_pos[1] - HEIGHT/2 - pan_y) * multiplier
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB: active_axis = "X" if active_axis == "Y" else "Y"
            if event.key == pygame.K_d:
                if hover_v is not None: mesh.remove_vertex(hover_v)
                elif hover_e is not None: mesh.remove_edge(hover_e)
            if event.key == pygame.K_c: 
                mesh.clear()
                angle_x = angle_y = pan_x = pan_y = 0
                FOV = 600
            if event.key == pygame.K_SPACE: mesh.auto_loop()

    # movement logic
    if moving_v_idx is not None:
        scale = DIST / FOV
        move_vec_screen = np.array([mouse_dx * scale, -mouse_dy * scale, 0])
        mesh.vertices[moving_v_idx] += rot_mat.T @ move_vec_screen

    # rotation logic
    if keys[pygame.K_r]:
        rel_x, rel_y = pygame.mouse.get_rel()
        if active_axis == "Y": angle_y += rel_x * 0.005
        else: angle_x += rel_y * 0.005
    else: pygame.mouse.get_rel()

    # render
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

    # ui
    deg_x, deg_y = int(math.degrees(angle_x)) % 360, int(math.degrees(angle_y)) % 360
    
    # angles and axis
    screen.blit(font.render(f"AXIS-{active_axis}", True, (100, 255, 100)), (10, 10))
    screen.blit(font.render(f"X: {deg_x}°", True, (150, 150, 150)), (10, 25))
    screen.blit(font.render(f"Y: {deg_y}°", True, (150, 150, 150)), (10, 40))

    # legend
    shortcuts = ["R: Rotate", "TAB: Axis", "SPACE: Poly", "D: Del", "C: Clear"]
    for i, text in enumerate(shortcuts):
        screen.blit(font.render(text, True, (80, 80, 80)), (10, HEIGHT - 20 * (len(shortcuts) - i)))

    # status
    status = "ROTATING" if keys[pygame.K_r] else "EDITING"
    status_col = (200, 200, 50) if status == "ROTATING" else (100, 100, 100)
    status_surface = font.render(status, True, status_col)
    screen.blit(status_surface, (WIDTH - status_surface.get_width() - 10, 10))

    pygame.display.flip(); clock.tick(60)
pygame.quit()