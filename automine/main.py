"""Main"""
import time
import pygame
import config
from controls import Controls
from logic import Logic
from ui import UI
from automation import Automation


def main():
    """Run program"""
    pygame.init()
    clock = pygame.time.Clock()

    logic = Logic()
    automation = Automation(logic)
    controls = Controls(logic, automation)
    game_ui = UI(logic, controls)

    while not controls.quit:
        controls.handle_controls()

        if controls.update_screen:
            win = logic.check_win()
            if win:
                controls.game_over = True
                print(f"Finished in {time.time() - logic.starting_time}")
            game_ui.draw()
            controls.update_screen = False

        if controls.game_over:
            # TODO: game over text
            time.sleep(1)

        # Time
        clock.tick(config.FPS)


if __name__ == "__main__":
    main()
