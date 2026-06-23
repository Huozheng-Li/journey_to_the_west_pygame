"""
唐僧 - 剧情角色
步骤14: 玩家与NPC碰撞交互
"""
import pygame
from .npc import NPCBase


class Tang(NPCBase):
    """
    唐僧
    仅作为装饰角色，静止站立
    """

    def __init__(self, x, y):
        """
        初始化唐僧
        :param x: 初始x坐标
        :param y: 初始y坐标
        """
        super().__init__(x, y, 48, 68, speed=0)
        self.image = pygame.Surface((48, 68), pygame.SRCALPHA)
        self.image.fill((255, 200, 150, 200))

    def update(self):
        """唐僧不移动"""
        pass

    def draw(self, surface):
        """绘制唐僧"""
        surface.blit(self.image, self.rect)
