"""
村庄场景
步骤5-17: TMX地图 + 角色 + NPC + 对话 + 场景切换
"""
import pygame
import os
from .base_scene import SceneBase
from utils.tiled_render import TiledScene
from actors.player import Player
from actors.god import God
from actors.elder import Elder
from actors.tang import Tang
from systems.dialog import DialogSystem
from config import TMX_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_DIR, DRAW_ROAD_EDGE


class PolygonArea:
    """多边形可行走区域，支持 colliderect 检测（点-in-多边形）"""
    def __init__(self, points):
        self.points = points  # [(x,y), ...]

    def colliderect(self, rect):
        """检查矩形中心点是否在多边形内"""
        cx, cy = rect.centerx, rect.centery
        return self._point_in_polygon(cx, cy)

    def __getattr__(self, name):
        """提供 x, y, width, height 属性以兼容 pygame.Rect 接口"""
        if name == 'x':
            return min(p[0] for p in self.points)
        elif name == 'y':
            return min(p[1] for p in self.points)
        elif name == 'width':
            return max(p[0] for p in self.points) - min(p[0] for p in self.points)
        elif name == 'height':
            return max(p[1] for p in self.points) - min(p[1] for p in self.points)
        raise AttributeError(name)

    def _point_in_polygon(self, x, y):
        """射线法判断点是否在多边形内"""
        n = len(self.points)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = self.points[i]
            xj, yj = self.points[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside


class VillageScene(SceneBase):
    """
    村庄场景
    加载village1.tmx地图和角色
    """

    def __init__(self, screen, player_stats=None):
        super().__init__(screen)
        self.player_stats = player_stats
        self.tiled_scene = TiledScene(f"{TMX_DIR}/village.tmx")
        self.scroll_x = 0
        self.scroll_y = 0
        self.map_width, self.map_height = self.tiled_scene.get_map_size()

        self.obstacles = self._load_obstacles()
        self.npcs = self._load_npcs()
        self.player = self._load_player()
        self.walkable_areas = self._load_walkable_areas()
        self._snap_player_to_road()
        self.dialog_system = DialogSystem()
        self.current_npc = None
        self.next_scene = None
        self.nearby_npc = None
        self.is_auto_encourage = False  # 是否为自动鼓励对话
        self.hint_font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 16)

    def on_enter(self):
        super().on_enter()
        if self.sound_system:
            self.sound_system.play_music('bgm', loop=True, force_restart=True)
        # 战斗失败后自动触发土地公对话
        if self.player_stats and self.player_stats.has_been_to_battle and not self.player_stats.last_battle_won:
            self._auto_talk_to_god()

    def _load_obstacles(self):
        obstacles = []
        for obj in self.tiled_scene.get_objects_by_layer('obstacle'):
            if obj.width > 0 and obj.height > 0:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                obstacles.append(rect)
        return obstacles

    def _load_walkable_areas(self):
        areas = []
        for obj in self.tiled_scene.get_objects_by_layer('road'):
            if hasattr(obj, 'points') and obj.points:
                # 多边形区域：保存顶点用于点-in-多边形检测，闭合多边形
                pts = [(p.x, p.y) for p in obj.points]
                if pts[0] != pts[-1]:
                    pts.append(pts[0])
                areas.append(PolygonArea(pts))
            elif obj.width > 0 and obj.height > 0:
                # 矩形区域：兜底
                areas.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        return areas

    def _snap_player_to_road(self):
        """确保玩家起始位置在某个可行走多边形内"""
        col = self.player.get_col_rect()
        for area in self.walkable_areas:
            if isinstance(area, PolygonArea) and area.colliderect(col):
                return
        poly_areas = [a for a in self.walkable_areas if isinstance(a, PolygonArea)]
        if not poly_areas:
            return
        best_dist = float('inf')
        best_center = None
        for area in poly_areas:
            cx = sum(p[0] for p in area.points) / len(area.points)
            cy = sum(p[1] for p in area.points) / len(area.points)
            dist = ((col.centerx - cx)**2 + (col.centery - cy)**2)**0.5
            if dist < best_dist:
                best_dist = dist
                best_center = (cx, cy)
        if best_center:
            self.player.set_position(best_center[0] - self.player.width // 2,
                                     best_center[1] - self.player.height // 2)

    def _load_npcs(self):
        npcs = []
        god_objects = self.tiled_scene.get_object_by_name('god')
        for obj in god_objects:
            god = God(obj.x, obj.y)
            god.player_stats = self.player_stats
            npcs.append(god)
        elder_objects = self.tiled_scene.get_objects_by_name_prefix('elder')
        for i, obj in enumerate(elder_objects):
            elder_type = (i % 4) + 1
            npcs.append(Elder(obj.x, obj.y, elder_type))
        tang_objects = self.tiled_scene.get_object_by_name('tang')
        for obj in tang_objects:
            npcs.append(Tang(obj.x, obj.y))
        return npcs

    def _load_player(self):
        player_objects = self.tiled_scene.get_object_by_name('sun')
        if player_objects:
            obj = player_objects[0]
            return Player(obj.x, obj.y, self.map_width, self.map_height)
        return Player(100, 100, self.map_width, self.map_height)

    def handle_events(self, events):
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
                            # 根据对话类型使用不同的next_dialog方法
                            if self.is_auto_encourage and isinstance(self.current_npc, God):
                                has_next = self.current_npc.next_encourage_dialog()
                            else:
                                has_next = self.current_npc.next_dialog()

                            if not has_next:
                                self.dialog_system.end_dialog()
                                self.player.is_talking = False
                                self.is_auto_encourage = False
                                # NPC交互属性加成
                                if isinstance(self.current_npc, Elder):
                                    if self.player_stats and self.player_stats.add_elder_hp():
                                        self._show_bonus_notification(f"HP +{self.player_stats.ELDER_HP_BONUS}!")
                                    self.current_npc.reset_dialog()
                                elif isinstance(self.current_npc, Tang):
                                    if self.player_stats and self.player_stats.add_tang_attack():
                                        self._show_bonus_notification(f"ATK +{self.player_stats.TANG_ATTACK_BONUS}!")
                                    self.current_npc.reset_dialog()
                                elif isinstance(self.current_npc, God):
                                    self.current_npc.reset_dialog()
                                    self.next_scene = 'temple'
                                self.current_npc = None
                            else:
                                # 获取下一条对话
                                if self.is_auto_encourage and isinstance(self.current_npc, God):
                                    dialog = self.current_npc.get_encourage_dialog()
                                else:
                                    dialog = self.current_npc.get_dialog()
                                self.dialog_system.start_dialog(dialog)
                    else:
                        self._check_npc_collision()

    def _check_npc_collision(self):
        player_rect = self.player.get_col_rect()
        for npc in self.npcs:
            npc_rect = npc.get_rect().inflate(20, 20)
            if player_rect.colliderect(npc_rect):
                dialog = npc.get_dialog()
                if dialog:
                    self.current_npc = npc
                    self.player.is_talking = True
                    self.dialog_system.start_dialog(dialog)
                    break

    def _auto_talk_to_god(self):
        """自动与土地公对话（战斗失败后）"""
        for npc in self.npcs:
            if isinstance(npc, God):
                self.current_npc = npc
                self.player.is_talking = True
                self.is_auto_encourage = True  # 标记为自动鼓励对话
                dialog = npc.get_encourage_dialog()
                if dialog:
                    self.dialog_system.start_dialog(dialog)
                break

    def update(self):
        if not self.dialog_system.is_dialog_active:
            keys = pygame.key.get_pressed()
            npc_rects = [npc.get_rect() for npc in self.npcs if npc is not self.current_npc]
            # 所有可行走区域都传给player（包括多边形）
            self.player.update(keys, self.obstacles + npc_rects, self.walkable_areas)
            for npc in self.npcs:
                npc.update()
            self._update_nearby_npc()
        else:
            self.nearby_npc = None
        self._update_camera()

    def _update_nearby_npc(self):
        player_rect = self.player.get_col_rect()
        self.nearby_npc = None
        for npc in self.npcs:
            npc_rect = npc.get_rect().inflate(20, 20)
            if player_rect.colliderect(npc_rect):
                self.nearby_npc = npc
                break

    def _update_camera(self):
        player_x, player_y = self.player.get_position()
        self.scroll_x = player_x - SCREEN_WIDTH // 2
        self.scroll_y = player_y - SCREEN_HEIGHT // 2

        self.scroll_x = max(0, min(self.scroll_x, self.map_width - SCREEN_WIDTH))
        self.scroll_y = max(0, min(self.scroll_y, self.map_height - SCREEN_HEIGHT))

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

    def _show_bonus_notification(self, text):
        """显示属性加成通知"""
        self._notification_text = text
        self._notification_timer = 120  # 显示3秒 (40FPS)

    def _draw_notification(self):
        """绘制属性加成通知"""
        if hasattr(self, '_notification_timer') and self._notification_timer > 0:
            self._notification_timer -= 1
            font = pygame.font.Font(os.path.join(FONT_DIR, 'newfont.TTF'), 28)
            surface = font.render(self._notification_text, True, (255, 255, 0))
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            bg = pygame.Surface(rect.inflate(20, 10).size, pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            self.screen.blit(bg, rect.inflate(20, 10).topleft)
            self.screen.blit(surface, rect)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.tiled_scene.render_map(self.screen, self.scroll_x, self.scroll_y)

        if DRAW_ROAD_EDGE:
            for area in self.walkable_areas:
                if isinstance(area, PolygonArea):
                    # 多边形绘制
                    screen_pts = [(p[0] - self.scroll_x, p[1] - self.scroll_y) for p in area.points]
                    s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                    pygame.draw.polygon(s, (0, 255, 0, 60), screen_pts)
                    self.screen.blit(s, (0, 0))
                    pygame.draw.polygon(self.screen, (0, 255, 0), screen_pts, 1)
                else:
                    # 矩形绘制
                    screen_rect = pygame.Rect(area.x - self.scroll_x, area.y - self.scroll_y,
                                              area.width, area.height)
                    s = pygame.Surface((screen_rect.width, screen_rect.height), pygame.SRCALPHA)
                    s.fill((0, 255, 0, 60))
                    self.screen.blit(s, screen_rect.topleft)
                    pygame.draw.rect(self.screen, (0, 255, 0), screen_rect, 1)
            for obs in self.obstacles:
                screen_rect = pygame.Rect(obs.x - self.scroll_x, obs.y - self.scroll_y,
                                          obs.width, obs.height)
                s = pygame.Surface((screen_rect.width, screen_rect.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 60))
                self.screen.blit(s, screen_rect.topleft)
                pygame.draw.rect(self.screen, (255, 0, 0), screen_rect, 1)

        for npc in self.npcs:
            npc.debug_draw(self.screen, self.scroll_x, self.scroll_y)

        self.player.debug_draw(self.screen, self.scroll_x, self.scroll_y)

        if self.nearby_npc and not self.dialog_system.is_dialog_active:
            screen_x = self.player.pos_x - self.scroll_x
            screen_y = self.player.pos_y - self.scroll_y
            self._draw_hint("按空格键发起对话", screen_x, screen_y)

        self.dialog_system.draw(self.screen)
        self._draw_notification()
