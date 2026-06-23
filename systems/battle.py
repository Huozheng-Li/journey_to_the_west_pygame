"""
战斗系统
步骤20-21: 打斗场景设计和应用
"""
import pygame
import enum


class BattleStatus(enum.IntEnum):
    """战斗状态"""
    READY = 1
    FIGHTING = 2
    WIN = 3
    LOSE = 4


class BattleSystem:
    """
    战斗系统
    管理战斗状态和逻辑
    """

    def __init__(self):
        """初始化战斗系统"""
        self.status = BattleStatus.READY
        self.player = None
        self.enemy = None
        self.battle_log = []
        self.turn_count = 0

    def start_battle(self, player, enemy):
        """
        开始战斗
        :param player: 玩家
        :param enemy: 敌人
        """
        self.player = player
        self.enemy = enemy
        self.status = BattleStatus.FIGHTING
        self.battle_log = []
        self.turn_count = 0
        self._add_log("战斗开始！")

    def player_attack(self):
        """玩家攻击"""
        if self.status != BattleStatus.FIGHTING:
            return

        if self.player and self.enemy:
            damage = self.player.attack_power
            self.enemy.take_damage(damage)
            self._add_log(f"孙悟空攻击造成 {damage} 点伤害！")

            if not self.enemy.is_alive:
                self.status = BattleStatus.WIN
                self._add_log("胜利！妖怪被打败了！")
            else:
                self.enemy_attack()

    def enemy_attack(self):
        """敌人攻击"""
        if self.status != BattleStatus.FIGHTING:
            return

        if self.player and self.enemy:
            damage = self.enemy.attack_power
            self.player.take_damage(damage)
            self._add_log(f"妖怪攻击造成 {damage} 点伤害！")

            if not self.player.is_alive:
                self.status = BattleStatus.LOSE
                self._add_log("失败！孙悟空被打败了！")

            self.turn_count += 1

    def _add_log(self, message):
        """添加战斗日志"""
        self.battle_log.append(message)
        if len(self.battle_log) > 5:
            self.battle_log.pop(0)

    def get_status(self):
        """
        获取战斗状态
        :return: 战斗状态
        """
        return self.status

    def is_battle_end(self):
        """
        检查战斗是否结束
        :return: 是否结束
        """
        return self.status in [BattleStatus.WIN, BattleStatus.LOSE]
