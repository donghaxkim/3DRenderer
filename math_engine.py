import numpy as np

def get_rotation_matrix(angle_x, angle_y):
    # This creates a 3D matrix that tells points how to spin
    #angle_x: how much to spin around the x-axis
    #angle_y: how much to spin around the y-axis

    # Matrix for spinning around the x-axis
    rot_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    # Matrix for spinning around the y-axis
    rot_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    # Multiply them together using @ for matrix multiplication
    return rot_x @ rot_y

def project(vertex, screen_width, screen_height, fov, viewer_distance):
    # This converts 3D coordinates to 2D screen coordinates
    # We add viewer_distance to the z-coordinate to make sure the closer objects are smaller
    z = vertex[2] + viewer_distance

    # Saftey check to avoid division by zero, don't divide by zero if a point is behind the  camera
    if z <= 0: z = 0.1

    # fov controls the width of the lens
    # Dividing by z makes distant objects move toward the center
    factor = fov / z

    x_2d = vertex[0] * factor
    y_2d = vertex[1] * factor

    # Convert to screen coordinates
    return (
        int(x_2d + screen_width / 2),
        int(-y_2d + screen_height / 2)
    )