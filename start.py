import pygame
import sys
from subprocess import Popen
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
button_width, button_height = 280, 50
button_margin = 20
size=window_size[0]
play_by_move_button = pygame.Rect((size - button_width) // 2, 200, button_width, button_height)
play_algorithm_button = pygame.Rect((size - button_width) // 2, 270, button_width, button_height)
exit_button = pygame.Rect((size - button_width) // 2, 340, button_width, button_height)


# Chạy game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_by_move_button.collidepoint(mouse_pos):
                print("Play by Move Key button clicked")
                # Thực hiện hành động khi nút được nhấn
                Popen(["python", "solution_by_player.py"])
            elif play_algorithm_button.collidepoint(mouse_pos):
                print("Play with Algorithm button clicked")
                # Thực hiện hành động khi nút được nhấn
                Popen(["python", "solution_by_algorithm.py"])
            elif exit_button.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    # Vẽ hình nền và nút button
    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, black, play_by_move_button)
    pygame.draw.rect(screen, black, play_algorithm_button)
    pygame.draw.rect(screen, black, exit_button)

    play_by_move_text = font.render("Play by Move Key", True, white)
    play_algorithm_text = font.render("Play with Algorithm", True, white)
    exit_text = font.render("Exit", True, white)

    screen.blit(play_by_move_text, (play_by_move_button.x + 20, play_by_move_button.y + 15))
    screen.blit(play_algorithm_text, (play_algorithm_button.x + 20, play_algorithm_button.y + 15))
    screen.blit(exit_text, (exit_button.x + 20, exit_button.y + 15))

    pygame.display.flip()
