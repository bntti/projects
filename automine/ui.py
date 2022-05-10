"""Draw the board"""
import math
import pygame
import config
from controls import Controls
from logic import Logic


class UI:
    """Draw the board"""

    def __init__(self, logic: Logic, control: Controls) -> None:
        self._logic = logic
        self._controls = control

        self.screen = pygame.display.set_mode((
            config.WIDTH * config.TILE_SIZE, config.HEIGHT * config.TILE_SIZE
        ))

    def draw_image(self, left_x: int, top_y: int, bg_color: tuple[int, int, int], path: str) -> None:
        """Draw image.

        Args:
            left_x (int): X of the left side of the image.
            top_y (int): Y of the top side of the image.
            bg_color (tuple): Background color.
            path (str): Path tho the image.
        """
        pygame.draw.rect(self.screen, bg_color, pygame.Rect(
            left_x + 1, top_y + 1, config.TILE_SIZE - 2, config.TILE_SIZE - 2
        ))
        flag_image = pygame.image.load(path)
        self.screen.blit(flag_image, (left_x, top_y))

    def _draw_tile(self, tile_x: int, tile_y: int) -> None:
        """Draw a tile"""
        left_x = math.floor(config.TILE_SIZE * tile_x)
        top_y = math.floor(config.TILE_SIZE * tile_y)
        tile = self._logic.user_field[tile_x][tile_y]

        if tile == "flag":
            self.draw_image(left_x, top_y, (30, 30, 30), "images/flag.png")
        elif tile == "-1":
            self.draw_image(left_x, top_y, (255, 0, 0), "images/mine.png")
        else:
            color = (30, 30, 30) if tile == "hidden" else (50, 50, 50)
            pygame.draw.rect(self.screen, color, pygame.Rect(
                left_x + 1, top_y + 1, config.TILE_SIZE - 2, config.TILE_SIZE - 2
            ))

            if tile != "hidden" and int(tile) > 0:
                font = pygame.font.Font('freesansbold.ttf', config.TILE_SIZE)
                text = font.render(str(tile), True, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.center = (
                    left_x + config.TILE_SIZE // 2,
                    top_y + config.TILE_SIZE // 2
                )
                self.screen.blit(text, text_rect)

    def draw(self) -> None:
        """Draw the board"""
        self.screen.fill((0, 0, 0))

        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                self._draw_tile(tile_x, tile_y)

        selected_tile = self._controls.selected_tile
        if selected_tile["visible"]:
            surface = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
            surface.set_alpha(128)
            surface.fill((255, 255, 255))
            self.screen.blit(surface, (
                selected_tile["x"] * config.TILE_SIZE,
                selected_tile["y"] * config.TILE_SIZE
            ))

        pygame.display.flip()
