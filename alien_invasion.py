import sys

import pygame

class AlienInvation():
    """Класс для управления ресурсами иповедением игры."""
    
    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Alien Invasion")
        
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # отображение последнего прорисованного экрана.
            pygame.display.flip()
            
if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvation()
    ai.run_game()