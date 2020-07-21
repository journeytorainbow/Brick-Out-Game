import pygame
from pygame.locals import *
from objects import Text, max_speed, min_speed
from fonts import *
from colors import *


def check_event(keys, ball, displayed_speed, pause):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                keys[0] = True
            elif event.key == K_RIGHT:
                keys[1] = True
            if event.key == K_f:
                if ball.speed < max_speed - 1:
                    ball.speed += 1
                    displayed_speed += 1
            elif event.key == K_d:
                if ball.speed > min_speed:
                    ball.speed -= 1
                    displayed_speed -= 1
            if event.key == K_p:
                pause = True
            elif event.key == K_u:
                pause = False
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                keys[0] = False
            elif event.key == K_RIGHT:
                keys[1] = False
    return displayed_speed, pause


def check_keys(play_screen, play_xpos, keys, paddle):
    if keys[0]:
        if paddle.rectangle.left > play_xpos:
            paddle.rectangle.centerx -= 10
    elif keys[1]:
        if paddle.rectangle.right < play_screen.rectangle.right:
            paddle.rectangle.centerx += 10


def check_ball_pos(play_screen, ball):
    if ball.rectangle.left < play_screen.rectangle.left:
        ball.rectangle.left = play_screen.rectangle.left
    elif ball.rectangle.right > play_screen.rectangle.right:
        ball.rectangle.right = play_screen.rectangle.right
    elif ball.rectangle.top < play_screen.rectangle.top:
        ball.rectangle.top = play_screen.rectangle.top


def check_block_nums(blocks, win, running):
    if len(blocks) == 0:
        win = True
        running = False
    return win, running


def check_win(screen, play_screen, win, score, record):
    clear = Text("Cleared!!", MINT, font1, (play_screen.rectangle.centerx, play_screen.rectangle.centery))
    over = Text("Game Over!!", PINK, font1, (play_screen.rectangle.centerx, play_screen.rectangle.centery))
    replay = Text("Replay [Press spacebar]", WHITE, font2, (play_screen.rectangle.centerx, play_screen.rectangle.centery + 140))
    tryagain = Text("Try Again!! [Press spacebar]", WHITE, font2, (play_screen.rectangle.centerx, play_screen.rectangle.centery + 100))
    congrats = Text("Wow! Congratulations!", PINK, font4, (play_screen.rectangle.centerx, play_screen.rectangle.centery + 70))
    pause_text = Text("Pause", YELLOW, font5, (play_screen.rectangle.centerx, play_screen.rectangle.centery))

    if win:
        screen.blit(clear.textrender, clear.textrect)
        screen.blit(replay.textrender, replay.textrect)
        screen.blit(congrats.textrender, congrats.textrect)
    else:
        screen.blit(over.textrender, over.textrect)
        screen.blit(tryagain.textrender, tryagain.textrect)
        current_score = Text("Current Score : " + str(score), MINT, font3, (play_screen.rectangle.centerx, play_screen.rectangle.centery + 180))
        best_score = Text("Best Score : " + str(max(record)), YELLOW, font3, (play_screen.rectangle.centerx, play_screen.rectangle.centery + 220))
        screen.blit(best_score.textrender, best_score.textrect)
        screen.blit(current_score.textrender, current_score.textrect)