"""
碰撞系统
步骤12: 精灵碰撞检测
"""
import pygame


class CollisionSystem:
    """
    碰撞检测系统
    """

    @staticmethod
    def check_rect_collision(rect1, rect2):
        """
        矩形碰撞检测
        :param rect1: 矩形1
        :param rect2: 矩形2
        :return: 是否碰撞
        """
        return rect1.colliderect(rect2)

    @staticmethod
    def check_obstacle_collision(rect, obstacles):
        """
        检查与障碍物碰撞
        :param rect: 角色矩形
        :param obstacles: 障碍物列表
        :return: 是否碰撞
        """
        for obstacle in obstacles:
            if rect.colliderect(obstacle):
                return True
        return False

    @staticmethod
    def check_sprite_collision(sprite1, sprite2):
        """
        精灵碰撞检测
        :param sprite1: 精灵1
        :param sprite2: 精灵2
        :return: 是否碰撞
        """
        return pygame.sprite.collide_rect(sprite1, sprite2)

    @staticmethod
    def check_sprite_group_collision(sprite, group):
        """
        精灵与组碰撞检测
        :param sprite: 精灵
        :param group: 精灵组
        :return: 碰撞的精灵列表
        """
        return pygame.sprite.spritecollide(sprite, group, False)
