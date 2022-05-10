"""Control"""
import math
from typing import Sequence
import pygame
from pygame.event import Event
import config
from automation import Automation
from logic import Logic

LEFT_CLICK = 1
RIGHT_CLICK = 3


class Controls:
    """Handle controls"""

    def __init__(self, logic: Logic, automation: Automation) -> None:
        self._logic = logic
        self._automation = automation

        self.selected_tile = {
            "x": 0,
            "y": 0,
            "visible": False,
            "moved": False
        }

        pygame.key.set_repeat(config.KBD_DELAY, config.KBD_INTERVAL)
        self.update_screen = True
        self.game_over = False
        self.quit = False

    def handle_controls(self) -> None:
        """Handle controls"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_click(event)
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                self._move_tile(pressed)
                self._handle_selected_tile_action(pressed)

                if pressed[pygame.K_q]:
                    self.quit = True
                if pressed[pygame.K_w] or pressed[pygame.K_a]:
                    if self._automation.autoflag():
                        self.update_screen = True
                if pressed[pygame.K_s] or pressed[pygame.K_a]:
                    if self._automation.autoclear():
                        self.game_over = True
                    self.update_screen = True

    def _handle_mouse_click(self, mouse_event: Event) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selection_x = math.floor(mouse_x / config.TILE_SIZE)
        selection_y = math.floor(mouse_y / config.TILE_SIZE)

        if mouse_event.button == LEFT_CLICK:
            if not self._logic.created:
                self._logic.create(selection_x, selection_y)

            if self._logic.action(selection_x, selection_y, True):
                self.game_over = 1
        elif mouse_event.button == RIGHT_CLICK:
            self._logic.action(selection_x, selection_y, False)

        self.update_screen = True
        self.selected_tile["visible"] = False

    def _move_tile(self, pressed: Sequence[bool]) -> None:
        """Move tile

        Args:
            pressed (Sequence): Pressed keys.
        """
        new_x = self.selected_tile["x"]
        new_y = self.selected_tile["y"]

        if pressed[pygame.K_UP]:
            new_y -= 1
        elif pressed[pygame.K_DOWN]:
            new_y += 1
        elif pressed[pygame.K_LEFT]:
            new_x -= 1
        elif pressed[pygame.K_RIGHT]:
            new_x += 1
        else:
            return

        self.selected_tile["moved"] = True
        new_x = max(0, min(new_x, config.WIDTH - 1))
        new_y = max(0, min(new_y, config.HEIGHT - 1))
        self.selected_tile["x"] = new_x
        self.selected_tile["y"] = new_y

        self.selected_tile["visible"] = True
        self.update_screen = True

    def _handle_selected_tile_action(self, pressed: Sequence[bool]) -> None:
        """Handle action made by selected tile (opening, flagging, etc.)"""
        if not self.selected_tile["visible"]:
            return

        if pressed[pygame.K_SPACE] and pressed[pygame.K_LSHIFT]:
            self._logic.action(
                self.selected_tile["x"], self.selected_tile["y"], False)
        elif pressed[pygame.K_SPACE]:
            if not self._logic.created:
                self._logic.create(
                    self.selected_tile["x"], self.selected_tile["y"])

            lost = self._logic.action(
                self.selected_tile["x"], self.selected_tile["y"], True)
            if lost:
                self.game_over = 1

        self.update_screen = True
