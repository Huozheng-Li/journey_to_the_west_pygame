"""
孙悟空 - 探索版
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
        super().__init__(x, y, 90, 126, speed=4)
        self.map_width = map_width
        self.map_height = map_height
        self.animations = {}
        self.is_moving = False
        self.is_talking = False
        self.prev_direction = self.DOWN
        self._load_animations()
        self.sync_rect_to_image()

    def _load_animations(self):
        """加载4方向动画 - swk素材: 下(0-3), 左(1000-1003), 上(2000-2003), 右(3000-3003)"""
        self.animations = {
            self.DOWN: Action('swk', '', 4, True, start_index=0, frame_delay=2, direction=0),
            self.LEFT: Action('swk', '', 4, True, start_index=0, frame_delay=2, direction=1000),
            self.UP: Action('swk', '', 4, True, start_index=0, frame_delay=2, direction=2000),
            self.RIGHT: Action('swk', '', 4, True, start_index=0, frame_delay=2, direction=3000),
        }
        # 缩放所有帧到目标尺寸
        target_w, target_h = 90, 126
        for direction, action in self.animations.items():
            action.action_images = [
                pygame.transform.scale(img, (target_w, target_h))
                for img in action.action_images
            ]
        if self.DOWN in self.animations:
            self.image = self.animations[self.DOWN].peek_current_image()

    def update(self, keys, obstacles=None, walkable_areas=None):
        """更新玩家状态"""
        self.update_hit_effect()
        if self.is_talking:
            return

        self.is_moving = False
        dx, dy = 0, 0
        current_speed = self.speed * 0.5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else self.speed

        # 方向设置 (视觉) - 等距视角45度映射
        if keys[pygame.K_s]:
            self.direction = self.DOWN
        elif keys[pygame.K_w]:
            self.direction = self.UP
        elif keys[pygame.K_a]:
            self.direction = self.LEFT
        elif keys[pygame.K_d]:
            self.direction = self.RIGHT

        # 速度计算 - 等距视角：W左上 A左下 S右下 D右上
        if keys[pygame.K_w]:
            dx -= current_speed
            dy -= current_speed
            self.is_moving = True
        if keys[pygame.K_a]:
            dx -= current_speed
            dy += current_speed
            self.is_moving = True
        if keys[pygame.K_s]:
            dx += current_speed
            dy += current_speed
            self.is_moving = True
        if keys[pygame.K_d]:
            dx += current_speed
            dy -= current_speed
            self.is_moving = True

        # 向量归一化：保证任意组合速度一致
        length = (dx * dx + dy * dy) ** 0.5
        if length > 0:
            dx = dx / length * current_speed
            dy = dy / length * current_speed

        if self.is_moving:
            new_x = self.pos_x + dx
            new_y = self.pos_y + dy

            new_x = max(0, min(new_x, self.map_width - self.width))
            new_y = max(0, min(new_y, self.map_height - self.height))

            # 碰撞检测使用脚部区域（50%宽，35%高，底部对齐）
            col_w = int(self.width * 0.5)
            col_h = int(self.height * 0.35)
            col_x = new_x + (self.width - col_w) // 2
            col_y = new_y + self.height - col_h - 2
            test_rect = pygame.Rect(col_x, col_y, col_w, col_h)

            if obstacles:
                for obstacle in obstacles:
                    if test_rect.colliderect(obstacle):
                        return

            if walkable_areas:
                in_area = any(test_rect.colliderect(area) for area in walkable_areas)
                if not in_area:
                    return

            self.set_position(new_x, new_y)

        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.direction in self.animations:
            if self.direction != self.prev_direction:
                self.animations[self.direction].reset()
                self.prev_direction = self.direction

            action = self.animations[self.direction]
            if self.is_moving:
                self.image = action.get_current_image()
            else:
                action.reset()
                self.image = action.peek_current_image()

    def draw(self, surface):
        """绘制玩家 - 居中显示避免跳动"""
        if self.image:
            img_rect = self.image.get_rect()
            # 以角色中心为基准居中绘制
            center_x = self.rect.centerx
            center_y = self.rect.centery
            img_rect.center = (center_x, center_y)
            surface.blit(self.image, img_rect)

    def get_col_rect(self):
        """获取脚部碰撞区域（用于NPC/怪物交互检测）"""
        col_w = int(self.width * 0.5)
        col_h = int(self.height * 0.35)
        col_x = self.pos_x + (self.width - col_w) // 2
        col_y = self.pos_y + self.height - col_h - 2
        return pygame.Rect(col_x, col_y, col_w, col_h)
