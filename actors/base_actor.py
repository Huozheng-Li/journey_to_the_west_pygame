"""
角色基类
步骤7: Sprite运动行为
"""
import pygame


class ActorBase(pygame.sprite.Sprite):
    """
    所有角色的基类
    继承自pygame.sprite.Sprite
    """

    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, x, y, width, height, speed=4):
        """
        初始化角色
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 角色宽度
        :param height: 角色高度
        :param speed: 移动速度
        """
        super().__init__()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = self.DOWN
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(x), int(y))

    def update_rect(self):
        """更新碰撞矩形位置"""
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

    def draw(self, surface):
        """
        绘制角色到surface
        :param surface: 目标surface
        """
        surface.blit(self.image, self.rect)

    def get_position(self):
        """
        获取角色位置
        :return: (x, y) 元组
        """
        return self.pos_x, self.pos_y

    def set_position(self, x, y):
        """
        设置角色位置
        :param x: x坐标
        :param y: y坐标
        """
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.update_rect()

    def get_rect(self):
        """
        获取碰撞矩形
        :return: pygame.Rect
        """
        return self.rect
