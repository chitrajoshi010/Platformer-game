import pygame
from pygame.locals import *
import pickle
from os import path
import definitions as defs
from definitions import GameState
from assets import Player, World, Platform, Coin, Lava, Exit, draw_text

pygame.init()

class Game():
    def __init__(self):
        self.window = pygame.display.set_mode((defs.window_width, defs.window_height))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.current_state = GameState.MENU
        self.music_on = True  # Add this line to track the music state

        # Load in level data and create world
        if path.exists(f'level{defs.file}_data'):
            with open(f'level{defs.file}_data', 'rb') as pickle_in:
                world_data = pickle.load(pickle_in)
        else:
            world_data = []
        self.world = World(world_data)
        self.player = Player(100, defs.window_height - 130, self.world)
        # Create dummy coin for showing the defs.score
        defs.score_coin = Coin(defs.tile_width // 2, defs.tile_height // 2)
        self.world.coin_group.add(defs.score_coin)

    def state_transition(self):
        if self.current_state == GameState.MENU:
            self.draw_background(defs.main_menu_img, self.window)
            defs.game_over = 0
        elif self.current_state == GameState.SETTING:
            self.draw_background(defs.main_menu_img, self.window)
            defs.game_over = 0
        elif self.current_state == GameState.ABOUT_US:
            self.draw_background(defs.main_menu_img, self.window)
            defs.game_over = 0
        elif self.current_state == GameState.LEVEL_SELECT:
            self.draw_background(defs.level_select_bk_img, self.window)
            defs.game_over = 0
        elif self.current_state == GameState.GAME:
            self.draw_background(defs.game_play_img, self.window)
            if defs.game_over == 0:
                self.world.blob_group.update()
                self.world.platform_group.update()
                #update defs.score
                #check if a coin has been collected
                if pygame.sprite.spritecollide(self.player, self.world.coin_group, True):
                    defs.score += 1
                    defs.coin_fx.play()
                draw_text('X ' + str(defs.score), defs.font_score, defs.white, defs.tile_width - 10, defs.tile_height, self.window)
            
            self.world.blob_group.draw(self.window)
            self.world.platform_group.draw(self.window)
            self.world.lava_group.draw(self.window)
            self.world.coin_group.draw(self.window)
            self.world.exit_group.draw(self.window)

            defs.game_over = self.player.update(defs.game_over, self.window)

            #if player has died
            if defs.game_over == -1:
                defs.score = 0
                self.current_state = GameState.YOU_FAIL

            #if player has completed the level
            if defs.game_over == 1:
                #reset game and go to next level
                self.current_state = GameState.GAME_OVER
                defs.file += 1
                defs.score = 0

        elif self.current_state == GameState.YOU_FAIL:
            self.reset_level(13)
            self.draw_background(defs.main_menu_img, self.window)
            defs.game_over = 0
        elif self.current_state == GameState.GAME_OVER:
            self.reset_level(14)
            self.draw_background(defs.main_menu_img, self.window)
            defs.game_over = 0
            

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            # Iterate over world tile list; each item is (tile_id, img, rect)
            for tile_data in self.world.tile_list:
                tile_id, img, rect = tile_data
                # Define which tile_ids are clickable buttons
                clickable_ids = {9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32}
                if tile_id in clickable_ids:
                    if rect.collidepoint(mouse_pos):
                        action = self.getActionForTile(tile_id)
                        if action:
                            action()
                            defs.button_click_fx.play()
                        break

    def getActionForTile(self, tile_id):
        # Adjust these mappings based on your game logic and current state.
        if self.current_state == GameState.MENU:
            if tile_id == 9:  # Play button
                return lambda: self.setState(GameState.LEVEL_SELECT, 3)
            elif tile_id == 10:  # Settings button
                return lambda: self.setState(GameState.SETTING, 2)
        elif self.current_state == GameState.SETTING:
            if tile_id == 11:  # Music On button
                return self.toggle_music
            elif tile_id == 13:  # Back button
                return lambda: self.setState(GameState.MENU, 1)
            elif tile_id == 14:  # About Us button
                return lambda: self.setState(GameState.ABOUT_US, 15)
        elif self.current_state == GameState.ABOUT_US:
            if tile_id == 13:  #back button
                return lambda: self.setState(GameState.SETTING, 2)
        elif self.current_state == GameState.LEVEL_SELECT:
            # Map level buttons (tile IDs 15 to 23) to starting the game on the selected level.
            if tile_id == 15:
                return lambda: self.setState(GameState.GAME, 4, 1)
            elif tile_id == 16:
                return lambda: self.setState(GameState.GAME, 5, 2)
            elif tile_id == 17:
                return lambda: self.setState(GameState.GAME, 6, 3)
            elif tile_id == 18:
                return lambda: self.setState(GameState.GAME, 7, 4)
            elif tile_id == 19:
                return lambda: self.setState(GameState.GAME, 8, 5)
            elif tile_id == 20:
                return lambda: self.setState(GameState.GAME, 9, 6)
            elif tile_id == 21:
                return lambda: self.setState(GameState.GAME, 10, 7)
            elif tile_id == 22:
                return lambda: self.setState(GameState.GAME, 11, 8)
            elif tile_id == 23:
                return lambda: self.setState(GameState.GAME, 12, 9)
            elif tile_id == 13:  #back button
                return lambda: self.setState(GameState.MENU, 1)
        elif self.current_state == GameState.GAME:
            if tile_id == 24:  # Menu button in gameplay
                return lambda: self.setState(GameState.LEVEL_SELECT, 3)
        elif self.current_state == GameState.YOU_FAIL:
            if tile_id == 25:  # Restart button
                return lambda: self.setState(GameState.GAME, defs.file)
            elif tile_id == 32:  # Home button
                return lambda: self.setState(GameState.MENU, 1)
        elif self.current_state == GameState.GAME_OVER:
            if tile_id == 26:  # Next button
                if defs.level < defs.total_levels:
                    return lambda: self.setState(GameState.GAME, defs.file)
                else:
                    defs.file = 3
                    return lambda: self.setState(GameState.LEVEL_SELECT, defs.file)
            elif tile_id == 32:  # Home button
                return lambda: self.setState(GameState.MENU, 1)
        return None

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def setState(self, state, file_level, actual_level = 1):
        defs.level = actual_level
        self.current_state = state
        defs.file = file_level
        self.reset_level(defs.file)

    def draw_background(self, img, window):
        self.window.blit(img, (0,0))
        self.world.draw(window)

    def run(self):
        run = True
        while run:
            self.clock.tick(self.fps)
            self.window.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                self.handle_events(event)

            self.state_transition()
            pygame.display.update()
        pygame.quit()

    # Function to reset a level
    def reset_level(self, lvl):
        self.player.reset(100, defs.window_height - 130)
        self.world.blob_group.empty()
        self.world.platform_group.empty()
        self.world.coin_group.empty()
        self.world.lava_group.empty()
        self.world.exit_group.empty()

        # Load in level data and create world
        if path.exists(f'level{lvl}_data'):
            with open(f'level{lvl}_data', 'rb') as pickle_in:
                world_data = pickle.load(pickle_in)
        else:
            world_data = []
        self.world = World(world_data)
        self.player.world = self.world