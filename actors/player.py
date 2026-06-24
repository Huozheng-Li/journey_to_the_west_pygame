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
        # 碰撞框：50%宽，35%高，底部对齐（脚部区域）
        self.col_w = int(self.width * 0.5)
        self.col_h = int(self.height * 0.35)
        self.col_offset_x = (self.width - self.col_w) // 2
        self.col_offset_y = self.height - self.col_h - 2

    def _load_animations(self):
        """加载4方向动画 - swk素材: 下(0-3), 左(1000-1003), 上(2000-2003), 右(3000-3003)"""
        self.animations = {
            self.DOWN: Action('swk', '', 4, True, start_index=0, frame_delay=2),
            self.LEFT: Action('swk', '', 4, True, start_index=1000, frame_delay=2),
            self.UP: Action('swk', '', 4, True, start_index=2000, frame_delay=2),
            self.RIGHT: Action('swk', '', 4, True, start_index=3000, frame_delay=2),
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
        if self.is_talking:
            return

        self.is_moving = False
        dx, dy = 0, 0
        current_speed = self.speed * 0.5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else self.speed

        # 方向设置 (视觉) - elif保证只有一个方向
        if keys[pygame.K_s]:
            self.direction = self.DOWN
        elif keys[pygame.K_w]:
            self.direction = self.UP
        elif keys[pygame.K_a]:
            self.direction = self.LEFT
        elif keys[pygame.K_d]:
            self.direction = self.RIGHT

        # 速度计算 (移动) - if独立累加支持斜向移动
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

            new_x = max(0, min(new_x, self.map_width - self.width))
            new_y = max(0, min(new_y, self.map_height - self.height))

            # 碰撞检测使用脚部区域
            test_rect = pygame.Rect(new_x + self.col_offset_x, new_y + self.col_offset_y,
                                    self.col_w, self.col_h)

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
        return pygame.Rect(self.pos_x + self.col_offset_x, self.pos_y + self.col_offset_y,
                           self.col_w, self.col_h)

    def debug_draw(self, surface, offset_x=0, offset_y=0):
        """调试绘制：红框=素材，蓝框=脚部碰撞"""
        screen_x = self.pos_x - offset_x
        screen_y = self.pos_y - offset_y
        surface.blit(self.image, (screen_x, screen_y))
        # 红色框 - 素材边界
        img_rect = pygame.Rect(screen_x, screen_y, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(surface, (255, 0, 0), img_rect, 2)
        # 蓝色框 - 脚部碰撞区域
        col_rect = pygame.Rect(screen_x + self.col_offset_x, screen_y + self.col_offset_y,
                               self.col_w, self.col_h)
        pygame.draw.rect(surface, (0, 100, 255), col_rect, 2)
