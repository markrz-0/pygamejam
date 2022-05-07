import enum

class Collider(enum.Enum):
    RECT = 0
    CIRCLE = 1


def circle_collider(click_pos, position, radius_squared):
    dist_squared = (click_pos[0] - position[0]) ** 2 + \
                   (click_pos[1] - position[1]) ** 2

    return dist_squared < radius_squared

def rect_collider(click_pos, position, size):
    min_x = position[0] - size[0] // 2
    max_x = position[0] + size[0] // 2
    click_x = click_pos[0]
    is_x_in_bounds = min_x <= click_x <= max_x

    min_y = position[1] - size[1] // 2
    max_y = position[1] + size[1] // 2
    click_y = click_pos[1]
    is_y_in_bounds = min_y <= click_y <= max_y

    return is_x_in_bounds and is_y_in_bounds
