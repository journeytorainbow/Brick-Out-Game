import sys, pygame, math, random
from pygame.locals import *

pygame.init()
width, height = 600, 800
screen = pygame.display.set_mode((width, height))
FPS = 60
fpsClock = pygame.time.Clock()

GRAY = (204, 204, 204)
MINT = (51, 255, 255)
PINK = (255, 000, 204)
RED = (255, 51, 51)
YELLOW = (255, 255, 102)
GREEN = (153, 255, 153)
BLUE = (51, 51, 255)
PURPLE = (102, 51, 255)
WHITE = (255, 255, 255)

max_speed = 14
min_speed = 10

class Item:
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect

    def draw_rect(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def draw_ellipse(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

class Ball(Item):
    def __init__(self, color, rect):
        super().__init__(color, rect)
        self.speed = min_speed
        self.dir = random.randint(-45, 45) + 270
    
    def move(self):
        self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed

class Text():
    def __init__(self, string, color, font, pos):
        self.string = string
        self.color = color
        self.font = font
        self.pos = pos
        self.textrender = self.font.render(self.string, True, self.color)
        self.textrect = self.textrender.get_rect(center=self.pos)

blocks = []
paddle = Item(GRAY, Rect(300, 700, 150, 20))
ball = Ball(GRAY, Rect(300, 400, 20, 20))
score = 0
record = []

def collide():
    global blocks, score

    if ball.rect.centery < 1000:
        ball.move()

    # 블록과 충돌
    prev_len = len(blocks)
    blocks = [block for block in blocks if not block.rect.colliderect(ball.rect)]
    if len(blocks) != prev_len:
        ball.dir = -ball.dir
        score += 10

    # 패들과 충돌
    if paddle.rect.colliderect(ball.rect):
        ball.dir = 90 + (paddle.rect.centerx - ball.rect.centerx) / paddle.rect.width * 80
    
    # 양 옆 벽면과 충돌
    if ball.rect.centerx < 0 or ball.rect.centerx > width:
        ball.dir = 180 - ball.dir
    # 천장과 충돌
    if ball.rect.centery < 0:
        ball.dir = -ball.dir
        if ball.speed < max_speed:
            ball.speed += 1

def main():
    keys = [False]*2
    
    font1 = pygame.font.SysFont("Impact", 80)
    font2 = pygame.font.SysFont("Impact", 30)

    clear = Text("Cleared!!", MINT, font1, (width/2, height/2))
    over = Text("Game Over!!", PINK, font1, (width/2, height/2))
    replay = Text("Replay [Press spacebar]", WHITE, font2, (width/2, height/2 + 100))
    tryagain = Text("Try Again!! [Press spacebar]", WHITE, font2, (width/2, height/2 + 100))

    colors = [RED, YELLOW, GREEN, BLUE, PURPLE]
    for ypos, color in enumerate(colors, start = 0):
        for xpos in range(0, 5):
            blocks.append(Item(color, Rect(xpos*130, ypos*60 + 30, 80, 30)))

    running = True
    while running:
        screen.fill(0)
        score_text = Text("score: " + str(score), WHITE, font2, (80, height - 30))
        screen.blit(score_text.textrender, score_text.textrect)

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
                elif event.key == K_d:
                    if ball.speed > min_speed:
                        ball.speed -= 1
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    keys[0] = False
                elif event.key == K_RIGHT:
                    keys[1] = False
        if keys[0]:
            if paddle.rect.centerx > paddle.rect.width/2:
                paddle.rect.centerx -= 10
        elif keys[1]:
            if paddle.rect.centerx < width - paddle.rect.width/2:
                paddle.rect.centerx += 10

        collide()
        ball.draw_ellipse()
        paddle.draw_rect()
        for block in blocks:
            block.draw_rect()
    
        if len(blocks) == 0:
            screen.fill(0)
            screen.blit(clear.textrender, clear.textrect)
            screen.blit(replay.textrender, replay.textrect)
            running = False
        elif ball.rect.centery >= height + ball.rect.height/2:
            screen.fill(0)
            screen.blit(over.textrender, over.textrect)
            screen.blit(tryagain.textrender, tryagain.textrect)
            running = False

        pygame.display.flip()
        fpsClock.tick(FPS)

main()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            blocks = []
            paddle = Item(GRAY, Rect(300, 700, 150, 20))
            ball = Ball(GRAY, Rect(300, 400, 20, 20))
            score = 0
            main()