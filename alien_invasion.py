import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvation():
    """Класс для управления ресурсами и поведением игры."""
    
    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # при каждом проходе цикла перерисовывается экран.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            
            # отображение последнего прорисованного экрана.
            pygame.display.flip()
            self.clock.tick(75)
            
if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvation()
    ai.run_game()