"""
怪物基类和牛怪
步骤18: 打斗NPC人物实现
"""
import pygame
from .base_actor import ActorBase
from .action import Action


class EnemyBase(ActorBase):
    """
    怪物基类
    所有怪物的父类
    """

    def __init__(self, x, y, width, height, hp=50, attack_power=10):
        """
        初始化怪物
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 角色宽度
        :param height: 角色高度
        :param hp: 生命值
        :param attack_power: 攻击力
        """
        super().__init__(x, y, width, height, speed=2)
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.is_alive = True
        self.animations = {}
        self.current_state = 'station'

    def take_damage(self, damage):
        """
        受到伤害
        :param damage: 伤害值
        """
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def update(self):
        """更新怪物状态"""
        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.current_state in self.animations:
            action = self.animations[self.current_state]
            self.image = action.get_current_image()

    def draw(self, surface):
        """绘制怪物"""
        if self.image:
            surface.blit(self.image, self.rect)


class Cattle(EnemyBase):
    """
    牛怪 - 战斗敌人
    """

    def __init__(self, x, y):
        """
        初始化牛怪
        :param x: 初始x坐标
        :param y: 初始y坐标
        """
        super().__init__(x, y, 64, 64, hp=50, attack_power=10)
        self._load_animations()

    def _load_animations(self):
        """加载牛怪动画"""
        self.animations = {
            'station': Action('cattle/station', '1644-a85e8726-', 2, True, start_index=0),
            'walk1': Action('cattle/walk1', '1252-7f2abf21-', 5, True, start_index=0),
            'walk2': Action('cattle/walk2', '1962-cb5fe03a-', 5, True, start_index=0),
            'fight': Action('cattle/fight', '0618-3c4fe166-', 13, False, start_index=0),
            'die': Action('cattle/die', '0762-4cbbea5a-', 11, False, start_index=0),
            'back': Action('cattle/back', '1172-75d7e3ed-', 12, True, start_index=0),
            'look': Action('cattle/look', '2193-e6e7de44-', 9, True, start_index=0),
            'run': Action('cattle/run', '0045-4fe166f-', 6, True, start_index=0),
        }
        if 'station' in self.animations:
            self.image = self.animations['station'].get_current_image()

    def set_state(self, state):
        """
        设置动画状态
        :param state: 状态名称
        """
        if state in self.animations:
            self.current_state = state
            self.animations[state].reset()
