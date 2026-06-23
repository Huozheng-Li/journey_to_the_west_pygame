"""
寺庙场景
步骤17-22: 第二个场景 + 战斗触发
"""
import pygame
from .base_scene import SceneBase
from utils.tiled_render import TiledScene
from actors.player import Player
from config import TMX_DIR, SCREEN_WIDTH, SCREEN_HEIGHT


class TempleScene(SceneBase):
    """
    寺庙场景
    加载temple.tmx地图，触发战斗
    """

    def __init__(self, screen):
        """
        初始化寺庙场景
        :param screen: 主屏幕surface
        """
        super().__init__(screen)
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
        self.battle_trigger_x = self.map_width // 2
        self.battle_trigger_y = self.map_height // 2

    def on_enter(self):
        """进入寺庙场景"""
        super().on_enter()
        if self.sound_system:
            self.sound_system.play_music('nmw', loop=True)

    def _load_obstacles(self):
        """从TMX加载障碍物"""
        obstacles = []
        if self.tiled_scene:
            for obj in self.tiled_scene.get_object_by_name('obstacle'):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                obstacles.append(rect)
        return obstacles

    def _load_player(self):
        """从TMX加载玩家位置"""
        if self.tiled_scene:
            player_objects = self.tiled_scene.get_object_by_name('sun')
            if player_objects:
                obj = player_objects[0]
                return Player(obj.x, obj.y, self.map_width, self.map_height)
        return Player(100, 100, self.map_width, self.map_height)

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False

    def update(self):
        """更新场景"""
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.obstacles)
        self._update_camera()
        self._check_battle_trigger()

    def _check_battle_trigger(self):
        """检查战斗触发"""
        player_x, player_y = self.player.get_position()
        distance = ((player_x - self.battle_trigger_x) ** 2 +
                   (player_y - self.battle_trigger_y) ** 2) ** 0.5
        if distance < 50:
            self.next_scene = 'battle'

    def _update_camera(self):
        """更新相机位置"""
        player_x, player_y = self.player.get_position()
        self.scroll_x = player_x - SCREEN_WIDTH // 2
        self.scroll_y = player_y - SCREEN_HEIGHT // 2

        self.scroll_x = max(0, min(self.scroll_x, self.map_width - SCREEN_WIDTH))
        self.scroll_y = max(0, min(self.scroll_y, self.map_height - SCREEN_HEIGHT))

    def draw(self):
        """绘制寺庙场景"""
        self.screen.fill((0, 0, 0))
        if self.tiled_scene:
            self.tiled_scene.render_map(self.screen, self.scroll_x, self.scroll_y)

        screen_x = self.player.pos_x - self.scroll_x
        screen_y = self.player.pos_y - self.scroll_y
        self.screen.blit(self.player.image, (screen_x, screen_y))
