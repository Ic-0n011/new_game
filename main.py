import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пожалуйста, ничего не трогайте")

# Цветовая палитра
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)  # Для декоративных объектов

# Обновленные зоны экрана
MONITOR_RECT = pygame.Rect(250, 50, 300, 200)  # Монитор 300x200
TABLE_RECT = pygame.Rect(0, 250, 800, 350)     # Стол 800x350

# Настройки кнопки
button_pos = (400, 400)
button_radius = 40
button_pressed = False

# Настройки рычага
switch_pos = (600, 400)
switch_angle = 0
switch_visible = False
switch_animating = False
switch_target_angle = 45

# Состояние игры
button_presses = 0
monitor_clicks = 0

# Шрифты
regular_font = pygame.font.Font(None, 24)  # Обычный текст
large_font = pygame.font.Font(None, 48)    # Крупные символы

# Типы концовок
ENDING_SMASHED_MONITOR = 1
ENDING_BUTTON_THREE_TIMES = 2
ENDING_BUTTON_AND_LEVER = 3

# Функция отображения концовки
def show_ending(ending_type):
    if ending_type == ENDING_SMASHED_MONITOR:
        screen.fill(BLACK)
        triangle_text = large_font.render("Здесь будут сиволы/подсказки для следующей загадки + разбитый монитор", True, WHITE).convert_alpha()
        text_rect = triangle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        for i in range(30):
            alpha = int((i / 29) * 255)
            triangle_text.set_alpha(alpha)
            screen.blit(triangle_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(100)
    elif ending_type == ENDING_BUTTON_THREE_TIMES:
        monitor_surface = pygame.Surface((MONITOR_RECT.width, MONITOR_RECT.height))
        monitor_surface.fill(BLACK)
        line1 = regular_font.render("ots: запуск_системы/завершить_игру", True, WHITE)
        line2 = regular_font.render("ошибка: Игрок не достоин", True, WHITE)
        monitor_surface.blit(line1, ((MONITOR_RECT.width - line1.get_width()) // 2, 50))
        monitor_surface.blit(line2, ((MONITOR_RECT.width - line2.get_width()) // 2, 100))
        screen.blit(monitor_surface, MONITOR_RECT.topleft)
        pygame.display.flip()
        pygame.time.wait(3000)
    elif ending_type == ENDING_BUTTON_AND_LEVER:
        monitor_surface = pygame.Surface((MONITOR_RECT.width, MONITOR_RECT.height))
        monitor_surface.fill(BLACK)
        win_text = large_font.render("ПОБЕДА", True, WHITE)
        text_rect = win_text.get_rect(center=(MONITOR_RECT.width // 2, MONITOR_RECT.height // 2))
        monitor_surface.blit(win_text, text_rect)
        screen.blit(monitor_surface, MONITOR_RECT.topleft)
        pygame.display.flip()
        pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Основной игровой цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if math.dist(mouse_pos, button_pos) <= button_radius:
                button_presses += 1
                button_pressed = True
                if button_presses == 1:
                    switch_visible = True
                elif button_presses == 3:
                    show_ending(ENDING_BUTTON_THREE_TIMES)
            elif MONITOR_RECT.collidepoint(mouse_pos):
                monitor_clicks += 1
                if monitor_clicks == 3:
                    show_ending(ENDING_SMASHED_MONITOR)
            elif switch_visible and math.dist(mouse_pos, switch_pos) <= 50:
                switch_animating = True

    if switch_animating and switch_angle < switch_target_angle:
        switch_angle += 5
        if switch_angle >= switch_target_angle:
            show_ending(ENDING_BUTTON_AND_LEVER)

    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, MONITOR_RECT, 3)
    pygame.draw.rect(screen, GRAY, TABLE_RECT, 3)

    # Декоративные объекты на столе
    pygame.draw.rect(screen, BROWN, (50, 500, 50, 50))  # Корзина
    pygame.draw.rect(screen, BROWN, (100, 450, 30, 40)) # Папка 1
    pygame.draw.rect(screen, BROWN, (140, 450, 30, 40)) # Папка 2
    pygame.draw.rect(screen, BROWN, (700, 450, 60, 20)) # Книга 1
    pygame.draw.rect(screen, BROWN, (700, 470, 60, 20)) # Книга 2

    current_radius = button_radius * 0.9 if button_pressed else button_radius
    pygame.draw.circle(screen, RED, button_pos, int(current_radius))
    button_pressed = False

    if switch_visible:
        switch_surf = pygame.Surface((20, 60), pygame.SRCALPHA)
        pygame.draw.rect(switch_surf, GREEN, (0, 20, 20, 40))
        pygame.draw.rect(switch_surf, GREEN, (5, 0, 10, 20))
        rotated_switch = pygame.transform.rotate(switch_surf, switch_angle)
        switch_rect = rotated_switch.get_rect(center=switch_pos)
        screen.blit(rotated_switch, switch_rect.topleft)

    pygame.display.flip()
    clock.tick(60)