import sys, pygame, math, random
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption("Brick Out!!!")
width, height = 850, 900  # 게임이 진행되는 실제 공간의 크기
w, h = 1200, 1000  # 전체 화면 크기
screen = pygame.display.set_mode((w, h))
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
BLUE2 = (70, 70, 255)  # 게임 백그라운드 컬러
BLACK = (0, 0, 0)  # 게임이 진행되는 실제 화면 컬러

heart = pygame.image.load("resources/images/heart.png")
blind = pygame.image.load("resources/images/blind.png")
blind2 = pygame.image.load("resources/images/blind2.png")
score_img = pygame.image.load("resources/images/score.png")
status = pygame.image.load("resources/images/status.png")
controls = pygame.image.load("resources/images/controls.png")
key_img = pygame.image.load("resources/images/keys.png")

pygame.mixer.music.load("resources/audio/ContactHigh.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.3)
hit1 = pygame.mixer.Sound("resources/audio/HitWood.wav")  # 블록 충돌음
hit2 = pygame.mixer.Sound("resources/audio/ChoppingLog.wav")  # 벽면 충돌음
hit3 = pygame.mixer.Sound("resources/audio/Pop.wav")  # 패들 충돌음
hit4 = pygame.mixer.Sound("resources/audio/Magic.wav")  # 특수 블록 충돌음

hit3.set_volume(0.5)

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
        self.dir = random.randint(-30, 30) + 270

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


# 게임화면에서 검은색 사각형 공간에 해당하는 객체들 생성
play_xpos, play_ypos = 50, 50  # 실제 게임이 플레이되는 공간의 topleft좌표
play_screen = Item(BLACK, Rect(play_xpos, play_ypos, width, height))
box_xpos, box_ypos = 950, 50  # 좌측 첫 번째 박스의 topleft 좌표 
box_width, box_height = 200, 200
box1 = Item(BLACK, Rect(box_xpos, box_ypos, box_width, box_height))
box2 = Item(BLACK, Rect(box_xpos, (box_ypos + box_height) + 70, box_width, box_height))
box3 = Item(BLACK, Rect(box_xpos, box_ypos + 2*(box_height + 70), box_width, box_height))
# 백그라운드 화면 하단 가림용 사각형 객체
bottom_screen = Item(BLUE2, Rect(0, play_screen.rect.bottom, w, h - play_screen.rect.bottom))

record = []
obstacles = []
timers = []  # 장애물 타이머


def collide_blocks(blocks, colors, score, ball):
    # 블록과 충돌
    prev_len = len(blocks)
    for block in blocks:
        if block.rect.colliderect(ball.rect):
            hit1.play()
            # 장애물 블록과 충돌
            collide_obstacles(block, colors)
            blocks.remove(block)

    if len(blocks) != prev_len:
        ball.dir = -ball.dir
        score += 10
    return blocks, score


def collide_obstacles(block, colors):
    if block.color in colors:
        obstacles.append(block)
        timers.append(1)
        hit4.play()
    return obstacles, timers


def draw_obstacles(blocks, colors):
    for block in blocks:
        if block.color in colors[1]:
            block.draw_ellipse()
        else:
            block.draw_rect()

    for obstacle in obstacles:
        if obstacle.color == colors[1][0]:
            imgRect = blind.get_rect(center=(play_screen.rect.centerx, play_screen.rect.centery))
            screen.blit(blind, imgRect)
        elif obstacle.color == colors[1][1]:
            imgRect = blind2.get_rect(center=(play_screen.rect.centerx, play_screen.rect.centery))
            screen.blit(blind2, imgRect)

    for i in range(len(timers)):
        timers[i] += 1
    for timer in timers:
        if timer >= 200:
            timers.remove(timer)
            obstacles.pop(0)


def collide_paddle(paddle, ball):
    if paddle.rect.colliderect(ball.rect):
        ball.dir = 90 + (paddle.rect.centerx - ball.rect.centerx) / paddle.rect.width * 80
        hit3.play()


def collide_wall(displayed_speed, ball):
    # 양 옆 벽면
    if ball.rect.left == play_screen.rect.left or ball.rect.right == play_screen.rect.right:
        ball.dir = 180 - ball.dir
        hit2.play()
    # 천장
    if ball.rect.top == play_ypos:
        ball.dir = -ball.dir
        if ball.speed < max_speed:
            ball.speed += 1
            displayed_speed += 1
        hit2.play()
    return displayed_speed


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


def check_keys(keys, paddle):
    if keys[0]:
        if paddle.rect.left > play_xpos:
            paddle.rect.centerx -= 10
    elif keys[1]:
        if paddle.rect.right < play_screen.rect.right:
            paddle.rect.centerx += 10


def main():
    blocks = []
    displayed_speed = 1
    paddle_startpos = (450, 870, 150, 20)
    paddle = Item(GRAY, Rect(paddle_startpos))
    ball_startpos = (450, 650, 20, 20)
    ball = Ball(GRAY, Rect(ball_startpos))

    score = 0
    keys = [False]*2
    lives = [heart]*3

    font1 = pygame.font.SysFont("Britannic", 80)
    font2 = pygame.font.SysFont("Britannic", 30)
    font3 = pygame.font.SysFont("Britannic", 23)
    font4 = pygame.font.SysFont("Britannic", 40)
    font5 = pygame.font.SysFont("Britannic", 50)

    clear = Text("Cleared!!", MINT, font1, (play_screen.rect.centerx, play_screen.rect.centery))
    over = Text("Game Over!!", PINK, font1, (play_screen.rect.centerx, play_screen.rect.centery))
    replay = Text("Replay [Press spacebar]", WHITE, font2, (play_screen.rect.centerx, play_screen.rect.centery + 140))
    tryagain = Text("Try Again!! [Press spacebar]", WHITE, font2, (play_screen.rect.centerx, play_screen.rect.centery + 100))
    congrats = Text("Wow! Congratulations!", PINK, font4, (play_screen.rect.centerx, play_screen.rect.centery + 70))
    pause_text = Text("Pause", YELLOW, font5, (play_screen.rect.centerx, play_screen.rect.centery))

    # 0번째 원소 = 일반 블럭 컬러, 1번째 원소 = 특수 블럭 컬러
    colors = [(RED, RED2, YELLOW, GREEN, NAVY, NAVY2, BLUE, PURPLE), (OLIVE, SALMON)]
    block_width, block_height = 100, 30
    block_xpos, block_ypos = 100, 100  # 좌측 상단 첫 번째 블록의 topleft 좌표
    num_blocks = 6  # 한 줄에 깔리는 블록 수
    for ypos, color in enumerate(colors[0], start=0):
        for xpos in range(0, num_blocks):
            blocks.append(Item(color, Rect(xpos*(block_width + ((width-play_xpos*2)-(num_blocks*block_width))//(num_blocks-1)) + block_xpos,
            ypos*(block_height+30) + block_ypos, block_width, block_height)))

    # 특수 블록을 랜덤한 위치에 배치
    for color in colors[1]:
        num = random.randint(0, 5*len(colors[0])-1)
        blocks[num].color = color

    pause = False
    running = True
    win = False
    while running:
        screen.fill(BLUE2)
        play_screen.draw_rect()
        box1.draw_rect()
        box2.draw_rect()
        box3.draw_rect()
        screen.blit(score_img, (900, 20))
        screen.blit(status, (900, 290))
        screen.blit(controls, (900, 550))
        score_text = Text(str(score), WHITE, font5, (box1.rect.centerx, box1.rect.centery))
        screen.blit(score_text.textrender, score_text.textrect)
        speed_text = Text("Speed : " + str(displayed_speed), YELLOW, font3, (box2.rect.centerx, box2.rect.centery + 40))
        screen.blit(speed_text.textrender, speed_text.textrect)
        imgRect = key_img.get_rect(center=(box3.rect.centerx, box3.rect.centery))
        screen.blit(key_img, imgRect)
        for xpos, life in enumerate(lives, start=1):
            imgRect = life.get_rect(center=(box2.rect.left + 50*xpos, box2.rect.centery))
            screen.blit(life, imgRect)

        displayed_speed, pause = check_event(keys, ball, displayed_speed, pause)

        if not pause:
            check_keys(keys, paddle)

            if lives:
                if ball.rect.centery < play_screen.rect.bottom + 400:
                    ball.move()                
                    if ball.rect.left < play_screen.rect.left:
                        ball.rect.left = play_screen.rect.left
                    elif ball.rect.right > play_screen.rect.right:
                        ball.rect.right = play_screen.rect.right
                    elif ball.rect.top < play_screen.rect.top:
                        ball.rect.top = play_screen.rect.top

                    if len(blocks) == 0:
                        win = True
                        running = False
                else:
                    lives.pop()
                    ball.rect = Rect(ball_startpos)
                    ball.dir = random.randint(-30, 30) + 270
                    ball.speed = min_speed
                    displayed_speed = 1
                    ball.move()
            else:
                running = False

            blocks, score = collide_blocks(blocks, colors[1], score, ball)
            displayed_speed = collide_wall(displayed_speed, ball)
            collide_paddle(paddle, ball)

            ball.draw_ellipse()
            bottom_screen.draw_rect()
            paddle.draw_rect()
            draw_obstacles(blocks, colors)

        else:
            screen.blit(pause_text.textrender, pause_text.textrect)

        pygame.display.flip()
        fpsClock.tick(FPS)

    play_screen.draw_rect()
    record.append(score)
    if win:
        screen.blit(clear.textrender, clear.textrect)
        screen.blit(replay.textrender, replay.textrect)
        screen.blit(congrats.textrender, congrats.textrect)
    else:
        screen.blit(over.textrender, over.textrect)
        screen.blit(tryagain.textrender, tryagain.textrect)
        current_score = Text("Current Score : " + str(score), MINT, font3, (play_screen.rect.centerx, play_screen.rect.centery + 180))
        best_score = Text("Best Score : " + str(max(record)), YELLOW, font3, (play_screen.rect.centerx, play_screen.rect.centery + 220))
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
            timers = []
            obstacles = []
            main()