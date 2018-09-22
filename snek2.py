import pygame
import random as r

unit = 40 # size of individual square in pixels
count_w = 64 # width in units
count_h = 35 # height in units
font_size = 20

# 40, 63, 33 for full screen

framerate = 60 # frames per second
speed = 10 # number of frames between movement
tail_growth = 10 # increase in tail length for each food eaten
starting_tail_length = 20 # starting length of tail
extra_food_chance = 3 # percent probability of adding extra food

width = count_w * unit # screen width in pixels
height = count_h * unit + font_size # screen height in pixels
max = count_w * count_h

pygame.init()
pygame.display.set_caption("snek2.py")
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN) # initialize game window
font = pygame.font.SysFont("consolas", font_size)
clock = pygame.time.Clock()

food_locations = []
white = (255, 255, 255)

class Snek:
	prev_direction = int
	message = ""
	food_eaten = 0
	
	def __init__(self, name, color, position, tail_length):
		self.x = position[0]
		self.y = position[1]
		self.tail = [(self.x, self.y)] # list of pairs making the tail, initialize with a pair
		self.tail_length = tail_length # int length of tail
		self.color = color # (red, green, blue) int tuple
		self.name = name
		
	def off_screen(self):
		if self.x < 0 or self.x > count_w - 1: # x location is out of bounds
			return True
		if self.y < 0 or self.y > count_h - 1: # y location is out of bounds
			return True
		return False # x and y are on screen
	
	def on_tail(self):
		if ((self.x, self.y)) in self.tail: # coordinates are in tail list
			return True
		return False
		
	def increment_tail(self):
		self.tail.append(self.tail[-1]) # put last element in list again on the end of list ([a, b, c] would become [a, b, c, c])
		for i in range(len(self.tail) - 1, 0, -1): # move from end of list to beginning
			self.tail[i] = self.tail[i - 1] # scoot element to the right
		self.tail[0] = (self.x, self.y) # first element becomes current head of snek now that space has been made
		del self.tail[self.tail_length:] # trim the tail to the right length (by deleting extra from the end)
		
	def eat(self):
		self.tail_length += tail_growth # max tail size increases
		self.food_eaten += 1
		print("Yum! " + self.name + " is now", self.tail_length, "snek units long.")
		
	def update(self, direction):
		if direction == 3: self.y -= 1 # up
		if direction == 1: self.y += 1 # down 
		if direction == 2: self.x -= 1 # left
		if direction == 0: self.x += 1 # right
		self.prev_direction = direction
		
		if self.off_screen(): # check that we are on the screen
			print(self.name + " meandered off the screen...")
			self.message = self.name + " meandered off the screen..."
			return False
		
		if self.on_tail(): # check that we aren't on our tail
			print(self.name + " munched their own tail...")
			self.message = self.name + " munched their own tail..."
			return False
			
		self.increment_tail() # move tail (internally, not drawing yet)
		return True
	
	def draw(self):
	
		size = max // 10
		start = 200
			
		for i in range(len(self.tail)):
		
			red = start - start * (i / size)
			green = start - start * (i / size)
			blue = start - start * (i / size)
			
			if red < self.color[0]: red = self.color[0]
			if green < self.color[1]: green = self.color[1]
			if blue < self.color[2]: blue = self.color[2]
			pygame.draw.rect(screen, (red, green, blue), pygame.Rect(self.tail[i][0] * unit, self.tail[i][1] * unit + font_size, unit, unit)) # multiply by unit to make squares the right size

	
def food(all_tails):
	while True: # keep trying to find valid coordinates (we must be sure there are free spaces before calling this function or we will get an infinite loop)
		x = r.randint(0, count_w - 1)
		y = r.randint(0, count_h - 1)
		if ((x, y)) not in all_tails: # coordinates are in free space
			return (x, y)

def food_check(snek): 
	global food_locations # specify global so python interpreter knows to use the existing variable
	for food in food_locations:
		if food == (snek.x, snek.y): # if snek happens to be on the food
			snek.eat()
			food_locations.remove(food)
			return True
	return False
	
def tie_check(snek_1, snek_2):
	if snek_1.x == snek_2.x and snek_1.y == snek_2.y:
		return True
	return False
	
def chomp_check(snek_1, snek_2):
	for coords in snek_2.tail:
		if snek_1.x == coords[0] and snek_1.y == coords[1]:
			return True # snek is chomped
	return False
	
def win_check(all_tails):
	if len(all_tails) >= max: # tail is at the maximum length that fits on the screen
		return True # game is won
	return False # otherwise we have not won

def draw_food():
	for food in food_locations:
		pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0] * unit, food[1] * unit + font_size, unit, unit)) # put food on the screen
	
def draw_header(snek, position):
	next_pos = position
	name_text = font.render(snek.name, True, snek.color)
	screen.blit(name_text, (next_pos, 0))
	next_pos += name_text.get_width() 
	
	length_text = font.render("  Length: {} ".format(len(snek.tail)), True, white)
	screen.blit(length_text, (next_pos, 0))
	next_pos += length_text.get_width()
	
	if snek.tail_length - len(snek.tail) > 0:
		extra_food_text = font.render("+{:<2} ".format(snek.tail_length - len(snek.tail)), True, (255, 0, 0))
		screen.blit(extra_food_text, (next_pos, 0))
	next_pos = position + name_text.get_width() + font_size * 10
	
	food_text = font.render("Food eaten: " + str(snek.food_eaten), True, white)
	screen.blit(food_text, (next_pos, 0))
	next_pos += food_text.get_width()
		
	screen_text = font.render("  Coverage: {:<4.1f}%".format((len(snek.tail) * 100) / (max)), True, white)
	screen.blit(screen_text, (next_pos, 0))
	
