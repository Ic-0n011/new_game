import pygame
import sys
import config as cfg
from gameobjects import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption("Пожалуйста, ничего не трогайте")
        self.clock = pygame.time.Clock()

        self.regular_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)

        # Инициализация объектов игры
        self.background = Background()
        self.monitor = MonitorSprite(pygame.Rect(*cfg.MONITOR_POS, *cfg.MONITOR_SIZE), self.regular_font, self.large_font)
        self.button = ButtonSprite((400, 500), (80, 80))
        self.lever = LeverSprite((500, 500), (20, 60))
        self.interactive_objects = [self.button, self.lever, self.monitor]

        # Состояние игры
        self.state = "menu"
        self.fullscreen = False
        self.music_on = True  # По умолчанию музыка включена

        # Загрузка и запуск музыки
        self.destroyed_sound = pygame.mixer.Sound("static/destroyed_complex.mp3")
        pygame.mixer.music.load("static/background_music_1.mp3")  # Укажи правильное расширение файла
        pygame.mixer.music.set_volume(0.5)
        if self.music_on:
            pygame.mixer.music.play(-1)  # Запускаем музыку в бесконечном цикле

        # Меню
        self.menu_buttons = [
            MenuButtonSprite((cfg.WIDTH // 2, 200), (200, 50)),
            MenuButtonSprite((cfg.WIDTH // 2, 300), (200, 50)),
            MenuButtonSprite((cfg.WIDTH // 2, 400), (200, 50)),
            MenuButtonSprite((cfg.WIDTH // 2, 500), (200, 50)),
        ]
        self.menu_labels = [
            self.large_font.render("Играть", True, cfg.WHITE),
            self.large_font.render("Настройки", True, cfg.WHITE),
            self.large_font.render("Об игре", True, cfg.WHITE),
            self.large_font.render("Выход", True, cfg.WHITE),
        ]

        # Настройки
        self.settings_buttons = [
            MenuButtonSprite((cfg.WIDTH // 2, 200), (200, 50)),  # Музыка
            MenuButtonSprite((cfg.WIDTH // 2, 300), (200, 50)),  # Полноэкранный режим
            MenuButtonSprite((cfg.WIDTH // 2, 400), (200, 50)),  # Назад
        ]
        self.settings_labels = [
            self.large_font.render(f"Музыка: {'Вкл' if self.music_on else 'Выкл'}", True, cfg.WHITE),
            self.large_font.render(f"Полноэкранный: {'Вкл' if self.fullscreen else 'Выкл'}", True, cfg.WHITE),
            self.large_font.render("Назад", True, cfg.WHITE),
        ]

        # Об игре
        self.about_text = [
            self.regular_font.render("игра: Пожалуйста, ничего не трогайте | автор: Ic0n", True, cfg.WHITE),
            self.regular_font.render("крайне короткая игра, с тремя концовками:", True, cfg.WHITE),
            self.regular_font.render("Первая достигается просто, нужно нажать три раза на красню кнопку, для второй ", True, cfg.WHITE),
            self.regular_font.render("нужно нажать сначало на кнопку, а потом на рычаг, который появится воле нее", True, cfg.WHITE),
            self.regular_font.render("для третьей нужно разбить экран, нажав по нему три раза", True, cfg.WHITE),
            self.regular_font.render("Нажмите Esc для возврата", True, cfg.WHITE),
        ]
        self.back_button = MenuButtonSprite((cfg.WIDTH // 2, 500), (200, 50))
        self.back_label = self.large_font.render("Назад", True, cfg.WHITE)

        # Подтверждение выхода
        self.confirm_buttons = [
            MenuButtonSprite((cfg.WIDTH // 2 - 150, 400), (200, 50)),
            MenuButtonSprite((cfg.WIDTH // 2 + 150, 400), (200, 50)),
        ]
        self.confirm_labels = [
            self.large_font.render("Да", True, cfg.WHITE),
            self.large_font.render("Нет", True, cfg.WHITE),
        ]
        self.confirm_text = self.large_font.render("Выйти? Прогресс будет потерян!", True, cfg.WHITE)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == "menu":
                        pygame.quit()
                        sys.exit()
                    elif self.state == "game":
                        self.state = "confirm_exit"
                    elif self.state in ["settings", "about"]:
                        self.state = "menu"

                if self.state == "menu":
                    for i, button in enumerate(self.menu_buttons):
                        if button.interact(event):
                            if i == 0:
                                self.reset_game()
                                self.state = "game"
                            elif i == 1:
                                self.state = "settings"
                            elif i == 2:
                                self.state = "about"
                            elif i == 3:
                                pygame.quit()
                                sys.exit()

                elif self.state == "settings":
                    for i, button in enumerate(self.settings_buttons):
                        if button.interact(event):
                            if i == 0:  # Кнопка "Музыка"
                                self.music_on = not self.music_on
                                if self.music_on:
                                    pygame.mixer.music.play(-1)  # Включаем музыку в цикле
                                else:
                                    pygame.mixer.music.stop()  # Выключаем музыку
                                self.settings_labels[0] = self.large_font.render(
                                    f"Музыка: {'Вкл' if self.music_on else 'Выкл'}", True, cfg.WHITE
                                )
                            elif i == 1:
                                self.fullscreen = not self.fullscreen
                                if self.fullscreen:
                                    self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT), pygame.FULLSCREEN)
                                else:
                                    self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
                                self.settings_labels[1] = self.large_font.render(
                                    f"Полноэкранный: {'Вкл' if self.fullscreen else 'Выкл'}", True, cfg.WHITE
                                )
                            elif i == 2:
                                self.state = "menu"

                elif self.state == "about":
                    if self.back_button.interact(event):
                        self.state = "menu"

                elif self.state == "confirm_exit":
                    for i, button in enumerate(self.confirm_buttons):
                        if button.interact(event):
                            if i == 0:
                                self.state = "menu"
                                self.reset_game()
                            elif i == 1:
                                self.state = "game"

                elif self.state == "game":
                    for obj in self.interactive_objects:
                        ending = obj.interact(event)
                        if ending:
                            if ending == cfg.ENDING_BUTTON_THREE_TIMES:
                                self.monitor.display_mode = 'ending2'
                                self.show_ending(ending)
                            elif ending == cfg.ENDING_SMASHED_MONITOR:
                                self.show_ending(ending)
                            elif ending == cfg.ENDING_BUTTON_AND_LEVER:
                                self.monitor.display_mode = 'ending3'
                                self.show_ending(ending)

            if self.state == "game":
                for obj in self.interactive_objects:
                    ending = obj.update()
                    if ending:
                        if ending == cfg.ENDING_BUTTON_AND_LEVER:
                            self.monitor.display_mode = 'ending3'
                            self.show_ending(ending)
                if self.button.presses >= 1:
                    self.lever.visible = True

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill(cfg.BLACK)
        if self.state == "menu":
            for button, label in zip(self.menu_buttons, self.menu_labels):
                button.draw(self.screen)
                label_rect = label.get_rect(center=button.rect.center)
                self.screen.blit(label, label_rect)
        elif self.state == "settings":
            for button, label in zip(self.settings_buttons, self.settings_labels):
                button.draw(self.screen)
                label_rect = label.get_rect(center=button.rect.center)
                self.screen.blit(label, label_rect)
        elif self.state == "about":
            for i, line in enumerate(self.about_text):
                line_rect = line.get_rect(center=(cfg.WIDTH // 2, 200 + i * 50))
                self.screen.blit(line, line_rect)
            self.back_button.draw(self.screen)
            label_rect = self.back_label.get_rect(center=self.back_button.rect.center)
            self.screen.blit(self.back_label, label_rect)
        elif self.state == "confirm_exit":
            text_rect = self.confirm_text.get_rect(center=(cfg.WIDTH // 2, 200))
            self.screen.blit(self.confirm_text, text_rect)
            for button, label in zip(self.confirm_buttons, self.confirm_labels):
                button.draw(self.screen)
                label_rect = label.get_rect(center=button.rect.center)
                self.screen.blit(label, label_rect)
        elif self.state == "game":
            self.background.draw(self.screen)
            for obj in self.interactive_objects:
                obj.draw(self.screen)

    def show_ending(self, ending_type):
        if ending_type == cfg.ENDING_SMASHED_MONITOR:
            self.screen.fill(cfg.BLACK)
            triangle_text = self.large_font.render("⛛", True, cfg.WHITE).convert_alpha()
            text_rect = triangle_text.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2))
            pygame.mixer.music.stop()
            self.destroyed_sound.play()
            for i in range(40):
                alpha = int((i / 29) * 255)
                triangle_text.set_alpha(alpha)
                self.screen.blit(triangle_text, text_rect)
                pygame.display.flip()
                pygame.time.wait(100)
            pygame.quit()
            sys.exit()
        else:
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 3000:
                self.draw()
                pygame.display.flip()
                self.clock.tick(60)
            self.reset_game()
            self.state = "menu"

    def reset_game(self):
        self.button.presses = 0
        self.lever.visible = False
        self.lever.angle = 0
        self.lever.animating = False
        self.monitor.click_count = 0
        self.monitor.display_mode = 'normal'
        self.monitor.image.fill(cfg.BLACK)
        self.monitor.image.blit(
            pygame.Surface((self.monitor.rect.width, self.monitor.rect.height)),
            (0, 0)
        )
        pygame.draw.rect(self.monitor.image, (100, 100, 100), (0, 0, self.monitor.rect.width, self.monitor.rect.height), 10)

if __name__ == "__main__":
    game = Game()
    game.run()