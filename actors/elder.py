"""
村民 - 背景NPC
步骤14: 玩家与NPC碰撞交互
"""
import pygame
from .npc import NPCBase
from .action import Action


class Elder(NPCBase):
    """
    村民NPC
    可以对话的背景角色
    """

    def __init__(self, x, y, elder_type=1):
        """
        初始化村民
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param elder_type: 村民类型 (1-4)
        """
        self.elder_type = elder_type
        frame_counts = {1: 10, 2: 6, 3: 7, 4: 10}
        super().__init__(x, y, 48, 68, speed=1)
        self.animations = {}
        self._load_animations(frame_counts.get(elder_type, 10))
        self.sync_rect_to_image()
        self._load_dialogs()

    def _load_animations(self, frame_count):
        """加载动画"""
        self.animations = {
            self.DOWN: Action(f'elder', f'elder{self.elder_type}-', frame_count, True, start_index=0),
        }
        if self.DOWN in self.animations:
            self.image = self.animations[self.DOWN].get_current_image()

    def _load_dialogs(self):
        """加载对话内容"""
        self.dialogs = [
            {"speaker": "村民", "text": "欢迎来到村庄！"},
        ]

    def update(self):
        """更新村民状态"""
        self._update_animation()

    def _update_animation(self):
        """更新动画帧 - Elder只有一个方向的动画"""
        if self.DOWN in self.animations:
            action = self.animations[self.DOWN]
            self.image = action.get_current_image()
        elif self.direction in self.animations:
            action = self.animations[self.direction]
            self.image = action.get_current_image()

    def draw(self, surface):
        """绘制村民"""
        if self.image:
            surface.blit(self.image, self.rect)
