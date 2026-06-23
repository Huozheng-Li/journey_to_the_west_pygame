"""
动画行为类
步骤6: Sprite应用
"""
import pygame
import os
from config import IMG_DIR


class Action:
    """
    角色动画行为类
    管理帧动画的加载、播放、切换
    """

    def __init__(self, path, prefix, image_count, is_loop=True, start_index=1):
        """
        初始化动画行为
        :param path: 图片目录路径 (如 'elder', 'cattle/fight')
        :param prefix: 文件名前缀 (如 'elder1-0000')
        :param image_count: 帧数量
        :param is_loop: 是否循环播放
        :param start_index: 起始帧索引 (默认为1)
        """
        self.image_index = 0
        self.image_count = image_count
        self.is_loop = is_loop
        self.action_images = []

        full_path = os.path.join(IMG_DIR, path)
        for i in range(image_count):
            frame_num = start_index + i
            img_path = os.path.join(full_path, f"{prefix}{frame_num:05d}.png")
            try:
                image = pygame.image.load(img_path).convert_alpha()
                self.action_images.append(image)
            except FileNotFoundError:
                try:
                    img_path = os.path.join(full_path, f"{prefix}{frame_num:05d}.tga")
                    image = pygame.image.load(img_path).convert_alpha()
                    self.action_images.append(image)
                except FileNotFoundError:
                    print(f"无法加载图片: {prefix}{frame_num:05d}")

    def get_current_image(self):
        """
        获取当前帧图像
        :return: 当前帧的Surface
        """
        if not self.action_images:
            return None

        image = self.action_images[self.image_index]

        if self.is_loop:
            self.image_index = (self.image_index + 1) % self.image_count
        else:
            if self.image_index < self.image_count - 1:
                self.image_index += 1

        return image

    def is_end(self):
        """
        检查动画是否播放完毕
        :return: 是否结束
        """
        if self.is_loop:
            return False
        return self.image_index >= self.image_count - 1

    def reset(self):
        """重置动画到第一帧"""
        self.image_index = 0

    def set_image_count(self, count):
        """
        设置帧数量
        :param count: 新的帧数
        """
        self.image_count = count
