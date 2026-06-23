"""
战斗场景
步骤20-21: 打斗场景设计和应用
"""
import pygame
from .base_scene import SceneBase
from actors.battle_player import BattlePlayer
from actors.enemy import Cattle
from systems.battle import BattleSystem, BattleStatus
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR


class BattleScene(SceneBase):
    """
    战斗场景
    与怪物战斗
    """

    def __init__(self, screen):
        """
        初始化战斗场景
        :param screen: 主屏幕surface
        """
        super().__init__(screen)
        self.player = BattlePlayer(200, 300)
        self.enemy = Cattle(500, 300)
        self.battle_system = BattleSystem()
        self.font = None
        self._load_font()

    def _load_font(self):
        """加载字体"""
        try:
            self.font = pygame.font.Font(f"{FONT_DIR}/newfont.TTF", 24)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.SysFont('simhei', 24)

    def on_enter(self):
        """进入战斗场景"""
        super().on_enter()
        self.player = BattlePlayer(200, 300)
        self.enemy = Cattle(500, 300)
        self.battle_system.start_battle(self.player, self.enemy)

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
                elif event.key == pygame.K_SPACE:
                    if self.battle_system.is_battle_end():
                        if self.battle_system.get_status() == BattleStatus.WIN:
                            self.next_scene = 'end_win'
                        else:
                            self.next_scene = 'end_lose'
                    elif self.battle_system.get_status() == BattleStatus.FIGHTING:
                        self.battle_system.player_attack()

    def update(self):
        """更新战斗场景"""
        if self.player:
            self.player.update()
        if self.enemy:
            self.enemy.update()

    def draw(self):
        """绘制战斗场景"""
        self.screen.fill((50, 50, 80))

        if self.player:
            self.screen.blit(self.player.image, (self.player.pos_x, self.player.pos_y))
            self._draw_hp_bar(self.player.pos_x, self.player.pos_y - 30,
                             self.player.hp, self.player.max_hp, "孙悟空")

        if self.enemy:
            self.screen.blit(self.enemy.image, (self.enemy.pos_x, self.enemy.pos_y))
            self._draw_hp_bar(self.enemy.pos_x, self.enemy.pos_y - 30,
                             self.enemy.hp, self.enemy.max_hp, "牛怪")

        self._draw_battle_log()
        self._draw_instructions()

    def _draw_hp_bar(self, x, y, hp, max_hp, name):
        """绘制血条"""
        bar_width = 100
        bar_height = 10
        hp_ratio = hp / max_hp

        name_surface = self.font.render(name, True, (255, 255, 255))
        self.screen.blit(name_surface, (x, y - 25))

        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, int(bar_width * hp_ratio), bar_height))

    def _draw_battle_log(self):
        """绘制战斗日志"""
        y = 450
        for i, log in enumerate(self.battle_system.battle_log):
            log_surface = self.font.render(log, True, (255, 255, 255))
            self.screen.blit(log_surface, (50, y + i * 30))

    def _draw_instructions(self):
        """绘制操作提示"""
        if self.battle_system.is_battle_end():
            hint = "按空格键结束战斗"
        else:
            hint = "按空格键攻击"
        hint_surface = self.font.render(hint, True, (200, 200, 200))
        self.screen.blit(hint_surface, (50, 550))
