import pygame
from pygame.locals import *
from objects import *
from colors import *
from fonts import *


heart = pygame.image.load("resources/images/heart.png")
score_img = pygame.image.load("resources/images/score.png")
status = pygame.image.load("resources/images/status.png")
controls = pygame.image.load("resources/images/controls.png")
key_img = pygame.image.load("resources/images/keys.png")


def draw_display(screen, play_screen, w, h, score, displayed_speed, lives):
    box_xpos, box_ypos = 950, 50  # 좌측 첫 번째 박스의 topleft 좌표 
    box_width, box_height = 200, 200
    box1 = Item(screen, BLACK, Rect(box_xpos, box_ypos, box_width, box_height))
    box2 = Item(screen, BLACK, Rect(box_xpos, (box_ypos + box_height) + 70, box_width, box_height))
    box3 = Item(screen, BLACK, Rect(box_xpos, box_ypos + 2*(box_height + 70), box_width, box_height))

    screen.fill(BLUE2)
    play_screen.draw_rect()
    box1.draw_rect()
    box2.draw_rect()
    box3.draw_rect()
    screen.blit(score_img, (900, 20))
    screen.blit(status, (900, 290))
    screen.blit(controls, (900, 550))
    score_text = Text(str(score), WHITE, font5, (box1.rectangle.centerx, box1.rectangle.centery))
    screen.blit(score_text.textrender, score_text.textrect)
    speed_text = Text("Speed : " + str(displayed_speed), YELLOW, font3, (box2.rectangle.centerx, box2.rectangle.centery + 40))
    screen.blit(speed_text.textrender, speed_text.textrect)
    imgRect = key_img.get_rect(center=(box3.rectangle.centerx, box3.rectangle.centery))
    screen.blit(key_img, imgRect)
    for xpos, life in enumerate(lives, start=1):
        imgRect = life.get_rect(center=(box2.rectangle.left + 50*xpos, box2.rectangle.centery))
        screen.blit(life, imgRect)