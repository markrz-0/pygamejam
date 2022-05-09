import pygame
from engine import game
from _client import loading_activity, menu_activity, galaxy_activity, outcome_activity


class Client(game.Game):
    def __init__(self):
        super().__init__(resizable=True)

        pygame.display.set_caption("Xstellar")

        self.fps_target = 30

        self.activities = {
            'loading': loading_activity.LoadingActivity(window_size=self.window.get_size()),
            'menu': menu_activity.MenuActivity(window_size=self.window.get_size()),
            'galaxy': galaxy_activity.GalaxyActivity(window_size=self.window.get_size()),
            'result': outcome_activity.OutcomeActivity(window_size=self.window.get_size())
        }
        self.current_activity = self.activities['menu']
        self.current_activity.start(self.session)


if __name__ == '__main__':
    client = Client()
    client.run_loop()