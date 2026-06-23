"""
音效系统
步骤23: 声音和音效
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
        self._init_mixer()

    def _init_mixer(self):
        """初始化混音器"""
        try:
            pygame.mixer.init()
            self.is_initialized = True
        except (pygame.error, OSError):
            print("音效系统初始化失败")

    def play_music(self, music_name, loop=True, ext='mp3'):
        """
        播放背景音乐
        :param music_name: 音乐文件名 (不含扩展名)
        :param loop: 是否循环播放
        :param ext: 文件扩展名 (默认mp3)
        """
        if not self.is_initialized:
            return

        music_path = f"{SOUND_DIR}/{music_name}.{ext}"
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = music_name
        except (pygame.error, FileNotFoundError):
            print(f"无法加载音乐: {music_path}")

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
