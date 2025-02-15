import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("smash the anger")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Load images (replace with your actual image paths)
try:
    duck_image = pygame.image.load("duck.png").convert_alpha()
    hammer_image = pygame.image.load("hammer.png").convert_alpha()
    hole_image = pygame.image.load("hole.png").convert_alpha()
except FileNotFoundError:
    print("Error: Images not found. Make sure 'duck.png', 'hammer.png', and 'hole.png' are in the same directory.")
    pygame.quit()
    exit()

# Duck properties
duck_width = 30 # Reduced width
duck_height = 30 # Reduced height
duck_x = 0
duck_y = 0  # Start at hole level
duck_speed = 5
duck_state = "hidden"
duck_timer = 0
duck_interval = 1000
duck_rise_duration = 300
duck_rise_y_offset = 20  # How much above the hole the duck rises

# Hole properties (Dynamic hole generation)
hole_width = 50
hole_height = 80
hole_positions = []
num_holes_x = 7
num_holes_y = 7
hole_spacing_x = width // num_holes_x
hole_spacing_y = height // num_holes_y

for x in range(num_holes_x):
    for y in range(num_holes_y):
        hole_positions.append((x * hole_spacing_x, y * hole_spacing_y))

# Hammer properties
hammer_width = 80
hammer_height = 80
hammer_x = 0
hammer_y = 0
hammer_is_swinging = False

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hammer_is_swinging = True
            hammer_x, hammer_y = pygame.mouse.get_pos()

    # Duck logic
    if duck_state == "hidden":
        current_time = pygame.time.get_ticks()
        if current_time - duck_timer > duck_interval:
            duck_state = "rising"
            current_hole = random.randint(0, len(hole_positions) - 1)
            duck_x = hole_positions[current_hole][0] + (hole_width // 2) - (duck_width // 2)
            duck_y = hole_positions[current_hole][1] - duck_height  # Start at the top of the hole
            duck_timer = current_time
            duck_rise_start_time = current_time

    elif duck_state == "rising":
        current_time = pygame.time.get_ticks()
        rise_progress = (current_time - duck_rise_start_time) / duck_rise_duration
        if rise_progress >= 1:
            rise_progress = 1
            duck_state = "visible"

        duck_y = hole_positions[current_hole][1] - duck_height - (rise_progress * duck_rise_y_offset)  # y position for duck to rise

    elif duck_state == "visible":
        if pygame.time.get_ticks() - duck_timer > duck_interval // 2:
            duck_state = "falling"

    elif duck_state == "falling":
        duck_y += duck_speed
        if duck_y > height:
            duck_state = "hidden"

    # Hammer logic
    if hammer_is_swinging:
        hammer_rect = hammer_image.get_rect(topleft=(hammer_x, hammer_y))
        duck_rect = duck_image.get_rect(topleft=(duck_x, duck_y))

        if hammer_rect.colliderect(duck_rect) and duck_state == "visible":
            score += 1
            duck_state = "hidden"

        hammer_is_swinging = False

    # Drawing
    screen.fill(white)

    # Draw holes
    for hole_pos in hole_positions:
        screen.blit(hole_image, hole_pos)

    if duck_state == "rising" or duck_state == "visible":
        screen.blit(duck_image, (duck_x, duck_y))

    if hammer_is_swinging:
        screen.blit(hammer_image, (hammer_x, hammer_y))

    # Draw score
    score_text = font.render("Score: " + str(score), 1, black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
