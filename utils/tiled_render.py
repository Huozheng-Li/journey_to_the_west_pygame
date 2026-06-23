"""
Tiled地图渲染工具类
基于pytmx库实现TMX地图的渲染
"""
import os
import pygame
import pytmx


class TiledRenderer:
    """
    Tiled地图渲染类
    用于加载和渲染TMX格式的地图文件
    """

    def __init__(self, tmx_path):
        """
        初始化渲染器
        :param tmx_path: TMX地图文件路径
        """
        self.tmx_path = tmx_path
        self.tmx_data = pytmx.load_pygame(tmx_path)

        # 获取地图尺寸（像素）
        self.pixel_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.pixel_height = self.tmx_data.height * self.tmx_data.tileheight
        self.pixel_size = (self.pixel_width, self.pixel_height)

        # 地图基本信息
        self.map_width = self.tmx_data.width
        self.map_height = self.tmx_data.height
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

    def render_map(self, surface):
        """
        渲染整个地图到指定的surface
        :param surface: 目标surface
        """
        # 遍历所有图层进行渲染
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tile_layer(surface, layer)
            elif isinstance(layer, pytmx.TiledImageLayer):
                self.render_image_layer(surface, layer)

    def render_tile_layer(self, surface, layer):
        """
        渲染瓦格图层
        :param surface: 目标surface
        :param layer: 瓦格图层
        """
        for x, y, gid in layer:
            tile = self.tmx_data.get_tile_image_by_gid(gid)
            if tile:
                # 计算瓦格位置
                px = x * self.tile_width
                py = y * self.tile_height
                surface.blit(tile, (px, py))

    def render_image_layer(self, surface, layer):
        """
        渲染图像图层
        :param surface: 目标surface
        :param layer: 图像图层
        """
        if layer.image:
            surface.blit(layer.image, (0, 0))

    def get_object_layer(self, layer_name):
        """
        获取指定名称的对象层
        :param layer_name: 对象层名称
        :return: 对象列表
        """
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == layer_name:
                return layer
        return None

    def get_objects_by_name(self, name):
        """
        根据名称获取对象
        :param name: 对象名称
        :return: 对象列表
        """
        objects = []
        for obj in self.tmx_data.objects:
            if obj.name == name:
                objects.append(obj)
        return objects

    def get_tile_at(self, x, y):
        """
        获取指定位置的瓦格
        :param x: 瓦格x坐标
        :param y: 瓦格y坐标
        :return: 瓦格GID
        """
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.tmx_data.get_gid(x, y)
        return None

    def is_blocked(self, x, y):
        """
        检查指定位置是否被阻挡
        :param x: 像素x坐标
        :param y: 像素y坐标
        :return: 是否被阻挡
        """
        # 转换为瓦格坐标
        tile_x = int(x // self.tile_width)
        tile_y = int(y // self.tile_height)

        # 检查障碍物对象层
        obstacles = self.get_object_layer('障碍物')
        if obstacles:
            for obj in obstacles:
                if hasattr(obj, 'width') and hasattr(obj, 'height'):
                    if (obj.x <= x <= obj.x + obj.width and
                        obj.y <= y <= obj.y + obj.height):
                        return True

        return False
