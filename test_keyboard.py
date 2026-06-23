"""
键盘输入测试
"""
import pygame
from pygame.constants import *

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Keyboard Test')

clock = pygame.time.Clock()
running = True
x, y = 200, 150

print("测试开始 - 请按方向键")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            print(f'KEYDOWN: key={event.key}')

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        y -= 5
        print(f'UP - y={y}')
    if keys[K_DOWN]:
        y += 5
        print(f'DOWN - y={y}')
    if keys[K_LEFT]:
        x -= 5
        print(f'LEFT - x={x}')
    if keys[K_RIGHT]:
        x += 5
        print(f'RIGHT - x={x}')

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
print("测试结束")
