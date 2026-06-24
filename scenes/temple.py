"""
寺庙场景
步骤17-22: 第二个场景 + 战斗触发
"""
import pygame
import os
from .base_scene import SceneBase
from utils.tiled_render import TiledScene
from actors.player import Player
from actors.enemy import Cattle
from config import TMX_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR


class TempleScene(SceneBase):
    """
    寺庙场景
    加载temple.tmx地图，触发战斗
    """

    def __init__(self, screen, player_stats=None):
        super().__init__(screen)
        self.player_stats = player_stats
        try:
            self.tiled_scene = TiledScene(f"{TMX_DIR}/temple.tmx")
        except (FileNotFoundError, pygame.error):
            self.tiled_scene = None
        self.scroll_x = 0
        self.scroll_y = 0
        if self.tiled_scene:
            self.map_width, self.map_height = self.tiled_scene.get_map_size()
        else:
            self.map_width, self.map_height = 800, 600

        self.obstacles = self._load_obstacles()
        self.player = self._load_player()
        self.walkable_areas = self._load_walkable_areas()
        self.battle_trigger_x = self.map_width // 2
        self.battle_trigger_y = self.map_height // 2
        self.monster = Cattle(self.battle_trigger_x, self.battle_trigger_y)
        self.nearby_monster = False
        self.hint_font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 16)

    def on_enter(self):
        super().on_enter()
        if self.sound_system:
            self.sound_system.play_music('bgm', loop=True, force_restart=True)

    def _load_obstacles(self):
        obstacles = []
        if self.tiled_scene:
            for obj in self.tiled_scene.get_objects_by_layer('actor'):
                if obj.width > 0 and obj.height > 0:
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    obstacles.append(rect)
        return obstacles

    def _load_walkable_areas(self):
        areas = []
        if self.tiled_scene:
            expand_x = self.player.width // 2
            expand_y = self.player.height // 2
            for obj in self.tiled_scene.get_objects_by_layer('road'):
                if obj.width > 0 and obj.height > 0:
                    rect = pygame.Rect(
                        obj.x - expand_x, obj.y - expand_y,
                        obj.width + expand_x * 2, obj.height + expand_y * 2
                    )
                    areas.append(rect)
        return areas

    def _load_player(self):
        if self.tiled_scene:
            player_objects = self.tiled_scene.get_object_by_name('sun')
            if player_objects:
                obj = player_objects[0]
                return Player(obj.x, obj.y, self.map_width, self.map_height)
        return Player(100, 100, self.map_width, self.map_height)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
                elif event.key == pygame.K_SPACE and self.nearby_monster:
                    self.next_scene = 'battle'

    def update(self):
        keys = pygame.key.get_pressed()
        all_obstacles = self.obstacles + [self.monster.get_rect()]
        self.player.update(keys, all_obstacles, self.walkable_areas)
        self.monster.update()
        self._update_camera()
        self._update_nearby_monster()

    def _update_nearby_monster(self):
        player_rect = self.player.get_col_rect()
        monster_rect = self.monster.get_rect().inflate(40, 40)
        self.nearby_monster = player_rect.colliderect(monster_rect)

    def _update_camera(self):
        player_x, player_y = self.player.get_position()
        self.scroll_x = player_x - SCREEN_WIDTH // 2
        self.scroll_y = player_y - SCREEN_HEIGHT // 2

        self.scroll_x = max(0, min(self.scroll_x, self.map_width - SCREEN_WIDTH))
        self.scroll_y = max(0, min(self.scroll_y, self.map_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.tiled_scene:
            self.tiled_scene.render_map(self.screen, self.scroll_x, self.scroll_y)

        self.monster.debug_draw(self.screen, self.scroll_x, self.scroll_y)

        self.player.debug_draw(self.screen, self.scroll_x, self.scroll_y)

        if self.nearby_monster:
            screen_x = self.player.pos_x - self.scroll_x
            screen_y = self.player.pos_y - self.scroll_y
            self._draw_hint("按空格键发起战斗", screen_x, screen_y)

    def _draw_hint(self, text, player_x, player_y):
        hint_surface = self.hint_font.render(text, True, (255, 255, 200))
        hint_rect = hint_surface.get_rect()
        bg_rect = hint_rect.inflate(10, 6)
        bg_x = player_x + 24 - bg_rect.width // 2
        bg_y = player_y - 30
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 160))
        self.screen.blit(bg_surface, (bg_x, bg_y))
        self.screen.blit(hint_surface, (bg_x + 5, bg_y + 3))
