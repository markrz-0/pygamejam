import pygame
from engine import camera


class BaseActivity:
    def __init__(self, bg_path = None, bg_color=(0, 0, 0), window_size=None):
        """
        bg image is superior to bg color
        :param bg_path:
        :param bg_color:
        """
        self.gameObjects = []
        self.camera = camera.Camera(view_size=window_size)

        self.bg_color = bg_color

        if bg_path is not None:
            self.bg_img = pygame.image.load(bg_path)
        else:
            self.bg_img = None

        self.session = {}

    def add(self, *args):
        for arg in args:
            self.gameObjects.append(arg)

    def resize(self, size):
        self.camera.view_size = size

    def on_mouse_down(self, event: pygame.event.Event):
        pass

    def on_mouse_up(self, event: pygame.event.Event):
        click_pos = event.pos
        for gameObject in self.gameObjects:
            if gameObject.is_clicked(click_pos):
                gameObject.on_click()
                break

    def on_mouse_move(self, event: pygame.event.Event):
        pass

    def on_key_down(self, event: pygame.event.Event):
        pass

    def on_key_up(self, event: pygame.event.Event):
        pass

    def on_other_event(self, event: pygame.event.Event):
        pass

    def get_gameobject_by_tag(self, tag):
        for gameObject in self.gameObjects:
            if gameObject.tag == tag:
                return gameObject

        return None

    def get_all_gameobjects_with_tag(self, tag):
        ret = []
        for gameObject in self.gameObjects:
            if gameObject.tag == tag:
                ret.append(gameObject)

        return ret

    def start(self, session):
        pass

    def stop(self):
        pass

    def pre_update(self, g, session: dict):
        pass

    def post_update(self, g, session: dict):
        pass

    def update(self, g, session: dict):
        """
        :param g: _client.engine.Game object
        :param session: dict with session values
        :return:
        """

        self.pre_update(g, session)

        self.session = session

        if self.bg_img is not None:
            # img_w, img_h = self.bg_img.get_size()
            # win_w, win_h = g.window.get_size()
            # scaled_by =
            # if win_w < win_h:

            scaled = pygame.transform.scale(self.bg_img, g.window.get_size())
            g.window.blit(scaled, (0, 0))
        else:
            g.window.fill(self.bg_color)

        self.camera.move(g.deltatime)

        for gameObject in self.gameObjects:
            gameObject.deltatime = g.deltatime
            gameObject.draw(g.window, self.camera, self.get_gameobject_by_tag)

        self.post_update(g, session)