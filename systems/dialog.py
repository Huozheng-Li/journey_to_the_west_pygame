"""
对话系统
步骤15: 对话框实现
"""
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR


class DialogSystem:
    """
    对话系统
    显示对话框和文字
    """

    def __init__(self):
        """初始化对话系统"""
        self.is_dialog_active = False
        self.current_dialog = None
        self.font = None
        self.dialog_surface = None
        self._load_font()

    def _load_font(self):
        """加载字体"""
        try:
            self.font = pygame.font.Font(f"{FONT_DIR}/newfont.TTF", 24)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.SysFont('simhei', 24)

    def start_dialog(self, dialog):
        """
        开始对话
        :param dialog: 对话内容 {"speaker": "xxx", "text": "xxx"}
        """
        self.is_dialog_active = True
        self.current_dialog = dialog
        self._create_dialog_surface()

    def end_dialog(self):
        """结束对话"""
        self.is_dialog_active = False
        self.current_dialog = None
        self.dialog_surface = None

    def _create_dialog_surface(self):
        """创建对话框表面"""
        width = SCREEN_WIDTH - 100
        height = 120
        x = 50
        y = SCREEN_HEIGHT - height - 30

        self.dialog_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.dialog_surface.fill((0, 0, 0, 200))
        self.dialog_rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        """
        绘制对话框
        :param screen: 主屏幕
        """
        if not self.is_dialog_active or not self.dialog_surface:
            return

        screen.blit(self.dialog_surface, self.dialog_rect)

        if self.current_dialog:
            speaker = self.current_dialog.get("speaker", "")
            text = self.current_dialog.get("text", "")

            speaker_surface = self.font.render(speaker, True, (255, 255, 0))
            screen.blit(speaker_surface, (self.dialog_rect.x + 20, self.dialog_rect.y + 15))

            text_surface = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (self.dialog_rect.x + 20, self.dialog_rect.y + 55))

            hint_surface = self.font.render("按空格键继续", True, (150, 150, 150))
            screen.blit(hint_surface, (self.dialog_rect.x + 20, self.dialog_rect.y + 90))
