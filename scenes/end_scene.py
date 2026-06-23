"""
结束场景
步骤22: 游戏状态管理
"""
import pygame
from .base_scene import SceneBase
from config import SCREEN_WIDTH, SCREEN_HEIGHT, IMG_DIR, FONT_DIR


class EndScene(SceneBase):
    """
    结束场景
    显示胜利或失败画面
    """

    def __init__(self, screen, is_win=True):
        """
        初始化结束场景
        :param screen: 主屏幕surface
        :param is_win: 是否胜利
        """
        super().__init__(screen)
        self.is_win = is_win
        self.bg_image = None
        self.font = None
        self._load_resources()

    def _load_resources(self):
        """加载资源"""
        try:
            self.font = pygame.font.Font(f"{FONT_DIR}/newfont.TTF", 48)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.SysFont('simhei', 48)

        if self.is_win:
            try:
                self.bg_image = pygame.image.load(f"{IMG_DIR}/win.jpg")
                self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except (FileNotFoundError, pygame.error):
                self.bg_image = None
        else:
            try:
                self.bg_image = pygame.image.load(f"{IMG_DIR}/fail.jpg")
                self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except (FileNotFoundError, pygame.error):
                self.bg_image = None

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.is_active = False

    def update(self):
        """更新结束场景"""
        pass

    def draw(self):
        """绘制结束场景"""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        if self.is_win:
            text = "胜利！"
            color = (255, 215, 0)
        else:
            text = "失败！"
            color = (255, 0, 0)

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

        hint_surface = self.font.render("按空格键或ESC退出", True, (200, 200, 200))
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(hint_surface, hint_rect)
