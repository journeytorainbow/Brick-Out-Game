import pygame
from objects import max_speed


pygame.mixer.init()

hit1 = pygame.mixer.Sound("resources/audio/HitWood.wav")  # 블록 충돌음
hit2 = pygame.mixer.Sound("resources/audio/ChoppingLog.wav")  # 벽면 충돌음
hit3 = pygame.mixer.Sound("resources/audio/Pop.wav")  # 패들 충돌음
hit4 = pygame.mixer.Sound("resources/audio/Magic.wav")  # 특수 블록 충돌음

hit3.set_volume(0.5)

def collide_blocks(blocks, colors, score, ball, obstacles, timers):
    # 블록과 충돌
    prev_len = len(blocks)
    for block in blocks:
        if block.rectangle.colliderect(ball.rectangle):
            hit1.play()
            # 장애물 블록과 충돌
            if block.color in colors:
                obstacles.append(block)
                timers.append(1)
                hit4.play()
            blocks.remove(block)

    if len(blocks) != prev_len:
        ball.dir = -ball.dir
        score += 10
    return score


def collide_paddle(paddle, ball):
    if paddle.rectangle.colliderect(ball.rectangle):
        ball.dir = 90 + (paddle.rectangle.centerx - ball.rectangle.centerx) / paddle.rectangle.width * 80
        hit3.play()


def collide_wall(play_screen, play_xpos, play_ypos, displayed_speed, ball):
    # 양 옆 벽면
    if ball.rectangle.left == play_screen.rectangle.left or ball.rectangle.right == play_screen.rectangle.right:
        ball.dir = 180 - ball.dir
        hit2.play()
    # 천장
    if ball.rectangle.top == play_ypos:
        ball.dir = -ball.dir
        if ball.speed < max_speed:
            ball.speed += 1
            displayed_speed += 1
        hit2.play()
    return displayed_speed