"""
孙悟空 - 战斗版
步骤19: 玩家打斗人物实现
"""
import pygame
from .base_actor import ActorBase
from .action import Action


class BattlePlayer(ActorBase):
    """
    孙悟空 - 战斗模式
    支持攻击、防御、受伤动画
    """

    def __init__(self, x, y):
        """
        初始化战斗玩家
        :param x: 初始x坐标
        :param y: 初始y坐标
        """
        super().__init__(x, y, 64, 64, speed=4)
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 20
        self.is_alive = True
        self.animations = {}
        self.current_state = 'station'
        self._load_animations()

    def _load_animations(self):
        """加载战斗动画 - 16帧: 方向0(00000-00003), 方向1(01000-01003), 方向2(02000-02003), 方向3(03000-03003)"""
        self.animations = {
            'station': Action('swk', '', 4, True, start_index=0),
            'fight': Action('swk', '', 4, False, start_index=1000),
            'back': Action('swk', '', 4, True, start_index=2000),
            'look': Action('swk', '', 4, True, start_index=3000),
            'run': Action('swk', '', 4, True, start_index=0),
        }
        if 'station' in self.animations:
            self.image = self.animations['station'].get_current_image()

    def take_damage(self, damage):
        """
        受到伤害
        :param damage: 伤害值
        """
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def attack(self):
        """执行攻击"""
        self.current_state = 'fight'
        self.animations['fight'].reset()

    def update(self):
        """更新战斗玩家状态"""
        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.current_state in self.animations:
            action = self.animations[self.current_state]
            self.image = action.get_current_image()

    def draw(self, surface):
        """绘制战斗玩家"""
        if self.image:
            surface.blit(self.image, self.rect)
