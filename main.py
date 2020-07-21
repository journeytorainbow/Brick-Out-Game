import sys, pygame, random
from pygame.locals import *
from colors import *
from objects import *
from collision import *
from block_placement import *
from ball_reset import *
from check import *
from fonts import *
from display_draw import *
from game_restart import *


# pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption("Brick Out!!!")
width, height = 850, 900  # 게임이 진행되는 실제 공간의 크기
w, h = 1200, 1000  # 전체 화면 크기
screen = pygame.display.set_mode((w, h))
FPS = 60
fpsClock = pygame.time.Clock()

pygame.mixer.music.load("resources/audio/ContactHigh.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.3)

play_xpos, play_ypos = 50, 50  # 실제 게임이 플레이되는 공간의 topleft좌표
play_screen = Item(screen, BLACK, Rect(play_xpos, play_ypos, width, height))
# 백그라운드 화면 하단 가림용 사각형 객체
bottom_screen = Item(screen, BLUE2, Rect(0, play_screen.rectangle.bottom, w, h - play_screen.rectangle.bottom))

record = []


def main():
    blocks = []
    obstacles = []
    timers = []
    displayed_speed = 1
    paddle_startpos = (450, 870, 150, 20)
    paddle = Item(screen, GRAY, Rect(paddle_startpos))
    ball_startpos = (450, 650, 20, 20)
    ball = Ball(screen, GRAY, Rect(ball_startpos))

    score = 0
    keys = [False]*2
    lives = [heart]*3

    place_blocks(screen, width, play_xpos, blocks)

    pause = False
    running = True
    win = False
    while running:
        draw_display(screen, play_screen, w, h, score, displayed_speed, lives)
        displayed_speed, pause = check_event(keys, ball, displayed_speed, pause)

        if not pause:
            check_keys(play_screen, play_xpos, keys, paddle)

            if lives:
                if ball.rectangle.centery < play_screen.rectangle.bottom + 400:
                    ball.move()                
                    check_ball_pos(play_screen, ball)
                    win, running = check_block_nums(blocks, win, running)
                else:
                    lives.pop()
                    displayed_speed = reset_ball(ball, ball_startpos, displayed_speed)
                    ball.move()
            else:
                running = False

            score = collide_blocks(blocks, block_colors[1], score, ball, obstacles, timers)
            displayed_speed = collide_wall(play_screen, play_xpos, play_ypos, displayed_speed, ball)
            collide_paddle(paddle, ball)

            ball.draw_ellipse()
            bottom_screen.draw_rect()
            paddle.draw_rect()
            draw_obstacles(screen, play_screen, blocks, obstacles, timers)

        else:
            screen.blit(pause_text.textrender, pause_text.textrect)

        pygame.display.flip()
        fpsClock.tick(FPS)

    play_screen.draw_rect()
    record.append(score)
    check_win(screen, play_screen, win, score, record)

    pygame.display.flip()

if __name__ == '__main__':
    func = main
    main()
    replay_game(func)