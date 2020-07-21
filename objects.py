import pygame, random, math


min_speed = 10
max_speed = 14

class Item:
    def __init__(self, canvas, color, rectangle):
        self.canvas = canvas
        self.color = color
        self.rectangle = rectangle

    def draw_rect(self):
        pygame.draw.rect(self.canvas, self.color, self.rectangle)

    def draw_ellipse(self):
        pygame.draw.ellipse(self.canvas, self.color, self.rectangle)


class Ball(Item):
    def __init__(self, canvas, color, rectangle):
        super().__init__(canvas, color, rectangle)
        self.speed = min_speed
        self.dir = random.randint(-30, 30) + 270

    def move(self):
        self.rectangle.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rectangle.centery -= math.sin(math.radians(self.dir)) * self.speed

class Text():
    def __init__(self, string, color, font, pos):
        self.string = string
        self.color = color
        self.font = font
        self.pos = pos
        self.textrender = self.font.render(self.string, True, self.color)
        self.textrect = self.textrender.get_rect(center=self.pos)

