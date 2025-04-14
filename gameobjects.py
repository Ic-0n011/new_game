import pygame
import config as cfg

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.position = position
        self.size = size
        self.normal_color = cfg.RED
        self.press_color = (0, 100, 0)
        self.presses = 0
        self.animating = False
        self.animation_scale = 1.0
        self.animation_timer = 0
        self.animation_duration = 200
        self.image = self.create_button_image(1.0)
        self.rect = self.image.get_rect(center=position)


    def create_button_image(self, scale):
        scaled_size = (int(self.size[0] * scale), int(self.size[1] * scale))
        surface = pygame.Surface(scaled_size, pygame.SRCALPHA)
        color = self.press_color if self.animating else self.normal_color
        pygame.draw.ellipse(surface, color, (0, 0, scaled_size[0], scaled_size[1]))
        return surface

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def interact(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                self.presses += 1
                self.animating = True
                self.animation_timer = pygame.time.get_ticks()
                self.image = self.create_button_image(self.animation_scale)
                if self.presses == 3:
                    return cfg.ENDING_BUTTON_THREE_TIMES
        return None

    def update(self):
        if self.animating:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.animation_timer
            if elapsed < self.animation_duration:
                progress = elapsed / self.animation_duration
                if progress < 0.5:
                    self.animation_scale = 1.0 - 0.2 * (progress / 0.5)
                else:
                    self.animation_scale = 0.8 + 0.2 * ((progress - 0.5) / 0.5)
                self.image = self.create_button_image(self.animation_scale)
                self.rect = self.image.get_rect(center=self.position)
            else:
                self.animating = False
                self.animation_scale = 1.0
                self.image = self.create_button_image(1.0)
                self.rect = self.image.get_rect(center=self.position)

class MenuButtonSprite(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.position = position
        self.size = size
        self.normal_color = (0, 255, 0)
        self.press_color = (0, 200, 0)
        self.clicked = False
        self.image = self.create_button_image()
        self.rect = self.image.get_rect(center=position)

    def create_button_image(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        color = self.normal_color
        if self.clicked:
            color = self.press_color
        pygame.draw.rect(surface, color, (0, 0, self.size[0], self.size[1]))
        return surface

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def interact(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True
                self.image = self.create_button_image()
                return True
        elif event.type == pygame.MOUSEBUTTONUP and self.clicked:
            self.clicked = False
            self.image = self.create_button_image()
        return None

    def update(self):
        pass

class LeverSprite(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.position = position
        self.size = size
        self.image = self.create_lever_image()
        self.rect = self.image.get_rect(center=position)
        self.angle = 0
        self.visible = False
        self.animating = False
        self.target_angle = 45

    def create_lever_image(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (150, 150, 150), (self.size[0] // 4, 0, self.size[0] // 2, self.size[1]))
        pygame.draw.circle(surface, (255, 0, 0), (self.size[0] // 2, 0), self.size[0] // 4)
        return surface

    def draw(self, screen):
        if self.visible:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.position)
            screen.blit(rotated_image, rotated_rect.topleft)

    def interact(self, event):
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                self.animating = True
        return None

    def update(self):
        if self.animating and self.angle < self.target_angle:
            self.angle += 5
            if self.angle >= self.target_angle:
                self.animating = False
                return cfg.ENDING_BUTTON_AND_LEVER
        return None

class MonitorSprite(pygame.sprite.Sprite):
    def __init__(self, rect, font_regular, font_large):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(cfg.BLACK)
        pygame.draw.rect(self.image, (100, 100, 100), (0, 0, rect.width, rect.height), 10)
        self.click_count = 0
        self.display_mode = 'normal'
        self.font_regular = font_regular
        self.font_large = font_large

    def draw(self, screen):
        # Всегда начинаем с чистой поверхности
        self.image.fill(cfg.BLACK)
        pygame.draw.rect(self.image, (100, 100, 100), (0, 0, self.rect.width, self.rect.height), 10)

        if self.display_mode == 'ending2':
            line1 = self.font_regular.render("ошибка: залипание кнопки", True, cfg.WHITE)
            line2 = self.font_regular.render("решение: не трогать кнопку", True, cfg.WHITE)
            self.image.blit(line1, ((self.rect.width - line1.get_width()) // 2, 50))
            self.image.blit(line2, ((self.rect.width - line2.get_width()) // 2, 100))
        elif self.display_mode == 'ending3':
            win_text = self.font_large.render("ПОБЕДА", True, cfg.WHITE)
            text_rect = win_text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            self.image.blit(win_text, text_rect)
        elif self.click_count:
            line1 = self.font_regular.render(f"пожалуйста, не трогайте экран", True, cfg.WHITE)
            line2 = self.font_regular.render("Он довольно хрупкий", True, cfg.WHITE)
            self.image.blit(line1, ((self.rect.width - line1.get_width()) // 2, 50))
            self.image.blit(line2, ((self.rect.width - line2.get_width()) // 2, 100))
        # Для 'normal' ничего не добавляем, остается пустая рамка
        screen.blit(self.image, self.rect.topleft)

    def interact(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                self.click_count += 1
                if self.click_count == 3:
                    return cfg.ENDING_SMASHED_MONITOR
        return None

class Background:
    def __init__(self):
        self.bookshelf_image = pygame.image.load(cfg.resource_path("static/bookshelf-large.png")).convert()
        self.bookshelf_image = pygame.transform.scale(self.bookshelf_image, (cfg.WIDTH, cfg.HEIGHT))
        self.table = self.create_table()

    def create_table(self):
        surface = pygame.Surface((600, 350))
        surface.fill((139, 69, 19))  # Цвет дерева
        return surface

    def draw(self, screen):
        screen.blit(self.bookshelf_image, (0, 0))
        screen.blit(self.table, (100, 400))