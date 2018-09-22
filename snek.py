import pygame
import random as r

unit = 100 # size of individual square in pixels
count_w = 10 # width in units
count_h = 10 # height in units
font_size = 20

framerate = 60 # frames per second
speed = 20 # number of frames between movement (greater than 0)
tail_growth = 5 # increase in tail length for each food eaten
starting_tail_length = 5 # starting length of tail

width = count_w * unit # screen width in pixels
height = count_h * unit + font_size # screen height in pixels
max = count_w * count_h

pygame.init()
pygame.display.set_caption("snek.py")
screen = pygame.display.set_mode((width, height)) # initialize game window
font = pygame.font.SysFont("consolas", font_size)
clock = pygame.time.Clock()

x = int
y = int
food_eaten = int
tail = [] # list will keep track of tail position


def reset_globals():
	global x
	global y
	global food_eaten
	global tail
	global tail_length
	
	x = -1
	y = 0
	food_eaten = 0
	tail = [(x, y)]
	tail_length = starting_tail_length

def off_screen(x, y):
	if x < 0 or x > count_w - 1: # x location is out of bounds
		return True
	if y < 0 or y > count_h - 1: # y location is out of bounds
		return True
	return False # x and y are on screen

def on_tail(x, y):
	if ((x, y)) in tail: # coordinates are in tail list
		return True
	return False
	
def food():
	while True: # keep trying to find valid coordinates (we must be sure there are free spaces before calling this function or we will get an infinite loop)
		x = r.randint(0, count_w - 1)
		y = r.randint(0, count_h - 1)
		if ((x, y)) not in tail: # coordinates are in free space
			return (x, y)

food_location = food() # create food now that food() has been defined

def food_check(x, y): 
	global food_location # specify global so python interpreter knows to use the existing variable
	global tail_length
	global food_eaten
	if food_location == (x, y): # if we happen to be on the food
		tail_length += tail_growth # max tail size increases
		food_eaten += 1
		print("Yum! You are now", tail_length, "snek units long.")
		food_location = food() # get a new food location
	
def win_check():
	if len(tail) >= max: # tail is at the maximum length that fits on the screen
		return True # game is won
	return False # otherwise we have not won

def increment_tail(x, y):
	tail.append(tail[-1]) # put last element in list again on the end of list ([a, b, c] would become [a, b, c, c])
	for i in range(len(tail) - 1, 0, -1): # move from end of list to beginning
		tail[i] = tail[i - 1] # scoot element to the right
	
	tail[0] = (x, y) # first element becomes current head of snek now that space has been made
	del tail[tail_length:] # trim the tail to the right length (by deleting extra from the end)

def draw_tail():
	for i in range(len(tail)):
		red = 255 - 255 * (i / max) * 2 # red moves from 255 to 0 over 1/2 max snek length
		if red < 0: red = 0
		green = 255 - 255 * (i / max) # green moves from 255 to 0 over max snek length
		if green < 0: green = 0
		pygame.draw.rect(screen, (red, green, 255), pygame.Rect(tail[i][0] * unit, tail[i][1] * unit + font_size, unit, unit)) # multiply by unit to make squares the right size

def draw():
	screen.fill((0, 0, 0)) # fill screen with black so we can re-draw from scratch
	pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_location[0] * unit, food_location[1] * unit + font_size, unit, unit)) # put food on the screen
	draw_tail()
	
	length_text = font.render("Length: {} ".format(len(tail)), True, (255, 255, 255))
	screen.blit(length_text, (0, 0))
	next_pos = length_text.get_width()
	
	if tail_length - len(tail) > 0:
		extra_food_text = font.render("+{:<2} ".format(tail_length - len(tail)), True, (255, 0, 0))
		screen.blit(extra_food_text, (next_pos, 0))
	next_pos = width // 3
	
	food_text = font.render("Food eaten: " + str(food_eaten), True, (255, 255, 255))
	screen.blit(food_text, (next_pos, 0))
	next_pos += food_text.get_width()
		
	screen_text = font.render("  Coverage: {:<4.1f}%".format((len(tail) * 100) / (max)), True, (255, 255, 255))
	screen.blit(screen_text, (next_pos, 0))
	
	pygame.display.flip() # updates display
	
def display_message(text):
	buffer = 5
	message = font.render(text, True, (255, 255, 255))
	pygame.draw.rect(screen, (0, 0, 0),  pygame.Rect(width // 2 - message.get_width() // 2 - buffer, height // 2 - message.get_height() // 2 - buffer, message.get_width() + buffer * 2, message.get_height() + buffer * 2))
	screen.blit(message, (width // 2 - message.get_width() // 2, height // 2 - message.get_height() // 2))
	pygame.display.flip() # updates display
	
def finish(text):
	print(" ")
	print("Results:")
	print("Ate", food_eaten, "morsels of snek food total.")
	print("Final length:", tail_length)
	print("Screen coverage: " + str((len(tail) * 100) / (max)) + "%")
	
	buffer = 5
	message = font.render("Press [Space] to restart", True, (255, 255, 255))
	pygame.draw.rect(screen, (0, 0, 0),  pygame.Rect(width // 2 - message.get_width() // 2 - buffer, height // 2 - message.get_height() // 2 - buffer + font_size + 2 * buffer, message.get_width() + buffer * 2, message.get_height() + buffer * 2))
	screen.blit(message, (width // 2 - message.get_width() // 2, height // 2 - message.get_height() // 2 + font_size + 2 * buffer))
	
	display_message(text)
	
	while not True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
				return True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return False
		clock.tick(framerate) # wait for 1/framerate seconds
		

def play():
	reset_globals()
	global x
	global y
			
	count = 0 # used to count frames since last snek update
	direction = 0 # int 0-3 corresponding to the direction of movement
	prev_direction = 0 # used to check new direction to prevent going straight back into tail
	print(" ")
	print("New snek game commencing:")

	exit = False
	done = False
	while not (done or exit): 
		count += 1
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
				exit = True
			
		pressed = pygame.key.get_pressed() # get list of pressed keys (these are update every frame)
		if pressed[pygame.K_UP] and prev_direction != 1: direction = 3 # set new direction and check against previous direction
		if pressed[pygame.K_DOWN] and prev_direction != 3: direction = 1
		if pressed[pygame.K_LEFT] and prev_direction != 0: direction = 2
		if pressed[pygame.K_RIGHT] and prev_direction != 2: direction = 0
		
		if count % speed == 0 and not exit: # if this is a frame we want to act on our input
			if direction == 3: y -= 1 # up
			if direction == 1: y += 1 # down 
			if direction == 2: x -= 1 # left
			if direction == 0: x += 1 # right
			prev_direction = direction
			
			if off_screen(x, y): # check that we are on the screen
				print("You meandered off the screen!")
				done = True
				exit = finish("You meandered off the screen!")
			
			if on_tail(x, y): # check that we aren't on our tail
				print("You munched your tail!")
				done = True
				exit = finish("You munched your tail!")
				
			increment_tail(x, y) # move tail (internally, not drawing yet)
				
			if win_check(): # check that we haven't used all the space
				print("You win!")
				done = True
				draw()
				exit = finish("You win!")
		
			if not done: # only if we aren't done with the loop
				food_check(x, y) # manage food
				draw() # update the screen
			
			count = 0
			
		clock.tick(framerate) # wait for 1/framerate seconds
	
	if exit:
		print("Exiting...")
		return False
	return True
	
def main():
	display_message("Press [Space] to start")
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
				done = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				done = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				if not play():
					done = True
		clock.tick(framerate) # wait for 1/framerate seconds
	print("Application closed.")
	
main()
			
	
	
