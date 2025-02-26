import pygame
from definitions import *


# Function to draw text on the screen
def draw_text(text, font, text_col, x, y, window):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

# Button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, window):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        window.blit(self.image, self.rect)
        return action
    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

# Player, World, Enemy, Platform, Lava, Coin, and Exit classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.reset(x, y)

    def update(self, game_over, window):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]
            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in self.world.tile_list:
                if tile[2].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[2].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[2].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[2].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            # check for collision with enemies
            if pygame.sprite.spritecollide(self, self.world.blob_group, False):
                game_over = -1
                game_over_fx.play()
            # check for collision with lava
            if pygame.sprite.spritecollide(self, self.world.lava_group, False):
                game_over = -1
                game_over_fx.play()
            # check for collision with exit
            if pygame.sprite.spritecollide(self, self.world.exit_group, False):
                game_over = 1
            # check for collision with platforms
            for platform in self.world.platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        window.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []
        self.blob_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 3:
                    blob = Enemy(col_count * tile_width, row_count * tile_height + 15)
                    self.blob_group.add(blob)
                elif tile == 4:
                    platform = Platform(col_count * tile_width, row_count * tile_height, 1, 0)
                    self.platform_group.add(platform)
                elif tile == 5:
                    platform = Platform(col_count * tile_width, row_count * tile_height, 0, 1)
                    self.platform_group.add(platform)
                elif tile == 6:
                    lava = Lava(col_count * tile_width, row_count * tile_height + (tile_height // 2))
                    self.lava_group.add(lava)
                elif tile == 7:
                    coin = Coin(col_count * tile_width + (tile_width // 2), row_count * tile_height + (tile_height // 2))
                    self.coin_group.add(coin)
                elif tile == 8:
                    exit = Exit(col_count * tile_width, row_count * tile_height - (tile_height // 2))
                    self.exit_group.add(exit)
                elif tile == 9:
                    img = pygame.transform.scale(play_btn_img, (4*tile_width, 2*tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                if tile == 10:
                    img = pygame.transform.scale(setting_btn_big_img, (4 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 11:
                    img = pygame.transform.scale(music_on_btn_img, (4 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 12:
                    img = pygame.transform.scale(music_off_btn_img, (4 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 13:
                    img = pygame.transform.scale(back_btn_img, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 14:
                    img = pygame.transform.scale(about_us_btn_img, (4 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 15:
                    img = pygame.transform.scale(level1_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 16:
                    img = pygame.transform.scale(level2_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 17:
                    img = pygame.transform.scale(level3_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 18:
                    img = pygame.transform.scale(level4_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 19:
                    img = pygame.transform.scale(level5_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 20:
                    img = pygame.transform.scale(level6_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 21:
                    img = pygame.transform.scale(level7_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 22:
                    img = pygame.transform.scale(level8_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 23:
                    img = pygame.transform.scale(level9_img, (2 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 24:
                    img = pygame.transform.scale(menu_btn_img, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 25:
                    img = pygame.transform.scale(restart_btn_img, (3 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 26:
                    img = pygame.transform.scale(next_btn_img, (2 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 27:
                    img = pygame.transform.scale(setting_img, (6 * tile_width, 3 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 28:
                    img = pygame.transform.scale(you_won_img, (5 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 29:
                    img = pygame.transform.scale(you_fail_img, (5 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 30:
                    img = pygame.transform.scale(setting_btn_img, (4 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 31:
                    img = pygame.transform.scale(select_level_img, (6 * tile_width, 3 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 32:
                    img = pygame.transform.scale(home_btn_img, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 33:
                    img = pygame.transform.scale(chitra_img, (6 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 34:
                    img = pygame.transform.scale(diksha_img, (6 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 35:
                    img = pygame.transform.scale(garima_img, (6 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 36:
                    img = pygame.transform.scale(samman_img, (6 * tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                elif tile == 37:
                    img = pygame.transform.scale(members_img, (8 * tile_width, 2 * tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    self.tile_list.append((tile, img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self, window):
        for tile in self.tile_list:
            window.blit(tile[1], tile[2])
        self.blob_group.draw(window)
        self.platform_group.draw(window)
        self.lava_group.draw(window)
        self.coin_group.draw(window)
        self.exit_group.draw(window)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_width, tile_height // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_width, tile_height // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_width // 2, tile_height // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_width, int(tile_height * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
