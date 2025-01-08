import json

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    
    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.high_score_file = "high_score.json"
        self.high_score = self._load_high_score()
        self.reset_stats()
        # игра Alien Invasion запускается в активном состоянии
        self.game_active = False
        
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def _load_high_score(self):
        """Загружает рекорд из файла."""
        try:
            with open(self.high_score_file, 'r') as f:
                return int(json.load(f))
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Сохрвняет рекорд в файл."""
        with open (self.high_score_file, 'w') as f:
            json.dump(self.high_score, f)