from constants import Color
from objects.balls import LinearMovingBall
from objects.text import Text
from scenes.base import Scene
from objects.button import Btn


class MainScene(Scene):
    MAX_COLLISIONS = 15

    def create_objects(self):
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.balls = [LinearMovingBall(self.game) for _ in range(5)]
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, 'Меню', self.back_to_menu)
        self.objects = self.balls + [self.text_count, self.button_back]

    def additional_logic(self):
        self.process_ball_collisions()
        self.text_count.update_text(
            'Коллизии со стенами: {}/{}'.format(
                self.game.wall_collision_count,
                self.MAX_COLLISIONS
            )
        )
        if self.game.wall_collision_count >= self.MAX_COLLISIONS:
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)

    def process_ball_collisions(self):
        for i in range(len(self.balls) - 1):
            for j in range(i + 1, len(self.balls)):
                if self.balls[i].collides_with(self.balls[j]):
                    print('Мячи {} и {} столкнулись'.format(i, j))
                    self.balls[i].collision(self.balls[j])

    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)
