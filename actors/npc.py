"""
NPC基类
步骤14: 玩家与NPC碰撞交互
"""
import pygame
import random
from .base_actor import ActorBase


class NPCBase(ActorBase):
    """
    NPC基类
    所有NPC的父类
    """

    def __init__(self, x, y, width, height, speed=2):
        """
        初始化NPC
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 角色宽度
        :param height: 角色高度
        :param speed: 移动速度
        """
        super().__init__(x, y, width, height, speed)
        self.dialogs = []
        self.dialog_index = 0
        self.is_auto_move = False
        self.move_timer = 0

    def get_dialog(self):
        """
        获取当前对话
        :return: 对话内容
        """
        if self.dialogs and self.dialog_index < len(self.dialogs):
            return self.dialogs[self.dialog_index]
        return None

    def next_dialog(self):
        """下一条对话"""
        if self.dialog_index < len(self.dialogs) - 1:
            self.dialog_index += 1
            return True
        return False

    def reset_dialog(self):
        """重置对话索引"""
        self.dialog_index = 0

    def auto_move(self):
        """自动移动"""
        if not self.is_auto_move:
            return

        self.move_timer += 1
        if self.move_timer > 60:
            self.direction = random.choice([self.DOWN, self.LEFT, self.UP, self.RIGHT])
            self.move_timer = 0

        dx, dy = 0, 0
        if self.direction == self.DOWN:
            dy = self.speed
        elif self.direction == self.UP:
            dy = -self.speed
        elif self.direction == self.LEFT:
            dx = -self.speed
        elif self.direction == self.RIGHT:
            dx = self.speed

        self.pos_x += dx
        self.pos_y += dy
        self.update_rect()
