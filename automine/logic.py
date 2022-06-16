"""Manage game"""
import random
import time
import config

MINE = -1


class Logic:
    """Manage game"""

    def __init__(self) -> None:
        self.created = False
        self.starting_time = 0
        self.game_field = [
            [0 for _ in range(config.HEIGHT)] for _ in range(config.WIDTH)
        ]
        self.user_field = [
            ["hidden" for _ in range(config.HEIGHT)] for _ in range(config.WIDTH)
        ]

    def create(self, start_x: int, start_y: int) -> None:
        """Create minefield"""
        self.created = True
        self.starting_time = time.time()

        possible_mines = []
        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                # Omit tiles right next to starting tile
                if abs(tile_x - start_x) > 1 or abs(tile_y - start_y) > 1:
                    possible_mines.append((tile_x, tile_y))

        random.shuffle(possible_mines)
        for i in range(config.MINE_COUNT):
            mine_x, mine_y = possible_mines[i]
            self.game_field[mine_x][mine_y] = MINE

        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                if self.game_field[tile_x][tile_y] == MINE:
                    continue

                nearby_mine_count = 0
                for new_x in range(tile_x - 1, tile_x + 2):
                    for new_y in range(tile_y - 1, tile_y + 2):
                        if 0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT:
                            if self.game_field[new_x][new_y] == MINE:
                                nearby_mine_count += 1

                self.game_field[tile_x][tile_y] = nearby_mine_count

    def reveal(self, start_x: int, start_y: int) -> None:
        """Reveal tiles starting from specified tile"""
        tiles = [(start_x, start_y)]
        while len(tiles) > 0:
            tile_x, tile_y = tiles.pop(0)

            for x_dir in range(-1, 2):
                for y_dir in range(-1, 2):
                    new_x = tile_x + x_dir
                    new_y = tile_y + y_dir
                    if not (0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT):
                        continue

                    if (
                        self.user_field[new_x][new_y] == "hidden"
                        and self.game_field[new_x][new_y] == 0
                    ):
                        tiles.append((new_x, new_y))
                        self.user_field[new_x][new_y] = "0"

                    if self.game_field[tile_x][tile_y] == 0 or (
                        x_dir == 0 and y_dir == 0
                    ):
                        self.user_field[new_x][new_y] = str(
                            self.game_field[new_x][new_y]
                        )

    def quick_reveal(self, tile_x: int, tile_y: int) -> bool:
        """Reveal nearby tiles when clicking a revealed tile and the correct number of flags are nearby

        Returns:
            bool: True if the game was lost
        """
        flag_amount = 0
        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                new_x = tile_x + x_dir
                new_y = tile_y + y_dir
                if 0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT:
                    if self.user_field[new_x][new_y] == "flag":
                        flag_amount += 1

        if flag_amount != int(self.user_field[tile_x][tile_y]):
            return False

        lost = False
        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                new_x = tile_x + x_dir
                new_y = tile_y + y_dir
                if 0 <= new_x < config.WIDTH and 0 <= new_y < config.HEIGHT:
                    if self.user_field[new_x][new_y] == "hidden":
                        mine_hit = self.action(new_x, new_y, True)
                        if mine_hit:
                            lost = True
        return lost

    def action(self, tile_x: int, tile_y: int, left_click: bool) -> bool:
        """User action.

        Args:
            tile_x (int): X of the selected tile.
            tile_y (int): Y of the selected tile.
            left_click (bool): True if click was a left click.

        Returns:
            bool: True if game is over.
        """
        user_tile = self.user_field[tile_x][tile_y]
        game_tile = self.game_field[tile_x][tile_y]

        if not left_click:
            if user_tile == "hidden" and user_tile != "flag":
                self.user_field[tile_x][tile_y] = "flag"
            elif user_tile == "flag":
                self.user_field[tile_x][tile_y] = "hidden"

        else:
            if user_tile == "hidden" and game_tile == -1:
                self.reveal(tile_x, tile_y)
                return True
            if user_tile == "hidden":
                self.reveal(tile_x, tile_y)
            elif user_tile != "flag":
                return self.quick_reveal(tile_x, tile_y)
        return False

    def check_win(self) -> bool:
        """Check for win

        Returns:
            bool: True if game was won, otherwise False
        """
        for tile_x in range(config.WIDTH):
            for tile_y in range(config.HEIGHT):
                if self.game_field[tile_x][tile_y] != -1:
                    if self.user_field[tile_x][tile_y] != str(
                        self.game_field[tile_x][tile_y]
                    ):
                        return False
        return True
