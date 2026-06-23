"""
村庄场景
步骤5-17: TMX地图 + 角色 + NPC + 对话 + 场景切换
"""
import pygame
from .base_scene import SceneBase
from utils.tiled_render import TiledScene
from actors.player import Player
from actors.god import God
from actors.elder import Elder
from actors.tang import Tang
from systems.dialog import DialogSystem
from config import TMX_DIR, SCREEN_WIDTH, SCREEN_HEIGHT


class VillageScene(SceneBase):
    """
    村庄场景
    加载village1.tmx地图和角色
    """

    def __init__(self, screen):
        """
        初始化村庄场景
        :param screen: 主屏幕surface
        """
        super().__init__(screen)
        self.tiled_scene = TiledScene(f"{TMX_DIR}/village1.tmx")
        self.scroll_x = 0
        self.scroll_y = 0
        self.map_width, self.map_height = self.tiled_scene.get_map_size()

        self.obstacles = self._load_obstacles()
        self.npcs = self._load_npcs()
        self.player = self._load_player()
        self.dialog_system = DialogSystem()
        self.current_npc = None
        self.next_scene = None

    def on_enter(self):
        """进入村庄场景"""
        super().on_enter()
        if self.sound_system:
            self.sound_system.play_music('aigei', loop=True)

    def _load_obstacles(self):
        """从TMX加载障碍物"""
        obstacles = []
        for obj in self.tiled_scene.get_object_by_name('obstacle'):
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            obstacles.append(rect)
        return obstacles

    def _load_npcs(self):
        """从TMX加载NPC"""
        npcs = []

        god_objects = self.tiled_scene.get_object_by_name('god')
        for obj in god_objects:
            npcs.append(God(obj.x, obj.y))

        elder_objects = self.tiled_scene.get_object_by_name('elder')
        for i, obj in enumerate(elder_objects):
            elder_type = (i % 4) + 1
            npcs.append(Elder(obj.x, obj.y, elder_type))

        tang_objects = self.tiled_scene.get_object_by_name('tang')
        for obj in tang_objects:
            npcs.append(Tang(obj.x, obj.y))

        return npcs

    def _load_player(self):
        """从TMX加载玩家位置"""
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
                    if self.dialog_system.is_dialog_active:
                        self.dialog_system.end_dialog()
                        self.player.is_talking = False
                    else:
                        self.is_active = False
                elif event.key == pygame.K_SPACE:
                    if self.dialog_system.is_dialog_active:
                        if self.current_npc:
                            if not self.current_npc.next_dialog():
                                self.dialog_system.end_dialog()
                                self.player.is_talking = False
                                if isinstance(self.current_npc, God):
                                    self.current_npc.reset_dialog()
                                    self.next_scene = 'temple'
                                self.current_npc = None
                            else:
                                self.dialog_system.start_dialog(self.current_npc.get_dialog())
                    else:
                        self._check_npc_collision()

    def _check_npc_collision(self):
        """检查与NPC碰撞"""
        player_rect = self.player.get_rect()
        for npc in self.npcs:
            if player_rect.colliderect(npc.get_rect()):
                dialog = npc.get_dialog()
                if dialog:
                    self.current_npc = npc
                    self.player.is_talking = True
                    self.dialog_system.start_dialog(dialog)
                    break

    def update(self):
        """更新场景"""
        if not self.dialog_system.is_dialog_active:
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.obstacles)
        self._update_camera()

    def _update_camera(self):
        """更新相机位置"""
        player_x, player_y = self.player.get_position()
        self.scroll_x = player_x - SCREEN_WIDTH // 2
        self.scroll_y = player_y - SCREEN_HEIGHT // 2

        self.scroll_x = max(0, min(self.scroll_x, self.map_width - SCREEN_WIDTH))
        self.scroll_y = max(0, min(self.scroll_y, self.map_height - SCREEN_HEIGHT))

    def draw(self):
        """绘制村庄场景"""
        self.screen.fill((0, 0, 0))
        self.tiled_scene.render_map(self.screen, self.scroll_x, self.scroll_y)

        for npc in self.npcs:
            screen_x = npc.pos_x - self.scroll_x
            screen_y = npc.pos_y - self.scroll_y
            self.screen.blit(npc.image, (screen_x, screen_y))

        screen_x = self.player.pos_x - self.scroll_x
        screen_y = self.player.pos_y - self.scroll_y
        self.screen.blit(self.player.image, (screen_x, screen_y))

        self.dialog_system.draw(self.screen)
