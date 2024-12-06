import sys

import pygame

from settings import Settings

class AlienInvation():
    """Класс для управления ресурсами иповедением игры."""
    
    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # при каждом проходе цикла перерисовывается экран.
            self.screen.fill(self.settings.bg_color)
            
            # отображение последнего прорисованного экрана.
            pygame.display.flip()
            
if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvation()
    ai.run_game()