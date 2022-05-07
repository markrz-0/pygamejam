import pygame
import threading
from engine import colors, colliders, helpers, activity, border, text, gameObject


class PlayButton(gameObject.GameObject):
    def __init__(self):
        super().__init__(
            position=(0, 0),
            collider=colliders.Collider.RECT,
            text=text.Text('   PLAY   ', 'monospace', font_percent_size=0.1),
            x_axis=gameObject.PositionOptions.CENTER,
            y_axis=gameObject.PositionOptions.CENTER,
            border=border.Border(colors.WHITE, thickness=5, radius=5, padding=5)
        )
        self.is_transitioning = False

    def on_click(self):
        if not self.is_transitioning:
            self.is_transitioning = True
            threading.Thread(target=helpers.smooth_code, args=(self.silence_music, self.start_loading)).start()

    def silence_music(self, i):
        pygame.mixer.music.set_volume(1 - i/20)
        faded_color = (int(255 * (1-i/20)), int(255 * (1-i/20)), int(255 * (1-i/20)))
        self.text = text.Text('   PLAY   ', 'monospace', font_percent_size=0.1, font_color=faded_color)
        self.border = border.Border(faded_color, thickness=5, radius=5, padding=5)


    @classmethod
    def start_loading(cls):
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        helpers.change_activity('loading')

class MenuText(gameObject.GameObject):
    def __init__(self):
        super().__init__(
            position=(0, 20),
            collider=colliders.Collider.RECT,
            text=text.Text('Menu', 'monospace', font_percent_size=0.1),
            x_axis=gameObject.PositionOptions.CENTER,
            y_axis=gameObject.PositionOptions.START
        )

class MenuActivity(activity.BaseActivity):
    def __init__(self, window_size):
        super().__init__(bg_path='_client/img/bg.png', window_size=window_size)

    def start(self, session):
        self.gameObjects.clear()

        pygame.mixer.music.load('_client/audio/ambient.wav')
        pygame.mixer.music.play(-1, fade_ms=500)

        self.add(
            MenuText(),
            PlayButton(),
        )




