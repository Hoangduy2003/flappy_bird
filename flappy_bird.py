import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((400,600))
pygame.display.set_caption('Flappy Bird')
running = True
start = False

BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
BROWN = (165,45,45)
GREEN = (0,250,0)

clock = pygame.time.Clock()

TUBE_WIDTH = 50
TUBE_DISTANCE = 200
TUBE_GAP = 150
tube1_x = 800
tube2_x = tube1_x + TUBE_DISTANCE
tube3_x = tube2_x + TUBE_DISTANCE
tube1_height = randint(100,350)
tube2_height = randint(100,350)
tube3_height = randint(100,350)
TUBE_VELOCITY = 3
BIRD_X = 50
bird_y = 150
BIRD_WIDTH = 35
BIRD_HEIHT = 35
FALLING_VELOCITY = 3
GRAVITY = 0.5
SAND_Y = 550

score = 0 
font = pygame.font.SysFont('sans',20)
tube1_pass = False
tube2_pass = False
tube3_pass = False
game_over = False

background_image = pygame.image.load("flappy_bird_background.png")
bird_image = pygame.image.load("flappy_bird.png")

#change image size
bird_image = pygame.transform.scale(bird_image,(BIRD_WIDTH,BIRD_HEIHT))

while running:
	clock.tick(60)
	screen.blit(background_image,(0,0))

	#draw sky
	sky_rect = pygame.draw.rect(screen,WHITE,(0,0,400,0))

	#draw sand
	sand_rect = pygame.draw.rect(screen,BROWN,(0,SAND_Y,400,50))

	#draw bird
	bird_rect = screen.blit(bird_image,(BIRD_X,bird_y))

	if start == False:
		#draw start button
		mouse_x, mouse_y = pygame.mouse.get_pos()
		pygame.draw.rect(screen,GREEN,(150,250,100,50))
		start_text = font.render("Start",True,BLACK)
		screen.blit(start_text,(181,262))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if 150 < mouse_x < 250 and 250 < mouse_y < 300:
						start = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					start = True

	if start:
		#draw tubes
		tube1_high_rect = pygame.draw.rect(screen,BLUE,(tube1_x,0,TUBE_WIDTH,tube1_height))
		tube1_low_rect = pygame.draw.rect(screen,BLUE,(tube1_x,tube1_height+TUBE_GAP,TUBE_WIDTH,600-tube1_height-TUBE_GAP))
		tube2_high_rect = pygame.draw.rect(screen,BLUE,(tube2_x,0,TUBE_WIDTH,tube2_height))
		tube2_low_rect = pygame.draw.rect(screen,BLUE,(tube2_x,tube2_height+TUBE_GAP,TUBE_WIDTH,600-tube2_height-TUBE_GAP))
		tube3_high_rect = pygame.draw.rect(screen,BLUE,(tube3_x,0,TUBE_WIDTH,tube3_height))
		tube3_low_rect = pygame.draw.rect(screen,BLUE,(tube3_x,tube3_height+TUBE_GAP,TUBE_WIDTH,600-tube3_height-TUBE_GAP))

		#draw sand
		sand_rect = pygame.draw.rect(screen,BROWN,(0,SAND_Y,400,50))

		#falling
		bird_y += FALLING_VELOCITY
		FALLING_VELOCITY += GRAVITY

		#tubes movement
		tube1_x -= TUBE_VELOCITY
		tube2_x -= TUBE_VELOCITY
		tube3_x -= TUBE_VELOCITY

		#generate new tube
		if tube1_x < -TUBE_WIDTH:
			tube1_x = tube3_x + TUBE_DISTANCE
			tube1_height = randint(100,325)
			tube1_pass = False
		if tube2_x < -TUBE_WIDTH:
			tube2_x = tube1_x + TUBE_DISTANCE
			tube2_height = randint(100,325)
			tube2_pass = False
		if tube3_x < -TUBE_WIDTH:
			tube3_x = tube2_x + TUBE_DISTANCE
			tube3_height = randint(100,325)
			tube3_pass = False

		#update score
		score_txt = font.render("Score: "+str(score),True,BLACK)
		screen.blit(score_txt,(5,5))
		if tube1_x + TUBE_WIDTH < BIRD_X and tube1_pass == False:
			score += 1
			tube1_pass = True
		if tube2_x + TUBE_WIDTH < BIRD_X and tube2_pass == False:
			score += 1
			tube2_pass = True
		if tube3_x + TUBE_WIDTH < BIRD_X and tube3_pass == False:
			score += 1
			tube3_pass = True

		#collision
		for tube in [tube1_high_rect, tube1_low_rect, tube2_high_rect, tube2_low_rect, tube3_high_rect, tube3_low_rect, sky_rect, sand_rect]:
			if bird_rect.colliderect(tube) or bird_y < 0:
				game_over = True
				TUBE_VELOCITY = 0
				FALLING_VELOCITY = 0
				game_over_txt = font.render("Game Over",True,BLACK)
				press_space_txt = font.render("Press Space To Continue",True,BLACK)
				pygame.draw.rect(screen,RED,(100,250,200,50))
				pygame.draw.rect(screen,WHITE,(100,300,200,50))
				screen.blit(game_over_txt,(157,262))
				screen.blit(score_txt,(168,309))
				screen.blit(press_space_txt,(107,370))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			#jumping
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if game_over:
						bird_y = 150
						TUBE_VELOCITY = 3
						FALLING_VELOCITY = 0
						tube1_x = 800
						tube2_x = tube1_x + TUBE_DISTANCE
						tube3_x = tube2_x + TUBE_DISTANCE
						score = 0
						game_over = False
				
					FALLING_VELOCITY = 0
					FALLING_VELOCITY -= 8

	pygame.display.flip()
 
pygame.quit()