import pygame
import Game

try:
    game = Game.Game()
    game.run()
except Exception as e:
    print(f"An error occurred: {e}")
    raise e
finally:
    print("Exiting...")
    pygame.quit()