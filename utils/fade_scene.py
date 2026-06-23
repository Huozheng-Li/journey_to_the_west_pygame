"""
渐变效果
步骤16: 场景切换渐入渐出
"""
import pygame
import enum


class SceneStatus(enum.IntEnum):
    """场景状态"""
    In = 1
    Normal = 2
    Out = 3
    Over = 4


class FadeScene:
    """
    渐变场景效果
    实现RGBA alpha通道渐变
    """

    def __init__(self, back_image):
        """
        初始化渐变效果
        :param back_image: 背景图片
        """
        self.back_image = back_image
        self.alpha = 0
        self.status = SceneStatus.In
        self.alpha_step = 20

    def set_status(self, status):
        """
        设置场景状态
        :param status: 新状态
        """
        self.status = status
        if status == SceneStatus.In:
            self.alpha = 0
        elif status == SceneStatus.Normal:
            self.alpha = 255
        elif status == SceneStatus.Out:
            self.alpha = 255

    def get_out(self):
        """
        检查渐出是否完成
        :return: 是否完成渐出
        """
        return self.status == SceneStatus.Over

    def update(self):
        """更新渐变状态"""
        if self.status == SceneStatus.In:
            self.alpha = min(255, self.alpha + self.alpha_step)
            if self.alpha >= 255:
                self.status = SceneStatus.Normal
        elif self.status == SceneStatus.Out:
            self.alpha = max(0, self.alpha - self.alpha_step)
            if self.alpha <= 0:
                self.status = SceneStatus.Over

    def get_back_image(self, x, y):
        """
        获取带alpha的背景图
        :param x: x坐标
        :param y: y坐标
        :return: 带alpha的surface
        """
        if self.back_image is None:
            return None

        surface = self.back_image.copy()
        surface.set_alpha(self.alpha)
        return surface
