import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#define game variables
clicked = False
level = 4
#game window
tile_size = 35
cols = 20
margin = 100
window_width = tile_size * cols
window_height = (tile_size * cols) + margin

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Level Editor')

# Game States 
# leve images
level1_img = pygame.image.load('img/level1.png')
level2_img = pygame.image.load('img/level2.png')
level3_img = pygame.image.load('img/level3.png')
level4_img = pygame.image.load('img/level4.png')
level5_img = pygame.image.load('img/level5.png')
level6_img = pygame.image.load('img/level6.png')
level7_img = pygame.image.load('img/level7.png')
level8_img = pygame.image.load('img/level8.png')
level9_img = pygame.image.load('img/level9.png')

# Load buttons
restart_btn_img = pygame.image.load('img/restart_btn.png')
play_btn_img = pygame.image.load('img/play_btn.png')
setting_btn_img = pygame.image.load('img/setting_btn.png')
back_btn_img = pygame.image.load('img/backward.png')
about_us_btn_img = pygame.image.load('img/About_us_btn.png')
music_on_btn_img = pygame.image.load('img/music_on_btn.png')
music_off_btn_img = pygame.image.load('img/music_off_btn.png')
menu_btn_img = pygame.image.load('img/menu.png')
next_btn_img = pygame.image.load('img/next_level_btn.png')
home_btn_img = pygame.image.load('img/home.png')
#load images
sun_img = pygame.image.load('img/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
game_play_img = pygame.image.load('img/sky.jpg')
game_play_img = pygame.transform.scale(game_play_img, (window_width, window_height - margin))
dirt_img = pygame.image.load('img/dirt.png')
grass_img = pygame.image.load('img/grass.png')
blob_img = pygame.image.load('img/blob.png')
platform_x_img = pygame.image.load('img/platform_x.png')
platform_y_img = pygame.image.load('img/platform_y.png')
lava_img = pygame.image.load('img/lava.png')
coin_img = pygame.image.load('img/coin.png')
exit_img = pygame.image.load('img/exit.png')
save_img = pygame.image.load('img/save_btn.png')
load_img = pygame.image.load('img/load_btn.png')
setting_img = pygame.image.load('img/setting_text.png')
setting_btn_big_img = pygame.image.load('img/setting_btn_big.png')
select_level_img = pygame.image.load('img/select_level_text.png')
you_fail_img = pygame.image.load('img/you_fail_text.png')
you_won_img = pygame.image.load('img/you_won_text.png')
# names 
chitra_img = pygame.image.load('img/chitra_text.png')
diksha_img = pygame.image.load('img/diksha_text.png')
garima_img = pygame.image.load('img/garima_text.png')
samman_img = pygame.image.load('img/samman_text.png')
members_img = pygame.image.load('img/members_text.png')



#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

# #create boundary
# for tile in range(0, 20):
# 	world_data[19][tile] = 2
# 	world_data[0][tile] = 1
# 	world_data[tile][0] = 1
# 	world_data[tile][19] = 1

#function for outputting text onto the window
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	window.blit(img, (x, y))

def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(window, white, (c * tile_size, 0), (c * tile_size, window_height - margin))
		#horizontal lines
		pygame.draw.line(window, white, (0, c * tile_size), (window_width, c * tile_size))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#enemy blocks
					img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
					window.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					window.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					window.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					window.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
				if world_data[row][col] == 9:
					# play button of menu
					img = pygame.transform.scale(play_btn_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10:
					# setting button of menu
					img = pygame.transform.scale(setting_btn_big_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 11:
					# music on button of setting
					img = pygame.transform.scale(music_on_btn_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12:
					# music off button of setting
					img = pygame.transform.scale(music_off_btn_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 13:
					# back button of setting
					img = pygame.transform.scale(back_btn_img, (tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 14:
					# about us button of menu
					img = pygame.transform.scale(about_us_btn_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 15:
					# level1 button of select level
					img = pygame.transform.scale(level1_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 16:
					# level2 button of select level
					img = pygame.transform.scale(level2_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 17:
					# level3 button of select level
					img = pygame.transform.scale(level3_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 18:
					# level4 button of select level
					img = pygame.transform.scale(level4_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 19:
					# level5 button of select level
					img = pygame.transform.scale(level5_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 20:
					# level6 button of select level
					img = pygame.transform.scale(level6_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 21:
					# level7 button of select level
					img = pygame.transform.scale(level7_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 22:
					# level8 button of select level
					img = pygame.transform.scale(level8_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 23:
					# level9 button of select level
					img = pygame.transform.scale(level9_img, (2 * tile_size, 2 * tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 24:
					# menu button of game play
					img = pygame.transform.scale(menu_btn_img, (tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 25:
					# restart button of game play
					img = pygame.transform.scale(restart_btn_img, (3*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 26:
					# next button of game play
					img = pygame.transform.scale(next_btn_img, (2*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 27:
					# setting text
					img = pygame.transform.scale(setting_img, (6*tile_size, 3*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 28:
					# you won text
					img = pygame.transform.scale(you_won_img, (5*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 29:
					# you fail text
					img = pygame.transform.scale(you_fail_img, (5*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 30:
					# setting_btn_img
					img = pygame.transform.scale(setting_btn_img, (4*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 31:
					# select_level_text_img
					img = pygame.transform.scale(select_level_img, (6*tile_size, 3*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 32:
					# home button of game play
					img = pygame.transform.scale(home_btn_img, (tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 33:
					# chitra text
					img = pygame.transform.scale(chitra_img, (6*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 34:
					# diksha text
					img = pygame.transform.scale(diksha_img, (6*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 35:
					# garima text
					img = pygame.transform.scale(garima_img, (6*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 36:
					# samman text
					img = pygame.transform.scale(samman_img, (6*tile_size, tile_size))
					window.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 37:
					# members
					img = pygame.transform.scale(members_img, (8*tile_size, 2*tile_size))
					window.blit(img, (col * tile_size, row * tile_size))

class Button():
	def __init__(self, image, x, y):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		window.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(save_img ,window_width // 2 - 150, window_height - 80)
load_button = Button(load_img ,window_width // 2 + 50, window_height - 80)

#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	window.fill(green)
	window.blit(game_play_img, (0, 0))
	window.blit(sun_img, (tile_size * 2, tile_size * 2))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, window_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, window_height - 40)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 20 and y < 20:
				#update tile value
				if pygame.mouse.get_pressed()[0]:
					world_data[y][x] += 1
					if world_data[y][x] > 37:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2]:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 37
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()