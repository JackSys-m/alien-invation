import os

import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблем."""
    
    def __init__(self, ai_game):
        """Инициирует корабль и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # проверка существования файла изображения
        if not os.path.exists ('images/ship.bmp'):
            raise FileNotFoundError ("Файл 'images/ship.bmp' не найден. Убедитесь, что он находится в папке 'images'.")
        
        # загрузка изображения корабля и получение его прямоугольника
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        
        # сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        
        # флаг перемещения.
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Обновляет позицию корабля с учётом флагов."""
        # обновляется атрибут х, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor
            
        # обновление атрибута rect на основании self.x
        self.rect.x = self.x
        
    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)