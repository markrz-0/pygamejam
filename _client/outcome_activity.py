from engine import colors, colliders, helpers, activity, border, text, gameObject


class ReplayButton(gameObject.GameObject):
    def __init__(self):
        super().__init__(
            position=(0, 20),
            collider=colliders.Collider.RECT,
            text=text.Text('  PLAY AGAIN  ', 'monospace', font_percent_size=0.1),
            x_axis=gameObject.PositionOptions.CENTER,
            y_axis=gameObject.PositionOptions.CENTER,
            border=border.Border(colors.WHITE, thickness=5, radius=5, padding=5)
        )
        self.is_transitioning = False

    def on_click(self):
        helpers.change_activity('menu')

class ResultText(gameObject.GameObject):
    def __init__(self, txt):
        super().__init__(
            position=(0, 40),
            collider=colliders.Collider.RECT,
            text=text.Text(txt, 'monospace', font_percent_size=0.1),
            x_axis=gameObject.PositionOptions.CENTER,
            y_axis=gameObject.PositionOptions.START
        )

class OutcomeActivity(activity.BaseActivity):
    def __init__(self, window_size):
        super().__init__(bg_path='_client/img/bg.png', window_size=window_size)

    def start(self, session):
        self.gameObjects.clear()

        result = session['result']

        self.add(
            ResultText(result),
            ReplayButton(),
        )




