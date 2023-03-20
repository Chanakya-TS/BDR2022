# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

rom neurosity import neurosity_sdk
from dotenv import load_dotenv
import os

load_dotenv()

timestamp = 0

neurosity = neurosity_sdk({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD"),
})

LATEST_MOVE = "NONE"

def callbackRight(data):
    global timestamp
    global LATEST_MOVE
    prob = data['predictions'][0]['probability']
    ts = data['predictions'][0]['timestamp']
    # print(prob)
    if prob > 0.8 and ts - timestamp > 5000:
        print("moving right")
        LATEST_MOVE = "RIGHT"
        timestamp = ts


def callbackLeft(data):
    global timestamp
    global LATEST_MOVE
    prob = data['predictions'][0]['probability']
    # print(prob)
    ts = data['predictions'][0]['timestamp']
    if prob > 0.8 and ts - timestamp > 5000:
        print("moving left")
        LATEST_MOVE = "LEFT"
        timestamp = ts


unsubscribeRight = neurosity.kinesis("rightArm", callbackRight)
unsubscribeLeft = neurosity.kinesis("leftArm", callbackLeft)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT,
            )
        )

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT] or LATEST_MOVE == "LEFT":
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT] or LATEST_MOVE == "RIGHT":
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                0,
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 600)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, and every sprite
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep our main loop running
running = True

clock = pygame.time.Clock()

# Our main loop

timer = 0

font = pygame.font.SysFont("Times New Roman", 30)

while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    timerDisplay = font.render(str(timer // 30), 10, (255, 255, 255))
    timer += 1

    screen.blit(timerDisplay, (SCREEN_WIDTH / 2, 30))

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        player.kill()
        running = False

    # Flip everything to the display
    pygame.display.flip()

    clock.tick(30)
