"""
唐僧 - 剧情角色
步骤14: 玩家与NPC碰撞交互
"""
import pygame
from .npc import NPCBase


class Tang(NPCBase):
    """
    唐僧
    剧情角色，可对话
    """

    def __init__(self, x, y):
        """
        初始化唐僧
        :param x: 初始x坐标
        :param y: 初始y坐标
        """
        super().__init__(x, y, 48, 68, speed=0)
        self._load_image()
        self._load_dialogs()

    def _load_image(self):
        """用代码绘制简笔唐僧"""
        self.image = pygame.Surface((48, 68), pygame.SRCALPHA)

        # 身体 - 金色袈裟
        pygame.draw.ellipse(self.image, (255, 200, 50), (8, 25, 32, 40))
        pygame.draw.ellipse(self.image, (220, 170, 30), (8, 25, 32, 40), 2)

        # 袈裟领口 - V字形
        pygame.draw.line(self.image, (180, 130, 20), (18, 28), (24, 45), 2)
        pygame.draw.line(self.image, (180, 130, 20), (30, 28), (24, 45), 2)

        # 头部 - 肤色
        pygame.draw.circle(self.image, (255, 220, 180), (24, 18), 12)
        pygame.draw.circle(self.image, (200, 160, 120), (24, 18), 12, 1)

        # 佛帽 - 红色小帽
        pygame.draw.ellipse(self.image, (200, 50, 50), (16, 2, 16, 10))
        pygame.draw.ellipse(self.image, (180, 30, 30), (16, 2, 16, 10), 1)
        # 帽顶装饰
        pygame.draw.circle(self.image, (255, 215, 0), (24, 4), 3)

        # 眼睛
        pygame.draw.circle(self.image, (50, 50, 50), (20, 17), 2)
        pygame.draw.circle(self.image, (50, 50, 50), (28, 17), 2)

        # 嘴巴 - 微笑
        pygame.draw.arc(self.image, (150, 80, 80), (19, 20, 10, 6), 3.14, 6.28, 1)

        # 脚 - 黑色僧鞋
        pygame.draw.ellipse(self.image, (60, 40, 30), (12, 62, 10, 6))
        pygame.draw.ellipse(self.image, (60, 40, 30), (26, 62, 10, 6))

    def _load_dialogs(self):
        """加载对话内容"""
        self.dialogs = [
            {"speaker": "唐僧", "text": "悟空，你来了。"},
            {"speaker": "唐僧", "text": "为师在此等候多时。"},
            {"speaker": "唐僧", "text": "听闻这观音院中藏有妖怪，"},
            {"speaker": "唐僧", "text": "偷走了为师的锦襕袈裟。"},
            {"speaker": "唐僧", "text": "你速去打探消息，找回袈裟。"},
            {"speaker": "唐僧", "text": "切记不可伤及无辜百姓。"},
            {"speaker": "唐僧", "text": "阿弥陀佛，善哉善哉。"},
        ]

    def update(self):
        """唐僧不移动"""
        pass

    def draw(self, surface):
        """绘制唐僧 - 居中显示"""
        if self.image:
            img_rect = self.image.get_rect()
            img_rect.center = self.rect.center
            surface.blit(self.image, img_rect)
