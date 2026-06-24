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
        # 追击AI属性
        self.chase_speed = 1.5
        self.aggro_range = 300
        self.attack_range = 40
        self.attack_cooldown = 60
        self.attack_timer = 0
        self.is_attacking = False

    def take_damage(self, damage):
        """
        受到伤害
        :param damage: 伤害值
        """
        self.hp -= damage
        self.trigger_hit_effect()
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def update(self):
        """更新怪物状态"""
        self.update_hit_effect()
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
        self.sync_rect_to_image()

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

    def chase_and_attack(self, player_x, player_y):
        """
        追击并攻击玩家
        :param player_x: 玩家x坐标
        :param player_y: 玩家y坐标
        """
        if not self.is_alive:
            return

        dx = player_x - self.pos_x
        dy = player_y - self.pos_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # 攻击冷却
        if self.attack_timer > 0:
            self.attack_timer -= 1

        # 攻击中不移动
        if self.is_attacking:
            return

        # 攻击范围内
        if distance < self.attack_range and self.attack_timer <= 0:
            self.is_attacking = True
            self.set_state('fight')
            self.attack_timer = self.attack_cooldown
            return

        # 仇恨范围内追击
        if distance < self.aggro_range and distance > 0:
            self.set_state('run')
            # 归一化并移动
            nx = dx / distance
            ny = dy / distance
            self.pos_x += nx * self.chase_speed
            self.pos_y += ny * self.chase_speed
            self.update_rect()
        else:
            self.set_state('station')

    def try_deal_damage(self):
        """
        尝试造成伤害 (攻击动画结束时调用)
        :return: 伤害值，否则返回0
        """
        if self.is_attacking and self.current_state == 'fight':
            if self.animations['fight'].is_end():
                self.is_attacking = False
                self.set_state('station')
                return self.attack_power
        return 0
