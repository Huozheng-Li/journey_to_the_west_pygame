"""
西游记观音院 - 主程序入口
基于Pygame的RPG游戏
"""
import os
import sys
import pygame
from pygame.constants import QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT

from scene import TiledScene
from actor.farmer import Farmer
from actor.player import Player

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Game:
    """
    游戏主类
    """

    def __init__(self):
        """
        游戏初始化
        """
        pygame.init()
        pygame.mixer.init()

        # 设置窗口
        self.screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('西游记 - 观音院')

        # 加载场景
        self.current_scene = None
        self.scenes = {}
        self.init_scenes()

        # 创建玩家
        self.player = None
        self.init_player()

        # 时钟
        self.clock = pygame.time.Clock()

    def init_scenes(self):
        """
        初始化场景
        """
        # 村庄场景
        village_path = os.path.join(BASE_DIR, "resource", "tmx", "village.tmx")
        self.scenes['village'] = TiledScene(village_path, self.screen)

        # 寺庙场景
        temple_path = os.path.join(BASE_DIR, "resource", "tmx", "temple.tmx")
        self.scenes['temple'] = TiledScene(temple_path, self.screen)

        # 设置初始场景
        self.current_scene = self.scenes['village']

    def init_player(self):
        """
        初始化玩家角色
        """
        # 从场景对象层获取玩家位置，或使用默认位置
        self.player = Player(400, 300)

    def run(self):
        """
        游戏主循环
        """
        print("游戏主循环开始")  # 调试
        running = True

        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # 使用键盘状态检测（支持持续按键）- 方向键控制
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.player.move_up()
            elif keys[K_DOWN]:
                self.player.move_down()
            elif keys[K_LEFT]:
                self.player.move_left()
            elif keys[K_RIGHT]:
                self.player.move_right()

            # 更新玩家位置
            self.player.update()

            # 清除屏幕
            self.screen.fill((0, 0, 0))

            # 绘制场景
            self.current_scene.draw()

            # 绘制玩家到屏幕
            self.player.draw(self.screen)

            # 更新显示
            pygame.display.update()
            self.clock.tick(40)

        print("游戏主循环结束")  # 调试
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
