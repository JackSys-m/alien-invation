import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvation():
    """Класс для управления ресурсами и поведением игры."""
    
    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        # создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
    def run_game(self):
        """Запуск основного цикла игры."""
        
        while True:
            self._check_events_()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
    
    def _check_events_(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # обновление позиций снарядов
        self.bullets.update()
        # удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # удаление снарядов и пришельцев, участвующих в коллизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
    
    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана, с последующим обновлением позиций всех пришельцев во влоте.
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        # проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # проверить, добрались ли пришельцы до нижнего края экрана
        self._check_alien_bottom()
    
    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        # уменьшает ship_left -= 1
        self.stats.ships_left -= 1
        
        # очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()
        
        # создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()
        
        # пауза
        sleep(0.5)
    
    def _check_alien_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же, что при столкновении с кораблём
                self._ship_hit()
                break
    
    def _create_fleet(self):
        """Создание флота вторжения."""
        # создание пришельца и вычисление количества пришельцев в ряду
        # интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_aliens_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_aliens_x // (2 * alien_width)
        
        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_aliens_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_aliens_y // (2 * alien_height)
        
        # создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Cоздание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(75)
            
if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvation()
    ai.run_game()