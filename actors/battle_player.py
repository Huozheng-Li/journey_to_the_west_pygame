"""
孙悟空 - 战斗版
支持WASD移动、鼠标点击攻击、4方向动画、十万八千里闪现
"""
import pygame
import random
from .base_actor import ActorBase
from .action import Action
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class BattlePlayer(ActorBase):
    """
    孙悟空 - 战斗模式
    支持WSD移动、攻击状态、挥砍范围
    """

    def __init__(self, x, y, map_width=None, map_height=None):
        """
        初始化战斗玩家
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param map_width: 地图宽度
        :param map_height: 地图高度
        """
        super().__init__(x, y, 90, 126, speed=4)
        self.map_width = map_width or SCREEN_WIDTH
        self.map_height = map_height or SCREEN_HEIGHT
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 20
        self.is_alive = True
        self.is_moving = False
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 20  # 攻击动画帧数
        self.prev_direction = self.DOWN
        self.animations = {}
        self._load_animations()
        self.sync_rect_to_image()
        # 十万八千里传送技能
        self.is_teleporting = False
        self.teleport_timer = 0
        self.magic_action = Action('magic/appear', '0000-b788e5a-', 18, False, start_index=0, frame_delay=2)
        # 缩放magic动画到角色大小的1.5倍
        scale = 0.8
        self.magic_action.action_images = [
            pygame.transform.smoothscale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            for img in self.magic_action.action_images
        ]
        self.magic_image = None
        self.magic_offset_y = -20  # magic动画相对角色的Y偏移

    def _load_animations(self):
        """加载4方向动画 - swk素材: 下(0-3), 左(1000-1003), 上(2000-2003), 右(3000-3003)"""
        self.animations = {
            'station': {
                self.DOWN: Action('swk', '', 4, True, start_index=0, frame_delay=2),
                self.LEFT: Action('swk', '', 4, True, start_index=1000, frame_delay=2),
                self.UP: Action('swk', '', 4, True, start_index=2000, frame_delay=2),
                self.RIGHT: Action('swk', '', 4, True, start_index=3000, frame_delay=2),
            },
            'run': {
                self.DOWN: Action('swk', '', 4, True, start_index=0, frame_delay=2),
                self.LEFT: Action('swk', '', 4, True, start_index=1000, frame_delay=2),
                self.UP: Action('swk', '', 4, True, start_index=2000, frame_delay=2),
                self.RIGHT: Action('swk', '', 4, True, start_index=3000, frame_delay=2),
            },
            'fight': {
                self.DOWN: Action('swk', '', 4, False, start_index=0, frame_delay=2),
                self.LEFT: Action('swk', '', 4, False, start_index=1000, frame_delay=2),
                self.UP: Action('swk', '', 4, False, start_index=2000, frame_delay=2),
                self.RIGHT: Action('swk', '', 4, False, start_index=3000, frame_delay=2),
            },
        }
        # 缩放所有帧到目标尺寸
        target_w, target_h = 90, 126
        for state, direction_dict in self.animations.items():
            for direction, action in direction_dict.items():
                action.action_images = [
                    pygame.transform.scale(img, (target_w, target_h))
                    for img in action.action_images
                ]
        if self.DOWN in self.animations.get('station', {}):
            self.image = self.animations['station'][self.DOWN].peek_current_image()

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

    def start_attack(self):
        """开始攻击动画"""
        if not self.is_attacking and self.is_alive:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            # 重置当前方向的攻击动画
            if self.direction in self.animations.get('fight', {}):
                self.animations['fight'][self.direction].reset()

    def get_attack_rect(self):
        """
        获取挥砍范围碰撞框 (基于当前方向)
        :return: 攻击范围矩形
        """
        attack_range = 60
        attack_width = 80
        attack_height = 40

        cx = self.pos_x + self.width // 2
        cy = self.pos_y + self.height // 2

        if self.direction == self.DOWN:
            return pygame.Rect(cx - attack_width // 2, cy, attack_width, attack_range)
        elif self.direction == self.UP:
            return pygame.Rect(cx - attack_width // 2, cy - attack_range, attack_width, attack_range)
        elif self.direction == self.LEFT:
            return pygame.Rect(cx - attack_range, cy - attack_height // 2, attack_range, attack_height)
        elif self.direction == self.RIGHT:
            return pygame.Rect(cx, cy - attack_height // 2, attack_range, attack_height)
        # 默认向下
        return pygame.Rect(cx - attack_width // 2, cy, attack_width, attack_range)

    def start_teleport(self, dest_x, dest_y):
        """
        十万八千里 - 闪现到目标位置，立即可移动，magic动画跟随
        :param dest_x: 目标x坐标
        :param dest_y: 目标y坐标
        """
        self.is_teleporting = True
        self.is_attacking = False
        self.attack_timer = 0
        self.teleport_timer = self.magic_action.image_count * self.magic_action.frame_delay
        self.set_position(dest_x, dest_y)
        self.magic_action.reset()
        self.magic_image = self.magic_action.get_current_image()

    def draw_magic(self, surface, offset_x=0, offset_y=0):
        """在角色中心叠加绘制magic动画，带闪烁效果"""
        if self.is_teleporting and self.magic_image:
            # 每2帧闪烁一次（奇数帧跳过绘制）
            if self.teleport_timer % 4 < 2:
                screen_x = self.pos_x - offset_x
                screen_y = self.pos_y - offset_y
                magic_rect = self.magic_image.get_rect()
                magic_rect.center = (screen_x + self.width // 2, screen_y + self.height // 2)
                surface.blit(self.magic_image, magic_rect)

    def update(self, keys=None):
        """
        更新战斗玩家状态
        :param keys: 键盘状态 (pygame.key.get_pressed())
        """
        # 更新受击效果
        self.update_hit_effect()

        # 传送特效倒计时（不阻止移动）
        if self.is_teleporting:
            self.teleport_timer -= 1
            self.magic_image = self.magic_action.get_current_image()
            if self.teleport_timer <= 0:
                self.is_teleporting = False
                self.magic_image = None

        # 攻击中不能移动
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
            self._update_animation()
            return

        self.is_moving = False
        dx, dy = 0, 0
        current_speed = self.speed

        if keys:
            # 方向设置 (视觉)
            if keys[pygame.K_s]:
                self.direction = self.DOWN
            elif keys[pygame.K_w]:
                self.direction = self.UP
            elif keys[pygame.K_a]:
                self.direction = self.LEFT
            elif keys[pygame.K_d]:
                self.direction = self.RIGHT

            # 速度计算 (移动)
            if keys[pygame.K_s]:
                dy += current_speed
                self.is_moving = True
            if keys[pygame.K_w]:
                dy -= current_speed
                self.is_moving = True
            if keys[pygame.K_a]:
                dx -= current_speed
                self.is_moving = True
            if keys[pygame.K_d]:
                dx += current_speed
                self.is_moving = True

            if dx != 0 and dy != 0:
                dx *= 0.707
                dy *= 0.707

            if self.is_moving:
                new_x = self.pos_x + dx
                new_y = self.pos_y + dy
                # 边界限制
                new_x = max(0, min(new_x, self.map_width - self.width))
                new_y = max(0, min(new_y, self.map_height - self.height))
                self.set_position(new_x, new_y)

        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.is_attacking:
            # 攻击动画
            anim = self.animations.get('fight', {}).get(self.direction)
            if anim:
                self.image = anim.get_current_image()
        elif self.is_moving:
            # 移动动画
            anim = self.animations.get('run', {}).get(self.direction)
            if anim:
                self.image = anim.get_current_image()
        else:
            # 站立动画
            anim = self.animations.get('station', {}).get(self.direction)
            if anim:
                anim.reset()
                self.image = anim.peek_current_image()

    def draw(self, surface):
        """绘制战斗玩家 - 居中显示避免跳动"""
        if self.image:
            img_rect = self.image.get_rect()
            img_rect.center = (self.rect.centerx, self.rect.centery)
            surface.blit(self.image, img_rect)

