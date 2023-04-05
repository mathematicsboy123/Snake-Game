import pygame
import os
import random
import time

pygame.init()

# Initialize Display and Basic Variables
WIDTH, HEIGHT = 750, 750
first = [True, True]
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
write_font = pygame.font.SysFont("comicsans", 40)

blue_rect = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_rectangle.jpg")), (30, 30))
green_rect = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_rectangle.jpg")), (30, 30))


class Snake:
    # Get information about instance of class
    def __init__(self, x, y, length, direction, image, coords):
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        self.image = image
        self.body = []
        self.coords = coords
        self.mask = pygame.mask.from_surface(image)

    # Blit snake onto the screen
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

        try: 
            for item in self.body:
                window.blit(item.image, (item.coords[0], item.coords[1]))
        except Exception:
            pass
    
    # Change the direction that the snake moves in
    def set_direction(self, direction):
        if direction == "w" and self.direction != "s":
            self.direction = "w"
        elif direction == "a" and self.direction != "d":
            self.direction = "a"
        elif direction == "s" and self.direction != "w":
            self.direction = "s"
        elif direction == "d" and self.direction != "a":
            self.direction = "d"
        else:
            pass

    # Move the snake in its already set direction
    def move(self, vel):
        self.coords = [self.x, self.y]
        if self.direction == "s" and self.y + vel + vel + 30 < HEIGHT:
            self.y += vel
        elif self.direction == "d" and self.x + vel + vel + 30 < WIDTH:
            self.x += vel
        elif self.direction == "w" and self.y - vel > 0:
            self.y -= vel
        elif self.direction == "a" and self.x - vel > 0:
            self.x -= vel
        else:
            pass

    # Check if snake is dead
    def check_death(self):
        if self.y + 36 > HEIGHT:
            return True
        elif self.x + 36 > WIDTH:
            return True
        elif self.y - 4 < 0:
            return True
        elif self.x - 4 < 0:
            return True

        for item in self.body:
            if item.coords == [self.x, self.y]:
                return True

        return False

    # Add another block to snake to make the snake grow
    def block_add(self):
        if first[0]: 
            chunk = Snake(self.coords[0], self.coords[1], 1, None, blue_rect, [self.coords[0], self.coords[1]]) 
            self.body.append(chunk)
            self.length += 1
            first[0] = False
        else:
            chunk = Snake(self.body[-1].coords[0], self.body[-1].coords[1], 1, None, blue_rect, [self.body[-1].coords[0], self.body[-1].coords[1]])
            self.length += 1
            self.body.append(chunk)
    
    # Update the coordinates for the "body", so they follow the head
    def update_coords(self):
        if first[1] and not first[0]:  
            self.body[0].coords = self.coords
            first[1] = False
        elif not first[1] and not first[0]:
            length = self.length - 1
            index = -1
            while index > -length:
                self.body[index].coords = [self.body[index - 1].coords[0], self.body[index - 1].coords[1]]
                index -= 1
            
            self.body[0].coords = self.coords
        
        for item in self.body:
            item.x = item.coords[0]
            item.y = item.coords[1]

    # Check if snake collides with food
    def collide_food(self, food):
        if collide(self, food):
            return True

        for item in self.body:
            if collide(item, food):
                return True


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    # Initialize basic variables and create my snake
    run = True
    score = 0
    food_available = False
    clock = pygame.time.Clock()
    FPS = 120

    snake = Snake(150, 375, 1, None, blue_rect, [375, 375])
    snake_vel = 2

    # Use the block_add function in snake to add more length to the block
    def add_block():
        for i in range(8):
            snake.block_add()

    # Main game loop
    while run:
        clock.tick(FPS)

        snake.move(snake_vel)
        snake.update_coords()
        if snake.check_death():
            main_menu(f"You Lost!, Your final score is {score}", True, 45)

        WIN.fill((0, 0, 0))
        snake.draw(WIN)

        if not food_available:
            if not first[0]:
                food_x = random.randint(0, WIDTH - 35)
                food_y = random.randint(0, HEIGHT - 35)
            else:
                food_x = 600
                food_y = 375

            WIN.blit(green_rect, (food_x, food_y))
            food_available = True
        else:
            WIN.blit(green_rect, (food_x, food_y))
            food_available = True

        food = Snake(food_x, food_y, 0, None, green_rect, [None, None])

        if snake.collide_food(food):
            food_available = False
            score += 1
            snake_vel += 0.1
            add_block()

        title_label = write_font.render(f"Score: {score}", 1, (255, 255, 255))
        WIN.blit(title_label, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            snake.set_direction("a")
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            snake.set_direction("d")
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            snake.set_direction("s")
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            snake.set_direction("w")


# Create main menu and show text on the screen
def main_menu(text, kill, size):
    run = True
    while run:
        WIN.fill((0, 0, 0))
        title_font = pygame.font.SysFont("comicsans", size)
        title_label = title_font.render(text, 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        if not kill:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    main()
        else:
            time.sleep(3)
            exit()


# Run code
if __name__ == "__main__":
    main_menu("Press the mouse to begin...", False, 60)
