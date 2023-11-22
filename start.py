import pygame
import sys
from subprocess import Popen
from button import Button
from settings import *
# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Maze Game")

# Load hình nền
background = pygame.image.load("img/khoidong.jpg")
background = pygame.transform.scale(background, window_size)

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# Font chữ
font = pygame.font.Font(None, 36)

# Tạo nút button
size=window_size[0]

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()


start_button = Button(200, 350, start_img, 0.5)
exit_button = Button(450, 350, exit_img, 0.5)
run = False
# Chạy game loop
while True:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    start_button.draw(screen)
    if start_button.clicked and not run:
        Popen(["python", "solution_by_algorithm.py"])
        run = True
    if exit_button.draw(screen):
        pygame.quit()
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.display.flip()
