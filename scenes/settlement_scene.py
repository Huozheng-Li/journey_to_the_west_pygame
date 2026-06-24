"""
结算画面
战斗胜利/失败后显示战斗结果
"""
import pygame
import os
from .base_scene import SceneBase
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR


class SettlementScene(SceneBase):
    """
    结算画面
    显示战斗结果、属性加成等信息
    """

    def __init__(self, screen, player_stats=None):
        """
        初始化结算画面
        :param screen: 主屏幕surface
        :param player_stats: 玩家属性
        """
        super().__init__(screen)
        self.player_stats = player_stats
        self.font = None
        self.small_font = None
        self._load_fonts()

    def _load_fonts(self):
        """加载字体"""
        try:
            self.font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 48)
            self.small_font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 24)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.SysFont('simhei', 48)
            self.small_font = pygame.font.SysFont('simhei', 24)

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    self.next_scene = 'village'

    def draw(self):
        """绘制结算画面"""
        self.screen.fill((20, 20, 40))

        # 根据胜负显示不同标题
        if self.player_stats and self.player_stats.last_battle_won:
            title_text = "战斗胜利！"
            title_color = (255, 215, 0)
        else:
            title_text = "战斗失败..."
            title_color = (255, 100, 100)

        # 标题
        title = self.font.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        # 分割线
        pygame.draw.line(self.screen, (100, 100, 100),
                         (SCREEN_WIDTH // 4, 140), (SCREEN_WIDTH * 3 // 4, 140))

        # 统计信息
        y = 180
        stats = []

        if self.player_stats:
            stats = [
                (f"击败敌人数量: {self.player_stats.total_enemies_defeated}", (255, 255, 255)),
                ("", None),  # 空行
                ("当前属性:", (200, 200, 200)),
                (f"  血量 (HP): {self.player_stats.hp}", (0, 200, 0)),
                (f"  攻击力 (ATK): {self.player_stats.attack_power}", (255, 200, 0)),
                ("", None),  # 空行
                ("属性加成:", (200, 200, 200)),
                (f"  村民加成次数: {self.player_stats.elder_bonus_count}/{self.player_stats.MAX_ELDER_BONUSES}", (150, 255, 150)),
                (f"  唐僧加成次数: {self.player_stats.tang_bonus_count}/{self.player_stats.MAX_TANG_BONUSES}", (255, 200, 150)),
            ]
        else:
            stats = [
                ("击败敌人数量: 0", (255, 255, 255)),
            ]

        for text, color in stats:
            if text == "":
                y += 25
                continue
            surface = self.small_font.render(text, True, color or (255, 255, 255))
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(surface, rect)
            y += 40

        # 提示
        y += 50
        hint = self.small_font.render("按空格键返回村庄", True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(hint, hint_rect)
