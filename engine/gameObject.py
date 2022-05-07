import pygame
import typing
from engine import camera
from engine.border import Border
from engine.text import Text
from engine.colliders import *

class PositionOptions(enum.Enum):
    NONE = 0
    CENTER = 1
    START = 2
    END = 3

class CircleRadius:
    ANGLED = 0
    VERTICAL = 1
    HORIZONTAL = 2


class GameObject:
    def __init__(self, collider: Collider,
                 position: tuple[int, int],
                 tag: str = 'undefined',
                 img_path: typing.Optional[str] = None,
                 text: typing.Optional[Text] = None,
                 border: typing.Optional[Border] = None,
                 x_axis = PositionOptions.NONE,
                 y_axis = PositionOptions.NONE,
                 circle_radius = CircleRadius.ANGLED):
        """
        :param collider: collider to use
        :param position: start position
        :param img_path: image path
        :param text: text to render
        :param border: border to render
        :param x_axis: if not PositionOptions.NONE treats position[0] as offset_x
        :param y_axis: if not PositionOptions.NONE treats position[1] as offset_y
        """
        if img_path is not None:
            self.img = pygame.image.load(img_path)
        else:
            self.img = None

        if border is not None:
            self.border = border
        else:
            self.border = None

        if text is not None:
            self.text = text
        else:
            self.text = None

        self.w, self.h = 0, 0

        self.position = position
        self.tag = tag
        self.collider = collider
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.circle_radius = circle_radius

        self.render_pos = (0, 0)

        self.deltatime = 0

    def is_clicked(self, click_pos):
        if self.collider == Collider.CIRCLE:
            # angled
            radius_squared = self.w ** 2 + self.h ** 2

            if self.circle_radius == CircleRadius.VERTICAL:
                radius_squared = (self.h // 2) ** 2
            elif self.circle_radius == CircleRadius.HORIZONTAL:
                radius_squared = (self.w // 2) ** 2

            return circle_collider(click_pos, self.render_pos, radius_squared)

        if self.collider == Collider.RECT:
            return rect_collider(click_pos, self.render_pos, (self.w, self.h))

    def on_click(self):
        pass

    def get_render_position(self, cam_pos, position, size, window_size):
        self.w = max(self.w, size[0])
        self.h = max(self.h, size[1])

        offset_x = 0
        offset_y = 0

        if self.x_axis != PositionOptions.NONE:
            cam_pos = (0, cam_pos[1])
            if self.x_axis == PositionOptions.CENTER:
                offset_x = window_size[0] // 2
            elif self.x_axis == PositionOptions.START:
                offset_x = size[0] // 2
            elif self.x_axis == PositionOptions.END:
                offset_x = window_size[0] - size[0] // 2

        if self.y_axis != PositionOptions.NONE:
            cam_pos = (cam_pos[0], 0)
            if self.y_axis == PositionOptions.CENTER:
                offset_y = window_size[1] // 2
            elif self.y_axis == PositionOptions.START:
                offset_y = size[1] // 2
            elif self.y_axis == PositionOptions.END:
                offset_y = window_size[1] - size[1] // 2

        self.render_pos = (offset_x + position[0] - cam_pos[0],  offset_y + position[1] - cam_pos[1])

        return self.render_pos[0] - size[0] // 2, self.render_pos[1] - size[1] // 2

    def draw(self, window: pygame.Surface, cam: camera.Camera, get_gameobject_by_tag):
        """
        :param window: pygame window to draw to
        :param cam: camera
        :param get_gameobject_by_tag: function to get gameObject by Tag
        :return:
        """
        cam_pos = cam.position
        self.w, self.h = 0, 0
        # retion FLAW
        # TODO: flaw -> every object is rendered; try hiding not visible ones
        # cam_size = cam.view_size

        # min_x = self.position[0] - self.w // 2
        # max_x = self.position[0] + self.w // 2
        # min_y = self.position[1] - self.h // 2
        # max_y = self.position[1] + self.h // 2
        #
        # min_cam_x = cam_pos[0] - cam_size[0] // 2
        # max_cam_x = cam_pos[0] + cam_size[0] // 2
        # min_cam_y = cam_pos[1] - cam_size[1] // 2
        # max_cam_y = cam_pos[1] + cam_size[1] // 2

        # if min_cam_x <= max_x and min_x <= max_cam_x and min_cam_y <= max_y and min_y <= max_cam_y:
        #endregion

        if self.img is not None:
            img_pos = self.get_render_position(cam_pos, self.position, self.img.get_size(), window.get_size())
            window.blit(self.img, img_pos)

        if self.text is not None:
            text = self.text.get_text(window)
            txt_pos = self.get_render_position(cam_pos, self.position, text.get_size(), window.get_size())
            window.blit(text, txt_pos)

        if self.border is not None:
            start_pos = self.get_render_position(cam_pos, self.position, (self.w, self.h), window.get_size())
            rect = (start_pos[0] - self.border.padding,
                    start_pos[1] - self.border.padding,
                    self.w + self.border.padding,
                    self.h + self.border.padding)
            pygame.draw.rect(window, self.border.color, rect, width=self.border.thickness,
                             border_radius=self.border.radius)

        self.loop(get_gameobject_by_tag)

    def loop(self, get_gameobject_by_tag):
        pass



