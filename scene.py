"""
场景类模块
"""
import os
import pygame
from utils.tiled_render import TiledRenderer


class TiledScene:
    """
    瓦格场景渲染类
    """

    def __init__(self, path, screen):
        """
        瓦格场景的构造函数
        :param path: 瓦格文件的路径
        :param screen: 游戏窗口surface
        """
        self.tiled_path = path
        self.screen = screen
        self.tiled = TiledRenderer(self.tiled_path)
        self.surface = pygame.Surface(self.tiled.pixel_size)
        self.tiled.render_map(self.surface)

    def get_surface(self):
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        return self.surface

    def draw(self):
        """
        绘制场景到屏幕
        """
        self.screen.blit(self.surface, (0, 0))

    def run(self):
        """
        场景的运行
        :return: 是否退出
        """
        scene_exit = False
        clock = pygame.time.Clock()

        while not scene_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene_exit = True

            self.draw()
            pygame.display.update()
            clock.tick(40)

        return scene_exit
