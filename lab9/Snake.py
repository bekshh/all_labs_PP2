import pygame  # Pygame кітапханасын қосу
import random  # Кездейсоқ сандармен жұмыс істеу үшін random кітапханасын қосу
import time  # Таймерлер үшін time модулі

pygame.init()  # Pygame-ді инициализациялау

# Терезе өлшемдері
WIDTH, HEIGHT = 600, 400  # Ойын терезесінің ені мен биіктігі
GRID_SIZE = 20  # Тор көзінің өлшемі (жылан мен тамақ осы тор бойынша қозғалады)
SPEED = 5  # Бастапқы жылдамдық
SCORE_TO_LEVEL_UP = 4  # Әр деңгей көтерілгенде қанша ұпай жинау керек

# Түстер анықтау (RGB форматында)
WHITE = (255, 255, 255)  # Ақ түс
GREEN = (0, 255, 0)  # Жасыл түс
DARK_GREEN = (0, 150, 0)  # Қою жасыл түс
RED = (255, 0, 0)  # Қызыл түс (тамақ)
BLUE = (0, 0, 255)  # Көк түс (ерекше тамақ)
BLACK = (0, 0, 0)  # Қара түс (фон түсі)

# Ойын терезесін жасау
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Терезе жасау
pygame.display.set_caption("Snake Game")  # Терезенің атауын орнату

# Жыланның бастапқы координаталары
snake = [(100, 100), (90, 100), (80, 100)]  # Жыланның алғашқы үш бөлігі
snake_dir = (GRID_SIZE, 0)  # Жыланның қозғалыс бағыты (оңға қарай)

# Тамақтың кездейсоқ координаталарын анықтау
food = None
food_weight = 1  # Тамақтың салмағы
food_timer = 0  # Тамақтың жоғалу уақыты

score = 0  # Ұпай саны
level = 1  # Бастапқы деңгей
running = True  # Ойын жүріп жатыр ма?
game_over = False  # Ойын аяқталды ма?
menu = True  # Мәзір көрсету керек пе?
paused = False  # Ойын кідіртілген бе?
clock = pygame.time.Clock()  # Ойын кадрларын басқару үшін сағат

# Тамақты кездейсоқ орналастыру үшін функция

def generate_food():
    global food_weight, food_timer
    while True:
        new_food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
        if new_food not in snake:  # Тамақ жыланның денесіне түспеу керек
            food_weight = random.choice([1, 2, 3])  # Тамақ салмағын кездейсоқ таңдау
            food_timer = time.time()  # Тамақтың пайда болған уақытын сақтау
            return new_food

# Алғашқы тамақты орнату
food = generate_food()

# Экранға мәтін шығару функциясы
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)  # Шрифт өлшемін орнату
    render_text = font.render(text, True, color)  # Мәтінді суретке айналдыру
    text_rect = render_text.get_rect(center=(x, y))  # Орталық координаталарын орнату
    screen.blit(render_text, text_rect)  # Экранға шығару

