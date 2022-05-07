from engine import movement


class StaticCamera:
    def __init__(self, position=None, view_size=None, camera_speed=1):
        if position is None:
            position = (0, 0)
        if view_size is None:
            view_size = (400, 300)

        self.position = position
        self.view_size = view_size
        self.camera_speed = camera_speed

    def move(self, deltatime):
        pass

class Camera(StaticCamera):
    def __init__(self, position=None, view_size=None, camera_speed=1, max_cam_offset=None):
        super().__init__(position, view_size, camera_speed)
        self.max_offset = max_cam_offset


    def move(self, deltatime):
        self.position = movement.wsad(deltatime, self.position, self.camera_speed * -1, self.max_offset)