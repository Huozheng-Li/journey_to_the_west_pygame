"""
TMX地图渲染器
步骤4: pytmx库使用
"""
import pygame
import pytmx
from pytmx.util_pygame import load_pygame


class TiledScene:
    """
    TMX地图场景封装类
    负责加载和渲染Tiled地图
    """

    def __init__(self, tmx_path):
        """
        初始化TMX场景
        :param tmx_path: TMX文件路径
        """
        self.tmx_data = load_pygame(tmx_path)
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

    def render_map(self, surface, scroll_x=0, scroll_y=0):
        """
        渲染地图到surface
        :param surface: 目标surface
        :param scroll_x: X滚动偏移
        :param scroll_y: Y滚动偏移
        """
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self._render_tile_layer(surface, layer, scroll_x, scroll_y)
            elif isinstance(layer, pytmx.TiledImageLayer):
                self._render_image_layer(surface, layer, scroll_x, scroll_y)

    def _render_tile_layer(self, surface, layer, scroll_x, scroll_y):
        """渲染图块层"""
        for x, y, image in layer.tiles():
            if image:
                pos_x = x * self.tmx_data.tilewidth - scroll_x
                pos_y = y * self.tmx_data.tileheight - scroll_y
                surface.blit(image, (pos_x, pos_y))

    def _render_image_layer(self, surface, layer, scroll_x, scroll_y):
        """渲染图像层"""
        if layer.image:
            pos_x = getattr(layer, 'offsetx', 0) - scroll_x
            pos_y = getattr(layer, 'offsety', 0) - scroll_y
            surface.blit(layer.image, (pos_x, pos_y))

    def get_object_by_name(self, name):
        """
        根据名称获取对象层中的对象
        :param name: 对象名称
        :return: 对象列表
        """
        objects = []
        for obj in self.tmx_data.objects:
            if obj.name == name:
                objects.append(obj)
        return objects

    def get_objects_by_name_prefix(self, prefix):
        """
        根据名称前缀获取对象层中的对象
        :param prefix: 名称前缀 (如 'elder' 匹配 'elder1', 'elder2' 等)
        :return: 对象列表
        """
        objects = []
        for obj in self.tmx_data.objects:
            if obj.name and obj.name.startswith(prefix):
                objects.append(obj)
        return objects

    def get_objects_by_layer(self, layer_name):
        """
        根据图层名称获取该图层中所有对象
        :param layer_name: 图层名称
        :return: 对象列表
        """
        for layer in self.tmx_data.layers:
            if layer.name == layer_name and isinstance(layer, pytmx.TiledObjectGroup):
                return list(layer)
        return []

    def get_layer_by_name(self, name):
        """
        根据名称获取图层
        :param name: 图层名称
        :return: 图层对象
        """
        for layer in self.tmx_data.layers:
            if layer.name == name:
                return layer
        return None

    def get_map_size(self):
        """
        获取地图尺寸
        :return: (width, height) 像素单位
        """
        return self.map_width, self.map_height
