import os

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс, представляющий одного пришельца."""
    
    def __init__(self, ai_game):
        """Инициализирует пришельца и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # проверка существования файла изображения
        if not os.path.exists ('images/alien.bmp'):
            raise FileNotFoundError ("Файл 'images/alien.bmp' не найден. Убедитесь, что он находится в папке 'images'.")
        
        # загрузка изображения пришельца и назначение атрибута rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        
        # каждый новый пришелец появляется в левом верхем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)

    def update(self):
        """Перемещает пришельца вправо."""
        self.x += self.settings.alien_speed
        self.rect.x = self.x