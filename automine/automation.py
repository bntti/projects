"""Automate a part of the game"""
import config
from logic import Logic


class Automation:
    """Automate a part of the game"""

    def __init__(self, logic: Logic) -> None:
        self._logic = logic

    def autoclear(self) -> bool:
        """Automatically open closed tiles next to satisfied empty tiles

        Returns:
            bool: True if lost the game
        """
        loss = False
        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                if self._logic.user_field[tile_x][tile_y] in ["hidden", "flag"]:
                    continue
                lost = self._logic.action(tile_x, tile_y, True)
                if lost:
                    loss = True
        return loss

    def autoflag(self) -> bool:
        """Automatically add trivial flags

        Returns:
            bool: True if flags were added
        """
        flagged = False
        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                if self._logic.user_field[tile_x][tile_y] == "hidden":
                    continue
                hidden_count = self.get_nearby_hidden_count(tile_x, tile_y)
                if (
                    hidden_count > 0
                    and hidden_count == self._logic.game_field[tile_x][tile_y]
                ):
                    self.flag_nearby(tile_x, tile_y)
                    flagged = True
        return flagged

    def get_nearby_hidden_count(self, tile_x: int, tile_y: int) -> int:
        """Get number of hidden tiles around specified tile

        Returns:
            int: Number of hidden tiles around tile
        """
        hidden_count = 0
        for new_x in range(tile_x - 1, tile_x + 2):
            for new_y in range(tile_y - 1, tile_y + 2):
                if new_x == tile_x and new_y == tile_y:
                    continue
                if 0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT:
                    if self._logic.user_field[new_x][new_y] in ["hidden", "flag"]:
                        hidden_count += 1
        return hidden_count

    def flag_nearby(self, tile_x: int, tile_y: int) -> None:
        """Flag all hidden tiles around specified tile"""
        for new_x in range(tile_x - 1, tile_x + 2):
            for new_y in range(tile_y - 1, tile_y + 2):
                if new_x == tile_x and new_y == tile_y:
                    continue
                if 0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT:
                    if self._logic.user_field[new_x][new_y] == "hidden":
                        self._logic.user_field[new_x][new_y] = "flag"
