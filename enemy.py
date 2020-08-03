import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    """docstring for SmallEnemy"""
    energy = 1

    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()

        self.image = pygame.image.load('images/enemy1.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),
            pygame.image.load('images/enemy1_down4.png').convert_alpha()
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.reset()
        self.energy = SmallEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        # 同时需要在各个类的reset（）成员函数中将active标志位置为真，以保证各个类型的飞机在重置之后是激活的状态：
        self.active = True
        self.energy = SmallEnemy.energy


class MidEnemy(pygame.sprite.Sprite):
    """docstring for MidEnemy"""

    energy = 8
    # 注意这里之所以将energy初始化为类的全局变量以及类对象的成员变量两种形式，
    # 是因为在接下来绘制血槽的过程中，需要计算当前血量和总血量的比值，
    # 全局energy用以保存总血量（定值），类对象的成员变量energy（随着被击中的次数而递减）表示当前血量

    def __init__(self, bg_size):
        super(MidEnemy, self).__init__()

        self.image = pygame.image.load('images/enemy2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy2_down1.png').convert_alpha(),
            pygame.image.load('images/enemy2_down2.png').convert_alpha(),
            pygame.image.load('images/enemy2_down3.png').convert_alpha(),
            pygame.image.load('images/enemy2_down4.png').convert_alpha()
            ])
        self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()
        self.energy = MidEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)
        self.active = True
        self.energy = MidEnemy.energy


class BigEnemy(pygame.sprite.Sprite):
    """docstring for BigEnemy"""
    energy = 20

    def __init__(self, bg_size):
        super(BigEnemy, self).__init__()

        self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
        self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy3_down1.png').convert_alpha(),
            pygame.image.load('images/enemy3_down2.png').convert_alpha(),
            pygame.image.load('images/enemy3_down3.png').convert_alpha(),
            pygame.image.load('images/enemy3_down4.png').convert_alpha(),
            pygame.image.load('images/enemy3_down5.png').convert_alpha(),
            pygame.image.load('images/enemy3_down6.png').convert_alpha()
            ])
        self.image_hit = pygame.image.load('images/enemy3_hit.png').convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image1)
        self.appear = False
        self.reset()
        self.energy = BigEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-20 * self.height, -10 * self.height) 
        self.active = True
        self.energy = BigEnemy.energy
