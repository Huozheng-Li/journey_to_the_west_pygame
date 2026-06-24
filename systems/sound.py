"""
音效系统
步骤23: 声音和音效
支持渐弱切歌
"""
import pygame
from config import SOUND_DIR


class SoundSystem:
    """
    音效系统
    管理背景音乐和音效
    """

    def __init__(self):
        """初始化音效系统"""
        self.is_initialized = False
        self.current_music = None
        self.sounds = {}
        self.fade_timer = 0
        self.fade_duration = 30  # 渐弱持续帧数 (约0.75秒)
        self.fade_callback = None
        self._init_mixer()

    def _init_mixer(self):
        """初始化混音器"""
        try:
            pygame.mixer.init()
            self.is_initialized = True
        except (pygame.error, OSError):
            print("音效系统初始化失败")

    def play_music(self, music_name, loop=True, ext='mp3', force_restart=False):
        """
        播放背景音乐
        :param music_name: 音乐文件名 (不含扩展名)
        :param loop: 是否循环播放
        :param ext: 文件扩展名 (默认mp3)
        :param force_restart: 是否强制重新播放（即使是同一首歌）
        """
        if not self.is_initialized:
            return

        # 如果是同一首歌且不强制重启，跳过
        if self.current_music == music_name and not force_restart:
            return

        # 如果有音乐在播放，先渐弱
        if self.current_music and pygame.mixer.music.get_busy():
            self._fade_and_switch(music_name, loop, ext)
        else:
            self._load_and_play(music_name, loop, ext)

    def _fade_and_switch(self, new_music_name, loop, ext):
        """
        渐弱当前音乐，然后切换到新音乐
        :param new_music_name: 新音乐文件名
        :param loop: 是否循环播放
        :param ext: 文件扩展名
        """
        self.fade_timer = self.fade_duration
        self.fade_callback = lambda: self._load_and_play(new_music_name, loop, ext)

    def _load_and_play(self, music_name, loop, ext):
        """
        加载并播放音乐
        :param music_name: 音乐文件名
        :param loop: 是否循环播放
        :param ext: 文件扩展名
        """
        music_path = f"{SOUND_DIR}/{music_name}.{ext}"
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1 if loop else 0)
            pygame.mixer.music.set_volume(1.0)
            self.current_music = music_name
        except (pygame.error, FileNotFoundError):
            print(f"无法加载音乐: {music_path}")

    def update(self):
        """
        更新音效系统（需要在游戏循环中调用）
        处理渐弱效果
        """
        if not self.is_initialized:
            return

        if self.fade_timer > 0:
            self.fade_timer -= 1
            # 计算当前音量 (从1.0渐弱到0.0)
            volume = self.fade_timer / self.fade_duration
            pygame.mixer.music.set_volume(volume)

            # 渐弱完成，执行回调
            if self.fade_timer <= 0 and self.fade_callback:
                callback = self.fade_callback
                self.fade_callback = None
                callback()

    def stop_music(self):
        """停止背景音乐"""
        if self.is_initialized:
            pygame.mixer.music.stop()
            self.current_music = None

    def play_sound(self, sound_name):
        """
        播放音效
        :param sound_name: 音效文件名 (不含扩展名)
        """
        if not self.is_initialized:
            return

        if sound_name not in self.sounds:
            sound_path = f"{SOUND_DIR}/{sound_name}.wav"
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
            except (pygame.error, FileNotFoundError):
                print(f"无法加载音效: {sound_path}")
                return

        self.sounds[sound_name].play()

    def set_volume(self, volume):
        """
        设置音量
        :param volume: 音量 (0.0-1.0)
        """
        if self.is_initialized:
            pygame.mixer.music.set_volume(volume)
