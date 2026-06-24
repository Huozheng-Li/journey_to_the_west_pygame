"""
战斗场景
支持WSAD移动、鼠标点击攻击、波次系统、HUD显示
"""
import pygame
import os
from .base_scene import SceneBase
from utils.tiled_render import TiledScene
from actors.battle_player import BattlePlayer
from actors.enemy import Cattle
from config import TMX_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR


class BattleScene(SceneBase):
    """
    实时战斗场景
    - WASD移动
    - 鼠标左键攻击
    - 敌人自动追击
    - 多波次战斗
    - HUD显示血条和攻击力
    """

    # 可调节的配置值
    TOTAL_WAVES = 3        # 总波次数
    WAVE_DELAY = 90        # 波次间隔 (帧数, 约2.25秒)

    def __init__(self, screen, player_stats=None):
        """
        初始化战斗场景
        :param screen: 主屏幕surface
        :param player_stats: 玩家属性
        """
        super().__init__(screen)
        self.player_stats = player_stats
        self.tiled_scene = None
        self.player = None
        self.enemy = None
        self.current_wave = 0
        self.enemies_defeated = 0
        self.wave_timer = 0
        self.between_waves = False
        self.battle_over = False
        self.battle_won = False
        self._battle_end_timer = 0
        self.font = None
        self.hud_font = None
        self._load_fonts()

    def _load_fonts(self):
        """加载字体"""
        try:
            self.font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 24)
            self.hud_font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 18)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.SysFont('simhei', 24)
            self.hud_font = pygame.font.SysFont('simhei', 18)

    def on_enter(self):
        """进入战斗场景"""
        super().on_enter()
        # 加载战斗地图
        try:
            self.tiled_scene = TiledScene(f"{TMX_DIR}/test.tmx")
        except (FileNotFoundError, pygame.error):
            self.tiled_scene = None

        map_width = SCREEN_WIDTH
        map_height = SCREEN_HEIGHT
        if self.tiled_scene:
            map_width, map_height = self.tiled_scene.get_map_size()

        # 读取出生点
        player_spawn = (100, 400)
        enemy_spawn = (600, 300)
        if self.tiled_scene:
            player_objs = self.tiled_scene.get_object_by_name('player_spawn')
            if player_objs:
                player_spawn = (player_objs[0].x, player_objs[0].y)
            enemy_objs = self.tiled_scene.get_object_by_name('enemy_spawn')
            if enemy_objs:
                enemy_spawn = (enemy_objs[0].x, enemy_objs[0].y)

        # 创建玩家 (使用持久化属性)
        self.player = BattlePlayer(player_spawn[0], player_spawn[1], map_width, map_height)
        if self.player_stats:
            self.player.hp = self.player_stats.hp
            self.player.max_hp = self.player_stats.hp
            self.player.attack_power = self.player_stats.attack_power
            self.player_stats.has_been_to_battle = True

        # 重置波次状态
        self.current_wave = 0
        self.enemies_defeated = 0
        self.between_waves = True
        self.wave_timer = self.WAVE_DELAY
        self.battle_over = False
        self.battle_won = False
        self._battle_end_timer = 60
        self.enemy_spawn = enemy_spawn

        # 生成第一波
        self._spawn_wave()

    def _spawn_wave(self):
        """生成新的一波敌人"""
        if self.current_wave >= self.TOTAL_WAVES:
            self.battle_over = True
            self.battle_won = True
            return

        self.enemy = Cattle(self.enemy_spawn[0], self.enemy_spawn[1])
        self.current_wave += 1
        self.between_waves = False

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.post(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.battle_over:
                    # 鼠标左键攻击
                    if self.player and not self.player.is_attacking:
                        self.player.start_attack()
                        self._check_attack_hit()

    def _check_attack_hit(self):
        """检查攻击是否命中敌人"""
        if not self.player or not self.enemy or not self.enemy.is_alive:
            return
        attack_rect = self.player.get_attack_rect()
        enemy_rect = self.enemy.get_rect()
        if attack_rect.colliderect(enemy_rect):
            self.enemy.take_damage(self.player.attack_power)
            if not self.enemy.is_alive:
                self.enemies_defeated += 1
                self.between_waves = True
                self.wave_timer = self.WAVE_DELAY

    def update(self):
        """更新战斗场景"""
        if self.battle_over:
            self._battle_end_timer -= 1
            if self._battle_end_timer <= 0:
                if self.player_stats:
                    self.player_stats.total_enemies_defeated = self.enemies_defeated
                    self.player_stats.last_battle_won = self.battle_won
                self.next_scene = 'settlement'
            return

        keys = pygame.key.get_pressed()

        # 更新玩家移动
        if self.player:
            self.player.update(keys)

        # 更新敌人AI
        if self.enemy and self.enemy.is_alive and self.player:
            self.enemy.chase_and_attack(self.player.pos_x, self.player.pos_y)
            self.enemy.update()  # 更新敌人动画
            # 敌人造成伤害
            damage = self.enemy.try_deal_damage()
            if damage > 0:
                self.player.take_damage(damage)
                if not self.player.is_alive:
                    self.battle_over = True
                    self.battle_won = False

        # 波次切换
        if self.between_waves:
            self.wave_timer -= 1
            if self.wave_timer <= 0:
                if self.current_wave < self.TOTAL_WAVES:
                    self._spawn_wave()
                else:
                    self.battle_over = True
                    self.battle_won = True

        # 检查玩家死亡
        if self.player and not self.player.is_alive:
            self.battle_over = True
            self.battle_won = False

    def draw(self):
        """绘制战斗场景"""
        # 绘制地图背景
        if self.tiled_scene:
            self.tiled_scene.render_map(self.screen, 0, 0)
        else:
            self.screen.fill((50, 50, 80))

        # 绘制敌人
        if self.enemy and self.enemy.is_alive:
            self.enemy.draw(self.screen)
            self._draw_entity_hp_bar(self.enemy)

        # 绘制玩家
        if self.player:
            self.player.debug_draw(self.screen, 0, 0)

        # 绘制HUD
        self._draw_hud()

        # 绘制波次信息
        self._draw_wave_info()

        # 绘制战斗结束提示
        if self.battle_over:
            self._draw_battle_end()

    def _draw_entity_hp_bar(self, entity):
        """绘制敌人头顶血条"""
        bar_width = 60
        bar_height = 6
        x = entity.pos_x + entity.width // 2 - bar_width // 2
        y = entity.pos_y - 15
        hp_ratio = max(0, entity.hp / entity.max_hp)
        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, int(bar_width * hp_ratio), bar_height))

    def _draw_hud(self):
        """绘制底部HUD"""
        hud_height = 60
        hud_y = SCREEN_HEIGHT - hud_height
        # 半透明背景
        hud_surface = pygame.Surface((SCREEN_WIDTH, hud_height), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 180))
        self.screen.blit(hud_surface, (0, hud_y))

        if not self.player:
            return

        # 血条
        bar_x, bar_y = 20, hud_y + 10
        bar_width, bar_height = 200, 20
        hp_ratio = max(0, self.player.hp / self.player.max_hp)
        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        hp_color = (0, 200, 0) if hp_ratio > 0.3 else (200, 0, 0)
        pygame.draw.rect(self.screen, hp_color, (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

        # HP文字
        hp_text = f"HP: {self.player.hp}/{self.player.max_hp}"
        hp_surface = self.hud_font.render(hp_text, True, (255, 255, 255))
        self.screen.blit(hp_surface, (bar_x + bar_width + 10, bar_y + 2))

        # 攻击力
        atk_text = f"ATK: {self.player.attack_power}"
        atk_surface = self.hud_font.render(atk_text, True, (255, 200, 0))
        self.screen.blit(atk_surface, (bar_x + bar_width + 140, bar_y + 2))

        # 波次计数 (右侧)
        wave_text = f"Wave: {self.current_wave}/{self.TOTAL_WAVES}"
        wave_surface = self.hud_font.render(wave_text, True, (200, 200, 255))
        self.screen.blit(wave_surface, (SCREEN_WIDTH - 180, bar_y + 2))

    def _draw_wave_info(self):
        """绘制波次信息"""
        if self.between_waves and not self.battle_over and self.current_wave < self.TOTAL_WAVES:
            text = f"第 {self.current_wave + 1} 波即将到来..."
            surface = self.font.render(text, True, (255, 255, 200))
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            bg = pygame.Surface(rect.inflate(20, 10).size, pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            self.screen.blit(bg, rect.inflate(20, 10).topleft)
            self.screen.blit(surface, rect)

    def _draw_battle_end(self):
        """绘制战斗结束提示"""
        if self.battle_won:
            text = "战斗胜利！"
            color = (255, 215, 0)
        else:
            text = "战斗失败..."
            color = (255, 100, 100)

        # 使用更大的字体
        try:
            big_font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 48)
        except (FileNotFoundError, pygame.error):
            big_font = pygame.font.SysFont('simhei', 48)

        surface = big_font.render(text, True, color)
        rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        bg = pygame.Surface(rect.inflate(20, 10).size, pygame.SRCALPHA)
        bg.fill((0, 0, 0, 200))
        self.screen.blit(bg, rect.inflate(20, 10).topleft)
        self.screen.blit(surface, rect)
