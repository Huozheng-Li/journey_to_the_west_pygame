"""
西游记观音院 - 游戏主入口
步骤2-23: 完整游戏
"""
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from core.scene_manager import SceneManager
from scenes.village import VillageScene
from scenes.temple import TempleScene
from scenes.battle_scene import BattleScene
from scenes.end_scene import EndScene
from systems.sound import SoundSystem


def main():
    pygame.init()
    pygame.key.stop_text_input()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    sound_system = SoundSystem()

    scene_manager = SceneManager(screen, sound_system)
    scene_manager.add_scene('village', VillageScene(screen))
    scene_manager.add_scene('temple', TempleScene(screen))
    scene_manager.add_scene('battle', BattleScene(screen))
    scene_manager.add_scene('end_win', EndScene(screen, True))
    scene_manager.add_scene('end_lose', EndScene(screen, False))
    scene_manager.set_current_scene('village', use_fade=False)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        scene_manager.handle_events(events)
        scene_manager.update()
        scene_manager.draw()

        if scene_manager.current_scene:
            if scene_manager.current_scene.next_scene:
                next_scene_name = scene_manager.current_scene.next_scene
                scene_manager.current_scene.next_scene = None
                scene_manager.set_current_scene(next_scene_name)

            if not scene_manager.current_scene.is_active:
                if scene_manager.scene_stack:
                    scene_manager.pop_scene()
                else:
                    running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
