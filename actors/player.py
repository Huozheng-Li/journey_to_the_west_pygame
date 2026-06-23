"""
孙悟空 - 探索版
步骤9: 玩家主角设计
"""
import pygame
from .base_actor import ActorBase
from .action import Action


class Player(ActorBase):
    """
    孙悟空 - 探索模式
    支持4方向移动和动画
    """

    def __init__(self, x, y, map_width=3780, map_height=2395):
        """
        初始化孙悟空
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param map_width: 地图宽度
        :param map_height: 地图高度
        """
        super().__init__(x, y, 48, 68, speed=4)
        self.map_width = map_width
        self.map_height = map_height
        self.animations = {}
        self.is_moving = False
        self.is_talking = False
        self._load_animations()

    def _load_animations(self):
        """加载4方向动画 - 128帧: 下(1-32), 左(33-64), 上(65-96), 右(97-128)"""
        self.animations = {
            self.DOWN: Action('swk2', 'China_SunWuKong_', 32, True, start_index=1),
            self.LEFT: Action('swk2', 'China_SunWuKong_', 32, True, start_index=33),
            self.UP: Action('swk2', 'China_SunWuKong_', 32, True, start_index=65),
            self.RIGHT: Action('swk2', 'China_SunWuKong_', 32, True, start_index=97),
        }
        if self.DOWN in self.animations:
            self.image = self.animations[self.DOWN].get_current_image()

    def update(self, keys, obstacles=None):
        """
        更新玩家状态
        :param keys: 按键状态
        :param obstacles: 障碍物列表
        """
        if self.is_talking:
            return

        self.is_moving = False
        dx, dy = 0, 0

        if keys[pygame.K_s]:
            self.direction = self.DOWN
            dy = self.speed
            self.is_moving = True
        elif keys[pygame.K_w]:
            self.direction = self.UP
            dy = -self.speed
            self.is_moving = True
        elif keys[pygame.K_a]:
            self.direction = self.LEFT
            dx = -self.speed
            self.is_moving = True
        elif keys[pygame.K_d]:
            self.direction = self.RIGHT
            dx = self.speed
            self.is_moving = True

        if self.is_moving:
            new_x = self.pos_x + dx
            new_y = self.pos_y + dy

            new_x = max(0, min(new_x, self.map_width - self.width))
            new_y = max(0, min(new_y, self.map_height - self.height))

            if obstacles:
                test_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                for obstacle in obstacles:
                    if test_rect.colliderect(obstacle):
                        return

            self.set_position(new_x, new_y)

        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.direction in self.animations:
            action = self.animations[self.direction]
            if self.is_moving:
                self.image = action.get_current_image()
            else:
                action.reset()
                self.image = action.get_current_image()

    def draw(self, surface):
        """绘制玩家"""
        if self.image:
            surface.blit(self.image, self.rect)
