import numpy as np

def get_rotation_matrix(angle_x, angle_y):
    rx = np.array([[1, 0, 0],
                   [0, np.cos(angle_x), -np.sin(angle_x)],
                   [0, np.sin(angle_x), np.cos(angle_x)]])
    ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                   [0, 1, 0],
                   [-np.sin(angle_y), 0, np.cos(angle_y)]])
    return ry @ rx

def project(vertex, width, height, fov, viewer_distance, pan_x=0, pan_y=0):
    z = vertex[2] + viewer_distance
    if z <= 0.1: z = 0.1
    factor = fov / z
    # Apply pan offsets to the projection
    x_2d = vertex[0] * factor + width / 2 + pan_x
    y_2d = -vertex[1] * factor + height / 2 + pan_y
    return (int(x_2d), int(y_2d))

def screen_to_world(mouse_pos, width, height, rot_matrix, fov, viewer_distance, pan_x=0, pan_y=0):
    # Reverse the pan and center offsets
    x_2d = (mouse_pos[0] - width / 2 - pan_x)
    y_2d = -(mouse_pos[1] - height / 2 - pan_y)
    
    scale = viewer_distance / fov
    world_vec = rot_matrix.T @ np.array([x_2d * scale, y_2d * scale, 0])
    return world_vec