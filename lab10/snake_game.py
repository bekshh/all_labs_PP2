import pygame
import sys
import time
from db_manager import GameDB

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.db = GameDB()
        self.username = self._get_username()
        self.user_id = self.db.get_or_create_user(self.username)
        self.current_level = self.db.get_user_level(self.user_id)
        self.level_config = self.db.get_level_config(self.current_level)
        
        self.speed = self.level_config[0]
        self.walls = self.level_config[1]["walls"]
        
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Snake Game - Level {self.current_level}")
        
        self.snake = [[100, 50], [90, 50], [80, 50]]
        self.food = [300, 300]
        self.direction = 'RIGHT'
        self.score = 0
        self.game_paused = False
        self.game_over = False
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)

    def _get_username(self):
        """Получение имени пользователя"""
        print("Welcome to Snake Game!")
        return input("Enter your username: ")

    def draw_snake(self):
        """Отрисовка змейки"""
        for pos in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    def draw_food(self):
        """Отрисовка еды"""
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], 10, 10))

    def draw_walls(self):
        """Отрисовка стен"""
        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(*wall))

    def move_snake(self):
        """Движение змейки"""
        if self.direction == 'RIGHT':
            self.snake.insert(0, [self.snake[0][0] + 10, self.snake[0][1]])
        elif self.direction == 'LEFT':
            self.snake.insert(0, [self.snake[0][0] - 10, self.snake[0][1]])
        elif self.direction == 'UP':
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] - 10])
        elif self.direction == 'DOWN':
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] + 10])
        
        # Проверка на съедение еды
        if self.snake[0] == self.food:
            self.score += 10
            self._generate_food()
        else:
            self.snake.pop()

    def _generate_food(self):
        """Генерация новой еды"""
        while True:
            self.food = [
                round((pygame.time.get_ticks() * 3) % (self.width - 10) / 10) * 10,
                round((pygame.time.get_ticks() * 7) % (self.height - 10) / 10) * 10
            ]
            # Проверка, чтобы еда не появилась в стене или в змейке
            food_in_wall = any(
                wall[0] <= self.food[0] <= wall[0] + wall[2] and
                wall[1] <= self.food[1] <= wall[1] + wall[3]
                for wall in self.walls
            )
            food_in_snake = any(segment == self.food for segment in self.snake)
            if not food_in_wall and not food_in_snake:
                break

    def check_collision(self):
        """Проверка столкновений"""
        # Со стенками экрана
        if (self.snake[0][0] >= self.width or self.snake[0][0] < 0 or
            self.snake[0][1] >= self.height or self.snake[0][1] < 0):
            return True
        
        # Со стенами уровня
        for wall in self.walls:
            if (wall[0] <= self.snake[0][0] <= wall[0] + wall[2] and
                wall[1] <= self.snake[0][1] <= wall[1] + wall[3]):
                return True
        
        # С самой собой
        for segment in self.snake[1:]:
            if segment == self.snake[0]:
                return True
        
        return False

    def pause_game(self):
        """Пауза игры и сохранение состояния"""
        self.game_paused = True
        game_state = {
            "snake": self.snake,
            "food": self.food,
            "direction": self.direction,
            "score": self.score
        }
        self.db.save_game_state(self.user_id, self.current_level, self.score, game_state)
        print("Game paused and state saved!")

    def display_score(self):
        """Отображение счета"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))

    def run(self):
        """Основной игровой цикл"""
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Пауза по клавише P
                        self.pause_game()
                    
                    if not self.game_paused:
                        if event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                            self.direction = 'RIGHT'
                        elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                            self.direction = 'LEFT'
                        elif event.key == pygame.K_UP and self.direction != 'DOWN':
                            self.direction = 'UP'
                        elif event.key == pygame.K_DOWN and self.direction != 'UP':
                            self.direction = 'DOWN'
            
            if not self.game_paused:
                self.screen.fill((0, 0, 0))
                self.move_snake()
                
                if self.check_collision():
                    self.game_over = True
                
                self.draw_walls()
                self.draw_snake()
                self.draw_food()
                self.display_score()
                
                pygame.display.update()
                self.clock.tick(self.speed)
            else:
                # Обработка паузы
                pause_text = self.font.render("GAME PAUSED - Press any key to continue", True, (255, 255, 255))
                self.screen.blit(pause_text, (self.width//2 - 200, self.height//2))
                pygame.display.update()
                
                # Ждем нажатия любой клавиши для продолжения
                wait = True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            wait = False
                            self.game_paused = False
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
        
        self.db.close()
        print(f"Game Over! Your score: {self.score}")

if __name__ == "__main__":
    game = SnakeGame()
    game.run()