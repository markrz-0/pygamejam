import pygame

def wsad(deltatime, position, movement_speed, max_offset):
    x, y = position
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        y += deltatime * movement_speed
    if keys[pygame.K_s]:
        y -= deltatime * movement_speed

    if keys[pygame.K_a]:
        x += deltatime * movement_speed
    if keys[pygame.K_d]:
        x -= deltatime * movement_speed

    if max_offset is not None:
        if abs(x) > max_offset:
            if x > 0:
                x = max_offset
            else:
                x = -max_offset

        if abs(y) > max_offset:
            if y > 0:
                y = max_offset
            else:
                y = -max_offset

    return x, y