"""
角色基类
步骤7: Sprite运动行为
"""
import pygame
from config import DRAW_CHARACTER_EDGE


class ActorBase(pygame.sprite.Sprite):
    """
    所有角色的基类
    继承自pygame.sprite.Sprite
    """

    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, x, y, width, height, speed=4):
        """
        初始化角色
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 角色宽度
        :param height: 角色高度
        :param speed: 移动速度
        """
        super().__init__()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = self.DOWN
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(x), int(y))
        # 受击效果
        self.hit_timer = 0
        self.hit_duration = 10  # 受击闪烁持续帧数
        self.original_image = None

    def sync_rect_to_image(self):
        """同步碰撞矩形大小到当前图像尺寸（在加载动画后调用）"""
        if self.image:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect.size = (self.width, self.height)
            self.original_image = self.image.copy()

    def trigger_hit_effect(self):
        """触发受击效果"""
        self.hit_timer = self.hit_duration

    def _apply_hit_effect(self):
        """
        应用受击变色效果 (降低绿色和蓝色通道，使图片偏红)
        :return: 变色后的图片
        """
        if self.hit_timer <= 0 or self.original_image is None:
            return self.image

        # 每隔2帧闪烁一次
        if self.hit_timer % 4 < 2:
            # 创建变色后的图片
            hit_image = self.original_image.copy()
            # 使用 surfarray 操作像素
            try:
                pixels = pygame.surfarray.pixels3d(hit_image)
                # 降低绿色通道 (乘以0.5)
                pixels[:, :, 1] = (pixels[:, :, 1] * 0.5).astype(int)
                # 降低蓝色通道 (乘以0.5)
                pixels[:, :, 2] = (pixels[:, :, 2] * 0.5).astype(int)
                del pixels
            except Exception:
                # numpy不可用时的fallback：RGB乘法偏红
                hit_image.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
            return hit_image
        else:
            return self.original_image

    def update_hit_effect(self):
        """更新受击效果计时器"""
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def update_rect(self):
        """更新碰撞矩形位置"""
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

    def draw(self, surface, offset_x=0, offset_y=0):
        """
        绘制角色到surface
        :param surface: 目标surface
        :param offset_x: 摄像机X偏移
        :param offset_y: 摄像机Y偏移
        """
        screen_x = self.pos_x - offset_x
        screen_y = self.pos_y - offset_y
        # 应用受击效果
        draw_image = self._apply_hit_effect()
        surface.blit(draw_image, (screen_x, screen_y))

    def debug_draw(self, surface, offset_x=0, offset_y=0):
        """
        绘制角色并根据DRAW_CHARACTER_EDGE标志绘制调试边框
        红色框=素材边界，蓝色框=碰撞体积（脚部区域）
        """
        screen_x = self.pos_x - offset_x
        screen_y = self.pos_y - offset_y
        draw_image = self._apply_hit_effect()
        surface.blit(draw_image, (screen_x, screen_y))
        if DRAW_CHARACTER_EDGE:
            img_w = self.image.get_width()
            img_h = self.image.get_height()
            # 红色框 - 素材边界
            pygame.draw.rect(surface, (255, 0, 0),
                             pygame.Rect(screen_x, screen_y, img_w, img_h), 2)
            # 蓝色框 - 碰撞体积（脚部区域）
            col_w = int(img_w * 0.5)
            col_h = int(img_h * 0.35)
            col_x = screen_x + (img_w - col_w) // 2
            col_y = screen_y + img_h - col_h - 2
            pygame.draw.rect(surface, (0, 100, 255),
                             pygame.Rect(col_x, col_y, col_w, col_h), 2)

    def get_position(self):
        """
        获取角色位置
        :return: (x, y) 元组
        """
        return self.pos_x, self.pos_y

    def set_position(self, x, y):
        """
        设置角色位置
        :param x: x坐标
        :param y: y坐标
        """
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.update_rect()

    def get_rect(self):
        """
        获取碰撞矩形
        :return: pygame.Rect
        """
        return self.rect
