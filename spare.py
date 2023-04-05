import pygame
import random

# Initialize pygame
pygame.init()

# Set the window size
window_size = (400, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Snake")

# Set the dimensions of the game elements
block_size = 20
apple_size = 20

# Set the initial position and velocity of the snake
snake_position = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]

# Set the initial position of the apple
apple_position = [300, 300]
apple_spawn = True

# Set the initial direction of the snake
direction = 'RIGHT'
change_to = direction

# Set the game clock
clock = pygame.time.Clock()

# Set the score
score = 0

# Define a function to end the game


def game_over():
    pygame.quit()
    exit()


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
        if event.type == pygame.QUIT:
            game_over()

    # Validate the direction change
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= block_size
    if direction == 'DOWN':
        snake_position[1] += block_size
    if direction == 'LEFT':
        snake_position[0] -= block_size
    if direction == 'RIGHT':
        snake_position[0] += block_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == apple_position[0] and snake_position[1] == apple_position[1]:
        apple_spawn = False
        score += 1
    else:
        snake_body.pop()

    if apple_spawn == False:
        x = random.randrange(
            0, (window_size[0]-block_size) // block_size) * block_size
        y = random.randrange(
            0, (window_size[1]-block_size) // block_size) * block_size
        apple_position = [x, y]
        apple_spawn = True

    # Draw the snake and the apple
    screen.fill((0, 0, 0))
    for pos in snake_body:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
            pos[0], pos[1], block_size, block_size))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
        apple_position[0], apple_position[1], apple_size, apple_size))

    # Check for game over conditions
    if snake_position[0] < 0 or snake_position[0] > window_size[0]-block_size:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_size[1]-block_size:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Display the score
    font = pygame.font.Font('freesansbold.ttf', 18)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (5, 10))

    # Update the screen
    pygame.display.update()

    # Set the frame rate
    clock.tick(10)
