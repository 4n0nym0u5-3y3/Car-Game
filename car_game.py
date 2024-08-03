import pygame
from pygame.locals import *
import random

pygame.init()

# Variables

WIDTH, HEIGHT = 500, 500
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 120
ROAD_WIDTH = 300
MARKER_WIDTH = 10
MARKER_HEIGHT = 50
LANE_POSITIONS = [150, 250, 350]
PLAYER_START_X, PLAYER_START_Y = 250, 400
VEHICLE_SCALE = 45  # Scaled vehicle width
VEHICLE_GAP = 1.5  # Gap multiplier between vehicles

GRAY = (50, 50, 50)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 232, 0)
BLACK = (0, 0, 0)

# Road 
ROAD = (100, 0, ROAD_WIDTH, HEIGHT)
LEFT_EDGE_MARKER = (95, 0, MARKER_WIDTH, HEIGHT)
RIGHT_EDGE_MARKER = (395, 0, MARKER_WIDTH, HEIGHT)

# Game variables
lane_marker_move_y = 0
gameover = False
speed = 2
score = 0

# Initialize the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Car Game')
clock = pygame.time.Clock()

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Scale the image
        image_scale = VEHICLE_SCALE / image.get_rect().width
        new_size = (int(image.get_rect().width * image_scale), int(image.get_rect().height * image_scale))
        self.image = pygame.transform.scale(image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create the player's car
player = PlayerVehicle(PLAYER_START_X, PLAYER_START_Y)
player_group.add(player)

# Load vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load('images/' + image_filename) for image_filename in image_filenames]

# Load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

def draw_background():
    """ Draws the grass, road, and edge markers """
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, ROAD)
    pygame.draw.rect(screen, YELLOW, LEFT_EDGE_MARKER)
    pygame.draw.rect(screen, YELLOW, RIGHT_EDGE_MARKER)

def draw_lane_markers():
    """ Draws the lane markers """
    global lane_marker_move_y
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= MARKER_HEIGHT * 2:
        lane_marker_move_y = 0
    for y in range(MARKER_HEIGHT * -2, HEIGHT, MARKER_HEIGHT * 2):
        pygame.draw.rect(screen, WHITE, (LANE_POSITIONS[0] + 45, y + lane_marker_move_y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(screen, WHITE, (LANE_POSITIONS[1] + 45, y + lane_marker_move_y, MARKER_WIDTH, MARKER_HEIGHT))

def add_vehicle():
    """ Adds a new vehicle to the road """
    if len(vehicle_group) < 2:
        add_vehicle = all(vehicle.rect.top > vehicle.rect.height * VEHICLE_GAP for vehicle in vehicle_group)
        if add_vehicle:
            lane = random.choice(LANE_POSITIONS)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, HEIGHT / -2)
            vehicle_group.add(vehicle)

def move_vehicles():
    """ Moves the vehicles down the road """
    global speed, score
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= HEIGHT:
            vehicle.kill()
            score += 1
            if score % 5 == 0:
                speed += 1

def display_score():
    """ Displays the player's score """
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {score}', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (50, 30)
    screen.blit(text, text_rect)

def check_collisions():
    """ Checks for collisions and handles the game over condition """
    global gameover
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
        screen.blit(crash, crash_rect)

def display_gameover():
    """ Displays the game over screen """
    pygame.draw.rect(screen, RED, (0, 50, WIDTH, 100))
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Game over. Play again? (Enter Y or N)', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH / 2, 100)
    screen.blit(text, text_rect)

def reset_game():
    """ Resets the game variables """
    global gameover, speed, score
    gameover = False
    speed = 2
    score = 0
    vehicle_group.empty()
    player.rect.center = [PLAYER_START_X, PLAYER_START_Y]

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > LANE_POSITIONS[0]:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < LANE_POSITIONS[2]:
                player.rect.x += 100
            if gameover:
                if event.key == K_y:
                    reset_game()
                elif event.key == K_n:
                    running = False

    draw_background()
    draw_lane_markers()
    player_group.draw(screen)
    add_vehicle()
    move_vehicles()
    vehicle_group.draw(screen)
    display_score()
    check_collisions()

    if gameover:
        display_gameover()

    pygame.display.update()

pygame.quit()
