import os

import pygame

class Ship():
    """Класс для управления кораблем."""
    
    def __init__(self, ai_game):
        """Инициирует корабль и задаёт его начальную позицию."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # проверка существования файла изображения
        if not os.path.exists ('images/ship.bmp'):
            raise FileNotFoundError ("Файл 'images/ship.bmp' не найден. Убедитесь, что он находится в папке 'images'.")
        
        # загрузка изображения корабля и получение его прямоугольника
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        
    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)