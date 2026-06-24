"""
土地公 - 剧情NPC
步骤14: 玩家与NPC碰撞交互
"""
import pygame
from .npc import NPCBase
from .action import Action


class God(NPCBase):
    """
    土地公
    触发剧情对话的NPC
    """

    def __init__(self, x, y):
        """
        初始化土地公
        :param x: 初始x坐标
        :param y: 初始y坐标
        """
        super().__init__(x, y, 48, 68, speed=2)
        self.animations = {}
        self._load_animations()
        self.sync_rect_to_image()
        self._load_dialogs()
        self.player_stats = None  # 玩家属性引用

    def _load_animations(self):
        """加载4方向动画 - 40帧: 下(00000-00009), 左(01000-01009), 上(02000-02009), 右(03000-03009)"""
        self.animations = {
            self.DOWN: Action('god', '0214-16505471-', 10, True, start_index=0),
            self.LEFT: Action('god', '0214-16505471-', 10, True, start_index=1000),
            self.UP: Action('god', '0214-16505471-', 10, True, start_index=2000),
            self.RIGHT: Action('god', '0214-16505471-', 10, True, start_index=3000),
        }
        if self.DOWN in self.animations:
            self.image = self.animations[self.DOWN].get_current_image()

    def _load_dialogs(self):
        """加载对话内容"""
        self.dialogs = [
            {"speaker": "土地公", "text": "施主可是孙悟空？"},
            {"speaker": "土地公", "text": "贫僧知道袈裟在何处。"},
            {"speaker": "土地公", "text": "请随我来，去观音院找回袈裟。"},
        ]
        # 鼓励对话（战斗失败后）
        self.encourage_dialogs = [
            {"speaker": "土地公", "text": "施主不必气馁。"},
            {"speaker": "土地公", "text": "老夫观你骨骼精奇，日后必成大器。"},
            {"speaker": "土地公", "text": "去找村民和唐僧修炼一番，定能战胜妖怪！"},
            {"speaker": "土地公", "text": "记住，失败乃成功之母。"},
        ]

    def get_dialog(self):
        """
        获取当前对话
        :return: 对话内容
        """
        if self.dialogs and self.dialog_index < len(self.dialogs):
            return self.dialogs[self.dialog_index]
        return None

    def get_encourage_dialog(self):
        """
        获取鼓励对话（战斗失败后自动触发）
        :return: 对话内容
        """
        if self.dialog_index < len(self.encourage_dialogs):
            return self.encourage_dialogs[self.dialog_index]
        return None

    def next_dialog(self):
        """下一条对话"""
        if self.dialog_index < len(self.dialogs) - 1:
            self.dialog_index += 1
            return True
        return False

    def next_encourage_dialog(self):
        """下一条鼓励对话"""
        if self.dialog_index < len(self.encourage_dialogs) - 1:
            self.dialog_index += 1
            return True
        return False

    def update(self):
        """更新土地公状态"""
        self.auto_move()
        self._update_animation()

    def _update_animation(self):
        """更新动画帧"""
        if self.direction in self.animations:
            action = self.animations[self.direction]
            self.image = action.get_current_image()

    def draw(self, surface):
        """绘制土地公"""
        if self.image:
            surface.blit(self.image, self.rect)
