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
RED2 = (255, 102, 102)
YELLOW = (255, 255, 102)
GREEN = (153, 255, 153)
BLUE = (51, 51, 255)
NAVY = (51, 51, 102)
NAVY2 = (000, 000, 102)
PURPLE = (102, 51, 255)
WHITE = (255, 255, 255)
OLIVE = (102, 102, 000)
SALMON = (204, 153, 153)

heart = pygame.image.load("resources/images/heart.png")
blind = pygame.image.load("resources/images/blind.png")
blind2 = pygame.image.load("resources/images/blind2.png")

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
obstacles = []
timers = [] # 장애물 타이머

def collide(colors):
    global blocks, score, obstacles, timers

    # 블록과 충돌
    prev_len = len(blocks)
    for block in blocks:
        if block.rect.colliderect(ball.rect):
            # 장애물 블록과 충돌
            if block.color in colors:
                obstacles.append(block)
                timers.append(1)
            blocks.remove(block)
 
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
    lives = [heart]*3

    font1 = pygame.font.SysFont("Impact", 80)
    font2 = pygame.font.SysFont("Impact", 30)
    font3 = pygame.font.SysFont("Impact", 23)
    font4 =  pygame.font.SysFont("Impact", 40)

    clear = Text("Cleared!!", MINT, font1, (width/2, height/2))
    over = Text("Game Over!!", PINK, font1, (width/2, height/2))
    replay = Text("Replay [Press spacebar]", WHITE, font2, (width/2, height/2 + 140))
    tryagain = Text("Try Again!! [Press spacebar]", WHITE, font2, (width/2, height/2 + 100))
    congrats = Text("Wow! Congratulations!", PINK, font4, (width/2, height/2 + 70))

    # 0번째 원소 = 일반 블럭 컬러, 1번째 원소 = 특수 블럭 컬러
    colors = [(RED, RED2, YELLOW, GREEN, NAVY, NAVY2, BLUE, PURPLE), (OLIVE, SALMON)]
    for ypos, color in enumerate(colors[0], start = 0):
        # 한줄에 블록 다섯개로 고정
        for xpos in range(0, 5):
            blocks.append(Item(color, Rect(xpos*130, ypos*60 + 30, 80, 30)))

    # 특수 블록을 랜덤한 위치에 배치
    for color in colors[1]:
        num = random.randint(0, 5*len(colors[0])-1)
        blocks[num].color = color

    running = True
    win = False
    while running:
        screen.fill(0)
        score_text = Text("score: " + str(score), WHITE, font2, (80, height - 30))
        screen.blit(score_text.textrender, score_text.textrect)
        for xpos, life in enumerate(lives, start = 1):
            screen.blit(life, (width - life.get_width() * xpos, height - life.get_height()))

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

        if lives:
            if ball.rect.centery < 1000:
                ball.move()
                if len(blocks) == 0:
                    win = True
                    running = False
            else:
                lives.pop()
                ball.rect = Rect(300, 400, 20, 20)
                ball.dir = random.randint(-45, 45) + 270
                ball.speed = min_speed
                ball.move()
        else:
            running = False

        collide(colors[1])
        ball.draw_ellipse()
        paddle.draw_rect()
        for block in blocks:
            if block.color in colors[1]:
                block.draw_ellipse()
            else:
                block.draw_rect()

        for obstacle in obstacles:
            if obstacle.color == colors[1][0]:
                screen.blit(blind, (1/2*(width - blind.get_width()), 1/2*(height - blind.get_height())))
            elif obstacle.color == colors[1][1]:
                screen.blit(blind2, (1/2*(width - blind2.get_width()), 1/2*(height - blind2.get_height())))
        
        # 일정 시간이 지나면 장애물 제거
        for i in range(len(timers)):
            timers[i] += 1
        for timer in timers:
            if timer >= 200:
                timers.remove(timer)
                obstacles.pop(0)

        pygame.display.flip()
        fpsClock.tick(FPS)

    screen.fill(0)
    record.append(score)
    if win:
        screen.blit(clear.textrender, clear.textrect)
        screen.blit(replay.textrender, replay.textrect)
        screen.blit(congrats.textrender, congrats.textrect)
    else:
        screen.blit(over.textrender, over.textrect)
        screen.blit(tryagain.textrender, tryagain.textrect)
        current_score = Text("Current Score : " + str(score), MINT, font3, (width/2, height/2 + 180))
        best_score = Text("Best Score : " + str(max(record)), YELLOW, font3, (width/2, height/2 + 220))
        screen.blit(best_score.textrender, best_score.textrect)
        screen.blit(current_score.textrender, current_score.textrect)
    
    pygame.display.flip()

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
            timers = []
            obstacles = []
            main()