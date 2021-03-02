import pygame,sys
import os#operating system, path to images
pygame.init()
pygame.font.init()
pygame.mixer.init()#sound effects

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))#window


pygame.display.set_caption("STAR WARS UWU!")#titol window
WHITE = (255,255,255)#rgb, tupple, white
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)




BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)#Separation between 2 spaces

BULLET_HIT_SOUND =pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3")) 
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3")) 
#YAY = pygame.mixer.Sound(os.path.join("Assets","Yay.mp3")) 

FPS = 60#how many frames per second we want our game to update at
VEL = 5#velocity we move
BULLET_VEL = 7 #velocity of the bullets
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40


#####################FONT 
main_font= pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

###############################COLISION, create an EVENT
YELLOW_HIT = pygame.USEREVENT +1 
RED_HIT = pygame.USEREVENT + 2
#import images im going to use

#SETTING IMAGES SIZE AND ROTATION
SPACE = pygame.transform.scale(pygame.image.load#BACKGROUND
	(os.path.join('Assets', "space.png")), (WIDTH,HEIGHT))




YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))#.convert()#path to image
YELLOW_SPACESHIP= pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
	(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)#55 widht, 40 height. 




RED_SPACESHIP_IMAGE = pygame.image.load(
os.path.join("Assets","spaceship_red.png"))#.convert()#path to image
RED_SPACESHIP= pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
	(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), -90)#55 widht, 40 height. 
######################################################################

def yellow_movement(keys_pressed,yellow):
	#DEFINE MOVING WSAD LEFT SPACESHIP, allows press multiple keys
		if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:#left
			yellow.x -=  VEL
		if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x-yellow.width:#right
			yellow.x +=  VEL
		if keys_pressed[pygame.K_w] and yellow.y - VEL >0:#UP
			yellow.y -=  VEL
		if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT-yellow.height-15:#DOWN
			yellow.y +=  VEL

def red_movement(keys_pressed, red):
	#DEFINE MOVING UP,DOWN,LEFT,RIGHT LEFT SPACESHIP, allows press multiple keys
		if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:#left
			red.x -=  VEL
		if keys_pressed[pygame.K_RIGHT] and  red.x + VEL < WIDTH-red.width:#right
			red.x +=  VEL
		if keys_pressed[pygame.K_UP] and red.y - VEL > 0:#UP
			red.y -=  VEL
		if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height -15:#DOWN
			red.y +=  VEL
		
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
	#move bullets, handle bullets crashing
	#print(red_lives)
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):#did yellow bullet collide with red spaceship?
			pygame.event.post(pygame.event.Event(RED_HIT))#red player was hit
			yellow_bullets.remove(bullet)
		
		#check if the bullets are out of the screen
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet) :#did yellow rectangle collide with bullet rectangle
			pygame.event.post(pygame.event.Event(YELLOW_HIT))#red player was hit
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
	
	WIN.blit(SPACE, (0,0))#Space BackGround
	#WIN.fill(WHITE)#color
	#TOP LEFT IS (0,0)
	#WIN.blit(HEART,(live_red.x,live_red.y))
	#WIN.blit(HEART,(live_yellow.x,live_yellow.y))

	img_red = main_font.render("Health: " + str(red_health) +"%", 1, WHITE)
	img_yellow = main_font.render("Health: " + str(yellow_health) +"%", 1, WHITE)

	WIN.blit(img_yellow, (10, 10))
	WIN.blit(img_red, (WIDTH-img_yellow.get_width()-15,10))
		
	pygame.draw.rect(WIN, BLACK,BORDER)#BORDER
	WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x,red.y))#put text or images to screen, put it left or right
#DRAW BULLETS IN SCREEN
	for bullet in red_bullets:
		pygame.draw.rect(WIN,RED,bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN,YELLOW,bullet)

	pygame.display.update()#update, show us white window


def draw_winner(text):

	winner = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(winner, (WIDTH/2 - winner.get_width()/2, HEIGHT/2 - winner.get_height()/2))
	pygame.display.update()
	#YAY.play()
	pygame.time.delay(7000) #pause, miliseconds


def main():
	#set game loop
	red  = pygame.Rect(700,250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)#red player
	#rectangle that defines this spaceship, X, Y ,WIDHT, HEIGHT
	yellow = pygame.Rect(200,250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	red_bullets =[]
	yellow_bullets = []

	

	
	red_health = 100 
	yellow_health = 100




	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)#controls the speed of the while loop,consistent at different computers

		for event in pygame.event.get():
			if event.type == pygame.QUIT: #user closes the window
			
				pygame.quit()#quit pygame close the window
				sys.exit()
				

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLETS:#bullets
					bullet = pygame.Rect(yellow.x + yellow.width,yellow.y+yellow.height//2-2,10,5)
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x,red.y+red.height//2-2,10,5)
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				red_health -= 10
				BULLET_HIT_SOUND.play()

			if event.type == YELLOW_HIT:
				yellow_health -= 10
				BULLET_HIT_SOUND.play()


		winner_text = ""
		if red_health <= 0:
			winner_text = "Yellow wins!"
			draw_winner(winner_text)
			break
			
			

		if yellow_health <= 0:
			winner_text = "Red wins!"
			draw_winner(winner_text)
			break

			

		# #winner_text != "":
			#draw_winner(winner_text)
			#break
			
			
			


		
		keys_pressed = pygame.key.get_pressed()#returns what keys are being pressed down
		yellow_movement(keys_pressed,yellow)
		red_movement(keys_pressed,red)
		
		handle_bullets(yellow_bullets, red_bullets, yellow, red)

		draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
		

	main()


if __name__ == "__main__":#we only run the game when we run this file 
	main()