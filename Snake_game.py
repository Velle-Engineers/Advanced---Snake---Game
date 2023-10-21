# importing libraries
import pygame
import time
import random

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# Add these variables at the beginning of your code
bonus_fruit = None  # Represents the bonus fruit position
speed_fruit = None  # Represents the speed fruit position
bonus_counter = 0  # Counter for the number of normal fruits eaten before spawning bonus fruit
speed_counter = 0  # Counter for the number of normal fruits eaten before spawning speed fruit
bonus_spawn_time = 5  # Time in seconds bonus fruit should appear
speed_spawn_time = 10  # Time in seconds speed fruit should appear
speed_fruit_effect_time = 10  # Time in seconds speed fruit effect lasts

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10, 
				random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# displaying Score function
def show_score(choice, color, font, size):

	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object 
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# game over function
def game_over():

	# creating font object my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	# creating a text surface on which text 
	# will be drawn
	game_over_surface = my_font.render(
		'Your Score is : ' + str(score), True, red)
	
	# create a rectangular object for the text 
	# surface object
	game_over_rect = game_over_surface.get_rect()
	
	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	# after 2 seconds we will quit the program
	time.sleep(2)
	
	# deactivating pygame library
	pygame.quit()
	
	# quit the program
	quit()


# Main Function
while True:
    
    # handling key events
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

    # If two keys pressed simultaneously
    # we don't want snake to move into two 
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        bonus_counter += 1
        speed_counter += 1
        if bonus_counter == 3 :
            bonus_fruit = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
            bonus_counter = 0
        elif speed_counter == 8 :
            speed_fruit = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
            speed_counter = 0	
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]


    # Check if the bonus fruit should disappear
    if bonus_fruit:
        bonus_spawn_time -= 1 / snake_speed
        if bonus_spawn_time <= 0:
            bonus_fruit = None
            bonus_spawn_time = 5
   

    # Check if the speed fruit should disappear and reset the speed effect
    if speed_fruit:
        speed_spawn_time -= 1 / snake_speed
        if speed_spawn_time <= 0:
            speed_fruit = None
            speed_spawn_time = 15
            snake_speed = 15  # Reset the snake speed

    fruit_spawn = True

    # Update the bonus and speed fruit timers
    show_score(2, white, 'times new roman', 20)

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))


    if bonus_fruit:
        pygame.draw.rect(game_window, green, pygame.Rect(bonus_fruit[0], bonus_fruit[1], 10, 10))

    if speed_fruit:
        pygame.draw.rect(game_window, red, pygame.Rect(speed_fruit[0], speed_fruit[1], 10, 10))



    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)

    # If bonus fruit is present and snake eats it, increase score and length
    if bonus_fruit and snake_position[0] == bonus_fruit[0] and snake_position[1] == bonus_fruit[1]:
        score += 50
        snake_body += [list(snake_body[-1]) for _ in range(5)]
        bonus_fruit = None

    # If speed fruit is present and snake eats it, increase snake speed
    if speed_fruit and snake_position[0] == speed_fruit[0] and snake_position[1] == speed_fruit[1]:
        speed_fruit = None
        speed_spawn_time = 10
        snake_speed += 1

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed)
