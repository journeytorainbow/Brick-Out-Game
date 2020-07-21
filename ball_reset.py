import random
from objects import min_speed
from pygame.locals import *


def reset_ball(ball, ball_startpos, displayed_speed):
    ball.rectangle = Rect(ball_startpos)
    ball.dir = random.randint(-30, 30) + 270
    ball.speed = min_speed
    displayed_speed = 1
    return displayed_speed