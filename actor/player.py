"""
玩家角色模块 - 孙悟空
"""
import os
import pygame


class Player(pygame.sprite.Sprite):
    """
    玩家角色类（孙悟空）
    """

    # 方向常量
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, pos_x, pos_y):
        """
        初始化玩家角色
        :param pos_x: 初始x位置
        :param pos_y: 初始y位置
        """
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 120
        self.height = 120
        self.speed = 4

        # 当前方向和帧索引
        self.direction = self.DOWN
        self.frame_index = 0
        self.frame_count = 4  # 每个方向4帧

        # 加载各方向的动画帧
        self.images = {
            self.DOWN: [],
            self.LEFT: [],
            self.UP: [],
            self.RIGHT: []
        }
        self.load_images()

        # 当前图像
        if self.images[self.direction]:
            self.image = self.images[self.direction][self.frame_index]
        else:
            # 如果没有图像，创建一个默认的
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))  # 红色方块作为占位
        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)

    def load_images(self):
        """
        加载玩家各方向的动画帧
        """
        # 获取项目根目录 - 使用多种方式确保路径正确
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        project_root = os.path.dirname(current_dir)
        base_path = os.path.join(project_root, 'resource', 'img', 'swk')

        print(f"Loading images from: {base_path}")  # 调试输出

        # 各方向的文件前缀
        prefixes = {
            self.DOWN: '00',   # 向下
            self.LEFT: '01',   # 向左
            self.UP: '02',     # 向上
            self.RIGHT: '03'   # 向右
        }

        for direction, prefix in prefixes.items():
            for i in range(self.frame_count):
                # 文件名格式: 00000.tga, 00001.tga, ... (5位数字)
                filename = f"{prefix}{i:03d}.tga"
                img_path = os.path.join(base_path, filename)
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (self.width, self.height))
                    self.images[direction].append(img)
                else:
                    print(f"File not found: {img_path}")  # 调试输出

    def move_up(self):
        """向上移动"""
        self.direction = self.UP
        self.pos_y -= self.speed

    def move_down(self):
        """向下移动"""
        self.direction = self.DOWN
        self.pos_y += self.speed

    def move_left(self):
        """向左移动"""
        self.direction = self.LEFT
        self.pos_x -= self.speed

    def move_right(self):
        """向右移动"""
        self.direction = self.RIGHT
        self.pos_x += self.speed

    def update(self):
        """
        更新玩家状态（动画帧）
        """
        # 更新动画帧
        if self.images[self.direction]:
            self.frame_index = (self.frame_index + 1) % len(self.images[self.direction])
            self.image = self.images[self.direction][self.frame_index]

        # 更新rect位置
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    def draw(self, surface):
        """
        绘制玩家
        :param surface: 目标surface
        """
        surface.blit(self.image, (self.pos_x, self.pos_y))