def display_message(text_list):
	buffer = 5
	for i in range(len(text_list)):
		if text_list[i][0] != "": # ignore empty messages
			message = font.render(text_list[i][0], True, text_list[i][1]) # create message for pygame
			pygame.draw.rect(screen, (0, 0, 0),  pygame.Rect(width // 2 - message.get_width() // 2 - buffer, height // 2 - message.get_height() // 2 - buffer  + (i - len(text_list) // 2) * (message.get_height() + 2 * buffer), message.get_width() + buffer * 2, message.get_height() + buffer * 2))
			screen.blit(message, ((width // 2 - message.get_width() // 2), (height // 2 - message.get_height() // 2) + (i - len(text_list) // 2) * (message.get_height() + 2 * buffer)))
	pygame.display.flip() # updates display
	
def finish():
	while not True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
				return True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return False
		clock.tick(framerate) # wait for 1/framerate seconds
		

def play():	
	count = 0 # used to count frames since last snek update
	direction_1 = 2 # int 0-3 corresponding to the direction of movement
	direction_2 = 0
	snek_1_crash = False
	snek_2_crash = False
	
	global food_locations
	food_locations = [(count_w // 2, count_h // 2)]
	
	print(" ")
	print("New snek game commencing:")
	
	snek_1 = Snek("Snek 1", (240, 240, 60), (count_w - 1, count_h - 1), starting_tail_length)
	snek_2 = Snek("Snek 2", (240, 60, 240), (0, 0), starting_tail_length)

	exit = False
	done = False
	while not (done or exit): 
		count += 1
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
				exit = True
			
		pressed = pygame.key.get_pressed() # get list of pressed keys (these are update every frame)
		if pressed[pygame.K_UP] and snek_1.prev_direction != 1: direction_1 = 3 # set new direction and check against previous direction
		if pressed[pygame.K_DOWN] and snek_1.prev_direction != 3: direction_1 = 1
		if pressed[pygame.K_LEFT] and snek_1.prev_direction != 0: direction_1 = 2
		if pressed[pygame.K_RIGHT] and snek_1.prev_direction != 2: direction_1 = 0
		
		if pressed[pygame.K_w] and snek_2.prev_direction != 1: direction_2 = 3 # set new direction and check against previous direction
		if pressed[pygame.K_s] and snek_2.prev_direction != 3: direction_2 = 1
		if pressed[pygame.K_a] and snek_2.prev_direction != 0: direction_2 = 2
		if pressed[pygame.K_d] and snek_2.prev_direction != 2: direction_2 = 0
		
		if count % speed == 0 and not exit: # if this is a frame we want to act on our input
			if not snek_1.update(direction_1):
				snek_1_crash = True
				
			if not snek_2.update(direction_2):
				snek_2_crash = True
				
			if snek_1_crash and snek_2_crash:
				display_message([("You tied.", white), ("", white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
			
			if not done and snek_1_crash:
				display_message([(snek_2.name + " wins!", snek_2.color), ("", white), (snek_1.message, white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
				
			if not done and snek_2_crash:
				display_message([(snek_1.name + " wins!", snek_1.color), ("", white), (snek_2.message, white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
				
				
			if not done and tie_check(snek_1, snek_2):
				display_message([("You tied.", white), ("", white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
				
			if not done and chomp_check(snek_1, snek_2):
				display_message([(snek_2.name + " wins!", snek_2.color), ("", white), (snek_1.name + " mistakenly chomped his friend", white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
				
			if not done and chomp_check(snek_2, snek_1):
				display_message([(snek_1.name + " wins!", snek_1.color), ("", white), (snek_2.name + " mistakenly chomped his friend", white), ("Press [Space] to restart", white)])
				done = True
				exit = finish()
				
				
			if not done and win_check(snek_1.tail + snek_2.tail): # check that we haven't used all the space
				screen.fill((0, 0, 0)) # fill screen with black so we can re-draw from scratch
				draw_header()
				draw_food()
				snek_2.draw() # draw our snek
				snek_1.draw()
				display_message([("You tied.", white), ("", white), ("Press [Space] to restart", white)])
				pygame.display.flip() # update display
				
				done = True
				exit = finish()
		
			if not done: # only if we aren't done with the loop
				if food_check(snek_1): # manage food
					food_locations.append(food(snek_1.tail + snek_2.tail)) # get a new food location
				if food_check(snek_2): # manage food
					food_locations.append(food(snek_1.tail + snek_2.tail)) # get a new food location
				if r.randint(0, 99) < extra_food_chance:
					food_locations.append(food(snek_1.tail + snek_2.tail)) # get a new food location
					
				screen.fill((0, 0, 0)) # fill screen with black so we can re-draw from scratch
				draw_header(snek_2, 0)
				draw_header(snek_1, width // 2)
				draw_food()
				snek_1.draw() # draw our snek
				snek_2.draw()
				pygame.display.flip() # update display
				
			count = 0
			
		clock.tick(framerate) # wait for 1/framerate seconds
	
	if exit:
		print("Exiting...")
		return False
	return True
	
def main():
	display_message([("Press [Space] to start", white)])
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
			
	
	
