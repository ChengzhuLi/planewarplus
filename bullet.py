import pygame


class Bullet1(pygame.sprite.Sprite):
    """docstring for Bullet1"""
    def __init__(self, position):
        # python 2的老继承方式
        super(Bullet1, self).__init__()
        # 对于含有 alpha 通道的图片（支持部分位置透明，像 PNG 图像），需要使用 Surface.convert_alpha() 函数进行转换。
        # 返回的 Surface  对象将包含与源文件相同的颜色格式，colorkey 和 alpha 透明度通道。
        # 通常需要调用 Surface.convert() 函数进行转换，这样可以使得在屏幕上绘制的速度更快。
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        # Pygame 中处理图形遮罩的模块，参考csdn
        # pygame.mask.from_surface()  ——  从指定 Surface 对象中返回一个 Mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bullet2(pygame.sprite.Sprite):
    """docstring for Bullet2"""
    def __init__(self, position):
        super(Bullet2, self).__init__()

        self.image = pygame.image.load("images/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 14
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
