"""
场景管理器
步骤16-17: 渐变效果 + 场景切换
"""
import pygame
from utils.fade_scene import FadeScene, SceneStatus


class SceneManager:
    """
    场景管理器
    管理场景切换和更新，集成渐变效果
    """

    def __init__(self, screen, sound_system=None):
        """
        初始化场景管理器
        :param screen: 主屏幕surface
        :param sound_system: 音效系统
        """
        self.screen = screen
        self.sound_system = sound_system
        self.scenes = {}
        self.current_scene = None
        self.scene_stack = []
        self.fade_scene = None
        self.is_transitioning = False
        self.next_scene_name = None

    def add_scene(self, name, scene):
        """
        添加场景
        :param name: 场景名称
        :param scene: 场景对象
        """
        self.scenes[name] = scene

    def set_current_scene(self, name, use_fade=True):
        """
        设置当前场景
        :param name: 场景名称
        :param use_fade: 是否使用渐变效果
        """
        if name in self.scenes:
            if use_fade and self.current_scene:
                self._start_transition(name)
            else:
                if self.current_scene:
                    self.current_scene.on_exit()
                self.current_scene = self.scenes[name]
                if self.sound_system:
                    self.current_scene.sound_system = self.sound_system
                self.current_scene.on_enter()

    def _start_transition(self, next_name):
        """开始场景切换渐变"""
        self.is_transitioning = True
        self.next_scene_name = next_name

        current_surface = self.screen.copy()
        self.fade_scene = FadeScene(current_surface)
        self.fade_scene.set_status(SceneStatus.Out)

    def push_scene(self, name):
        """
        压入场景
        :param name: 场景名称
        """
        if name in self.scenes:
            if self.current_scene:
                self.scene_stack.append(self.current_scene)
                self.current_scene.on_exit()
            self.current_scene = self.scenes[name]
            self.current_scene.on_enter()

    def pop_scene(self):
        """弹出场景"""
        if self.scene_stack:
            self.current_scene.on_exit()
            self.current_scene = self.scene_stack.pop()
            self.current_scene.on_enter()

    def handle_events(self, events):
        """处理事件"""
        if self.current_scene and not self.is_transitioning:
            self.current_scene.handle_events(events)

    def update(self):
        """更新场景"""
        if self.is_transitioning and self.fade_scene:
            self.fade_scene.update()

            if self.fade_scene.get_out():
                self.current_scene.on_exit()
                self.current_scene = self.scenes[self.next_scene_name]
                self.current_scene.on_enter()
                self.fade_scene.set_status(SceneStatus.In)
                self.is_transitioning = False
                self.next_scene_name = None
        elif self.current_scene:
            self.current_scene.update()

    def draw(self):
        """绘制场景"""
        if self.current_scene:
            self.current_scene.draw()

        if self.is_transitioning and self.fade_scene:
            fade_surface = self.fade_scene.get_back_image(0, 0)
            if fade_surface:
                self.screen.blit(fade_surface, (0, 0))
