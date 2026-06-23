"""
场景基类
步骤5: TMX地图封装
"""
import pygame


class SceneBase:
    """
    场景基类
    所有场景的父类，定义通用接口
    """

    def __init__(self, screen):
        """
        初始化场景
        :param screen: 主屏幕surface
        """
        self.screen = screen
        self.is_active = True
        self.next_scene = None
        self.sound_system = None

    def handle_events(self, events):
        """
        处理事件
        :param events: 事件列表
        """
        pass

    def update(self):
        """更新场景状态"""
        pass

    def draw(self):
        """绘制场景"""
        pass

    def on_enter(self):
        """进入场景时调用"""
        self.is_active = True
        self.next_scene = None

    def on_exit(self):
        """退出场景时调用"""
        self.is_active = False
