import sys, pygame
from pygame.locals import *


def replay_game(func):
    global timers, obstacles
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                timers = []
                obstacles = []
                func()