import numpy as np

def get_rotation_matrix(angle_x, angle_y):
    # Order: Pitch (X) then Yaw (Y) to keep the vertical axis stable
    rx = np.array([[1, 0, 0],
                   [0, np.cos(angle_x), -np.sin(angle_x)],
                   [0, np.sin(angle_x), np.cos(angle_x)]])
    ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                   [0, 1, 0],
                   [-np.sin(angle_y), 0, np.cos(angle_y)]])
    return ry @ rx

def project(vertex, width, height, fov, viewer_distance):
    z = vertex[2] + viewer_distance
    if z <= 0.1: z = 0.1
    factor = fov / z
    return (int(vertex[0] * factor + width / 2), int(-vertex[1] * factor + height / 2))

def screen_to_world(mouse_pos, width, height, rot_matrix, fov, viewer_distance):
    x_2d, y_2d = mouse_pos[0] - width / 2, -(mouse_pos[1] - height / 2)
    scale = viewer_distance / fov
    return rot_matrix.T @ np.array([x_2d * scale, y_2d * scale, 0])