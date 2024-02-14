import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Initial direction: right

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the last segment

    def grow(self):
        tail = self.body[-1]
        new_tail = (tail[0] - self.direction[0], tail[1] - self.direction[1])
        self.body.append(new_tail)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Game over screen
def game_over(screen, score):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    retry_text = font.render("Try Again (Space)", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(retry_text, retry_rect)

    pygame.display.flip()

    # Wait for the player to choose an option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "retry"


# Start game screen
def start_game(screen):
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press any key to start", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill(BLACK)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

    # Wait for the player to start the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                return


# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    start_game(screen)

    snake = Snake()
    food = Food()
    score = 0

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()

        if snake.body[0] == food.position:
            snake.grow()
            food = Food()
            score += 1

        snake.draw(screen)
        food.draw(screen)

        # Check for collisions
        if (snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT or
                len(snake.body) != len(set(snake.body))):
            action = game_over(screen, score)
            if action == "retry":
                snake = Snake()
                score = 0

        pygame.display.flip()
        clock.tick(10)  # Adjust snake speed

    pygame.quit()


if __name__ == "__main__":
    main()
