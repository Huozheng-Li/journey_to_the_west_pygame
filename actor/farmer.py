"""
农民角色模块
"""
import os
import pygame


class Farmer(pygame.sprite.Sprite):
    """
    农民角色类
    """

    def __init__(self, pos_x, pos_y):
        """
        初始化农民角色
        :param pos_x: 初始x位置
        :param pos_y: 初始y位置
        """
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 58
        self.height = 83

        # 加载图像
        self.images = []
        self.image_index = 0
        self.load_images()

        # 当前图像
        if self.images:
            self.image = self.images[0]
        else:
            # 如果没有图像，创建一个默认的
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((0, 255, 0))

        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)

    def load_images(self):
        """
        加载农民图像
        """
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(current_dir, 'resource', 'img', 'elder')
        for i in range(10):
            filename = f"elder1-0000{i}.tga"
            img_path = os.path.join(base_path, filename)
            if os.path.exists(img_path):
                img = pygame.image.load(img_path)
                self.images.append(img)

    def update(self):
        """
        更新农民状态
        """
        if self.images:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def draw(self, surface):
        """
        绘制农民
        :param surface: 目标surface
        """
        surface.blit(self.image, (self.pos_x, self.pos_y))
