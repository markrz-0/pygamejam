import pygame
import sys
from engine import activity
from engine.helpers import Events

class Game:
    def __init__(self, size=(600, 400), resizable=False):
        pygame.init()
        if resizable:
            pygame.display.set_mode(size, pygame.RESIZABLE)
        else:
            pygame.display.set_mode(size)

        self.window = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps_target = 60
        self.deltatime = 0
        self.current_activity = activity.BaseActivity(window_size=size)
        self.activities = {}

        self.session = {}

    def fps(self, target_fps):
        self.fps_target = target_fps

    @classmethod
    def on_exit(cls):
        pygame.quit()
        sys.exit(0)

    def on_mouse_down(self, event: pygame.event.Event):
        pass

    def on_mouse_up(self, event: pygame.event.Event):
        pass

    def on_mouse_move(self, event: pygame.event.Event):
        pass

    def on_key_down(self, event: pygame.event.Event):
        pass

    def on_key_up(self, event: pygame.event.Event):
        pass

    def on_resize(self, event: pygame.event.Event):
        self.current_activity.resize(self.window.get_size())

    def on_user_event(self, event: pygame.event.Event):
        if event.val == Events.CHANGE_ACTIVITY:
            self.current_activity.stop()
            self.current_activity = self.activities[event.name]
            self.current_activity.start(self.session)
        elif event.val == Events.ADD_SESSION_DATA:
            self.session[event.key] = event.vl

    def on_other_event(self, event: pygame.event.Event):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.on_exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_down(event)
                self.current_activity.on_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_up(event)
                self.current_activity.on_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.on_mouse_move(event)
                self.current_activity.on_mouse_move(event)
            elif event.type == pygame.KEYDOWN:
                self.on_key_down(event)
                self.current_activity.on_key_down(event)
            elif event.type == pygame.KEYUP:
                self.on_key_down(event)
                self.current_activity.on_key_up(event)
            elif event.type == pygame.WINDOWRESIZED:
                self.on_resize(event)
            elif event.type == pygame.USEREVENT:
                self.on_user_event(event)
            else:
                self.on_other_event(event)
                self.current_activity.on_other_event(event)

    def pre_draw(self):
        pass

    def post_draw(self):
        pass

    def run_loop(self):
        while True:
            self.deltatime = self.clock.tick(self.fps_target) # in milliseconds.
            self.events()
            self.pre_draw()
            self.current_activity.update(self, self.session)
            self.post_draw()
            pygame.display.update()
