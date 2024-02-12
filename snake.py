import pygame, sys, random
from pygame.math import Vector2

pygame.init()

BLACK = (0, 0, 0)
DARK_GREEN = (88, 126, 65)

clock = pygame.time.Clock()
cell_size = 30
number_of_cells = 20

OFFSET = 75

screen = pygame.display.set_mode((cell_size*number_of_cells, OFFSET + cell_size*number_of_cells))

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
        self.food_img = pygame.transform.scale(pygame.image.load("Images/food.png"), (cell_size, cell_size))

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
            cell_size, cell_size)
        screen.blit(self.food_img, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.heads = [pygame.image.load('Images/head_up.png'), pygame.image.load('Images/head_down.png'), pygame.image.load('Images/head_right.png'), pygame.image.load('Images/head_left.png')]
        self.head_img = self.heads[1]
        self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.game_over_sound = pygame.mixer.Sound("Sounds/wall.mp3")
        self.UP = Vector2(0, -1)
        self.DOWN = Vector2(0, 1)
        self.LEFT = Vector2(-1, 0)
        self.RIGHT = Vector2(1, 0)

    def draw(self):
        if self.direction == self.UP:
            self.head_img = pygame.transform.scale(self.heads[0], (cell_size, cell_size))
        if self.direction == self.DOWN:
            self.head_img = pygame.transform.scale(self.heads[1], (cell_size, cell_size))
        if self.direction == self.RIGHT:
            self.head_img = pygame.transform.scale(self.heads[2], (cell_size, cell_size))
        if self.direction == self.LEFT:
            self.head_img = pygame.transform.scale(self.heads[3], (cell_size, cell_size))
        screen.blit(self.head_img, (self.body[0].x * cell_size, OFFSET+ self.body[0].y * cell_size))
        
        for segment in self.body[1:]:
            segment_rect = (segment.x * cell_size, OFFSET+ segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        pos = (self.body[0] + self.direction)
        pos.x %= number_of_cells
        pos.y %= number_of_cells
        self.body.insert(0, pos)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)
    
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.score_font = pygame.font.Font(None, 40)

    def draw(self):
        pygame.draw.line(screen, DARK_GREEN, (0, OFFSET), (cell_size*number_of_cells, OFFSET))
        self.food.draw()
        self.snake.draw()
        score_surface = self.score_font.render("Score: "+str(game.score), True, DARK_GREEN)
        screen.blit(score_surface, (OFFSET-5, 20))
        pygame.display.update()
    
    def update(self):
        self.snake.update()
        self.check_collision_with_food()
        self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.score = 0
        self.snake.game_over_sound.play()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()


game = Game()
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 100)
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != game.snake.DOWN:
                game.snake.direction = game.snake.UP
            if event.key == pygame.K_DOWN and game.snake.direction != game.snake.UP:
                game.snake.direction = game.snake.DOWN
            if event.key == pygame.K_LEFT and game.snake.direction != game.snake.RIGHT:
                game.snake.direction = game.snake.LEFT
            if event.key == pygame.K_RIGHT and game.snake.direction != game.snake.LEFT:
                game.snake.direction = game.snake.RIGHT
				
    screen.fill(BLACK)
    game.draw()
    
    clock.tick(60)