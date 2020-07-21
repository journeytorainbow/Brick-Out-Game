import pygame, random
from colors import *
from objects import *
from pygame.locals import *


blind = pygame.image.load("resources/images/blind.png")
blind2 = pygame.image.load("resources/images/blind2.png")

# 0번째 원소 = 일반 블럭 컬러, 1번째 원소 = 특수 블럭 컬러
block_colors = [(RED, RED2, YELLOW, GREEN, NAVY, NAVY2, BLUE, PURPLE), (OLIVE, SALMON)]

def draw_obstacles(screen, play_screen, blocks, obstacles, timers):
    for block in blocks:
        if block.color in block_colors[1]:
            block.draw_ellipse()
        else:
            block.draw_rect()

    for obstacle in obstacles:
        if obstacle.color == block_colors[1][0]:
            imgRect = blind.get_rect(center=(play_screen.rectangle.centerx, play_screen.rectangle.centery))
            screen.blit(blind, imgRect)
        elif obstacle.color == block_colors[1][1]:
            imgRect = blind2.get_rect(center=(play_screen.rectangle.centerx, play_screen.rectangle.centery))
            screen.blit(blind2, imgRect)

    for i in range(len(timers)):
        timers[i] += 1
    for timer in timers:
        if timer >= 200:
            timers.remove(timer)
            obstacles.pop(0)

def place_blocks(screen, width, play_xpos, blocks):
    block_width, block_height = 100, 30
    block_xpos, block_ypos = 100, 100  # 좌측 상단 첫 번째 블록의 topleft 좌표
    num_blocks = 6  # 한 줄에 깔리는 블록 수
    for ypos, color in enumerate(block_colors[0], start=0):
        for xpos in range(0, num_blocks):
            blocks.append(Item(screen, color, Rect(xpos*(block_width + ((width-play_xpos*2)-(num_blocks*block_width))//(num_blocks-1)) + block_xpos, ypos*(block_height+30) + block_ypos, block_width, block_height)))

    # 특수 블록을 랜덤한 위치에 배치
    for color in block_colors[1]:
        num = random.randint(0, 5*len(block_colors[0])-1)
        blocks[num].color = color