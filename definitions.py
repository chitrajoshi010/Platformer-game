import pygame
import pygame.font
from pygame import mixer
from enum import Enum

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Define the game states
class GameState(Enum):
    MENU = 1
    SETTING = 2
    ABOUT_US = 3
    LEVEL_SELECT = 4
    GAME = 5
    YOU_FAIL = 6
    GAME_OVER = 7


# Define the game variables
window_width = 1000
window_height = 800
tile_width = window_width // 20
tile_height = window_height // 20
game_over = 0
file = 1
level = 1
total_levels = 9
score = 0

# Define fonts
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Define colours
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

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
# BACK GROUND IMAGES
main_menu_img = pygame.image.load('img/main_menu.jpg')
main_menu_img = pygame.transform.scale(main_menu_img, (window_width, window_height))
level_select_bk_img = pygame.image.load('img/select_level.jpg')
level_select_bk_img = pygame.transform.scale(level_select_bk_img, (window_width, window_height))
game_play_img = pygame.image.load('img/sky.jpg')
game_play_img = pygame.transform.scale(game_play_img, (window_width, window_height))
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
chitra_img = pygame.image.load('img/chitra_text_img.png')
prepared_by_img = pygame.image.load('img/prepared_text_img.png')

# Load sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.ogg')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)
button_click_fx = pygame.mixer.Sound('img/buttonClick.wav')
button_click_fx.set_volume(0.5)