# Бастапқы мәзірді көрсету функциясы
def show_menu():
    screen.fill(BLACK)  # Экранды қара түспен бояу
    draw_text("SNAKE GAME", WIDTH // 10, GREEN, WIDTH // 2, HEIGHT // 4)  # Ойын атауын шығару
    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 20, 150, 50)  # Бастау батырмасының өлшемдері
    pygame.draw.rect(screen, WHITE, start_button)  # Бастау батырмасын салу
    draw_text("Start", WIDTH // 15, BLACK, WIDTH // 2, HEIGHT // 2 + 5)  # Батырма мәтінін шығару
    pygame.display.flip()  # Экранды жаңарту
    return start_button  # Батырманы қайтару

# Мәзір көрсетілген кезде күту
while menu:
    start_button = show_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Ойынды жабу
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Тышқан батырмасы басылғанда
            if start_button.collidepoint(event.pos):  # Егер бастау батырмасы басылса
                menu = False


# Ойын циклі
while running:
    screen.fill(BLACK)
    
    # Ойынды жабу оқиғасы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                snake_dir = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                snake_dir = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                snake_dir = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                snake_dir = (GRID_SIZE, 0)
    

    if game_over:  # Егер ойын аяқталса
        draw_text("YOU LOSE", WIDTH // 10, RED, WIDTH // 2, HEIGHT // 3) #мәтінді шығару
        restart_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50) #бастау батырмасының өлшемдері
        quit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50) #шығу батырмасының өлшемдері
        pygame.draw.rect(screen, WHITE, restart_button) #бастау батырмасын салу
        pygame.draw.rect(screen, WHITE, quit_button) #шығу батырмасын салу
        draw_text("Restart", WIDTH // 15, BLACK, WIDTH // 2, HEIGHT // 2 + 25) #бастау мәтінін шығару
        draw_text("Quit", WIDTH // 15, BLACK, WIDTH // 2, HEIGHT // 2 + 85) #шығу мәтінін шығару
        pygame.display.flip() #экранды жаңарту
        for event in pygame.event.get(): #события
            if event.type == pygame.MOUSEBUTTONDOWN: #тышқан батырмасы басылғанда
                if restart_button.collidepoint(event.pos): #қайта бастау батырмасы басылса
                    snake = [(100, 100), (90, 100), (80, 100)] # Жыланның алғашқы үш бөлігі
                    snake_dir = (GRID_SIZE, 0) # Жыланның қозғалыс бағыты (оңға қарай)
                    food = generate_food() # Тамақты кездейсоқ орналастыру
                    score = 0 # Ұпай саны
                    level = 1 # Бастапқы деңгей
                    SPEED = 5 # Бастапқы жылдамдық
                    game_over = False # Ойын аяқталды 
                elif quit_button.collidepoint(event.pos): #шығу батырмасы басылса
                    running = False #ойынды жабу
        continue #келесі циклга өтеміз

    
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1]) # Жыланның жаңа басы
    new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)  # Шекарадан өткенде екінші жақтан шығу
    
    if new_head in snake:  # Егер жылан өз денесіне тисе
        game_over = True # Ойын аяқталды
    

    if not game_over: # Ойын аяқталмаса
        snake.insert(0, new_head) # Жыланның жаңа басын енгізу
        if new_head == food: # Егер жыланның басы тамаққа тең болса
            score += 1 # Ұпай саны өседі
            food = generate_food() # Тамақты кездейсоқ орналастыру
            if score % SCORE_TO_LEVEL_UP == 0: # Ұпай саны қанша болса
                level += 1 # Деңгей өседі
                SPEED += 1 # Жылдамдық өседі
        else: 
            snake.pop() # Жыланның соңғы басын алу

    # Жыланның жаңа басын есептеу
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)  # Шекарадан өткенде екінші жақтан шығу
    
    # Егер жылан өз денесіне тисе - ойын аяқталады
    if new_head in snake:
        game_over = True
    
    if not game_over:
        snake.insert(0, new_head)
        if new_head == food:  # Егер жылан тамақты жесе
            score += food_weight  # Тамақтың салмағына байланысты ұпай қосылады
            food = generate_food()  # Жаңа тамақ пайда болады
            if score % SCORE_TO_LEVEL_UP == 0:
                level += 1
                SPEED += 1
        else:
            snake.pop()
    
    # Егер тамақ біраз уақыттан кейін жоғалу керек болса
    if time.time() - food_timer > 5:  # 5 секундтан кейін тамақ жоғалады
        food = generate_food()
    
    # Жыланның және тамақтың суретін салу
    pygame.draw.rect(screen, DARK_GREEN, (snake[0][0], snake[0][1], GRID_SIZE, GRID_SIZE))
    for segment in snake[1:]:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
    
    # Тамақтың түсі салмағына байланысты өзгереді
    food_color = RED if food_weight == 1 else BLUE if food_weight == 2 else WHITE
    pygame.draw.rect(screen, food_color, (food[0], food[1], GRID_SIZE, GRID_SIZE))
    
    # Ұпай мен деңгейді экранға шығару
    draw_text(f"Score: {score}", 30, WHITE, 70, 15)
    draw_text(f"Level: {level}", 30, WHITE, 70, 45)
    
    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()