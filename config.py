"""
全局配置文件 - 西游记观音院
"""
import os

# 窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 40
GAME_TITLE = "西游记观音院"

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, 'resource')
IMG_DIR = os.path.join(RESOURCE_DIR, 'img')
TMX_DIR = os.path.join(RESOURCE_DIR, 'tmx')
FONT_DIR = os.path.join(RESOURCE_DIR, 'font')
SOUND_DIR = os.path.join(RESOURCE_DIR, 'sound')

# 地图配置
MAP_WIDTH = 3780
MAP_HEIGHT = 2395

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FALLBACK_BG_COLOR = (100, 149, 237)  # Cornflower blue
