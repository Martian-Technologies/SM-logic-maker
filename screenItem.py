import pygame
from helpers import Helpers
from main import App
from pygame import Vector2 as Vec


class ScreenItem:
    """
    A base class for all screen items.
    """

    def __init__(self, name=None) -> None:
        """
        Initializes a new instance of the ScreenItem class.

        Args:
        - name: A string representing the name of the screen item.
        """
        self.ID = None
        self.name = name
        self.itemManager = None
        self.app: App = None

    def initInWin(self):
        """
        Initializes the screen item in the window.
        """
        pass

    def draw(self):
        """
        Draws the screen item.
        """
        pass

    def handleEvents(self, events: list[pygame.event.Event]):
        """
        Handles the events for the screen item.

        Args:
        - events: A list of pygame events.
        """
        pass

    def update(self):
        """
        Updates the screen item.
        """
        pass


class ScreenSpriteItem(ScreenItem):
    """
    A class representing a screen item with a sprite.
    """

    def __init__(self, sprite: pygame.surface.Surface, pos: Vec, name: str = None) -> None:
        """
        Initializes a new instance of the ScreenSpriteItem class.

        Args:
        - sprite: A pygame surface representing the sprite of the screen item.
        - pos: A Vector2 representing the position of the screen item.
        - name: A string representing the name of the screen item.
        """
        super().__init__(name)
        self.sprite: pygame.surface.Surface = sprite
        self.pos: Vec = pos

    def screenPosToSurfPos(self, pos):
        """
        Converts the screen position to the surface position.

        Args:
        - pos: A Vector2 representing the position of the screen item.

        Returns:
        - A Vector2 representing the position of the surface.
        """
        return pos - self.pos

    def surfPosToScreenPos(self, pos):
        """
        Converts the surface position to the screen position.

        Args:
        - pos: A Vector2 representing the position of the surface.

        Returns:
        - A Vector2 representing the position of the screen item.
        """
        return pos + self.pos

    def intersectsPos(self, pos: Vec):
        """
        Checks if the position intersects with the sprite.

        Args:
        - pos: A Vector2 representing the position to check.

        Returns:
        - A boolean indicating if the position intersects with the sprite.
        """
        return Helpers.relitivePosIntersectsSurf(self.screenPosToSurfPos(pos), self.sprite)

    def isTouchingMouse(self):
        """
        Checks if the screen item is touching the mouse.

        Returns:
        - A boolean indicating if the screen item is touching the mouse.
        """
        return self.intersectsPos(Helpers.getMousePos())

    def draw(self):
        """
        Draws the screen item.
        """
        self.app.screen.blit(self.sprite, (self.pos.x, self.pos.y))

    def handleEvents(self, events: list[pygame.event.Event]):
        """
        Handles the events for the screen item.

        Args:
        - events: A list of pygame events.
        """
        pass

    def update(self):
        """
        Updates the screen item.
        """
        pass

    def updatePos(self, newPos: Vec):
        """
        Updates the position of the screen item.

        Args:
        - newPos: A Vector2 representing the new position of the screen item.
        """
        self.pos = newPos


class Button(ScreenSpriteItem):
    """
    A class representing a button screen item.
    """

    def __init__(
        self,
        sprite: pygame.surface.Surface,
        pos: Vec,
        spriteOffsetOnClick: Vec = Vec(),
        name: str = None,
    ) -> None:
        """
        Initializes a new instance of the Button class.

        Args:
        - sprite: A pygame surface representing the sprite of the button.
        - pos: A Vector2 representing the position of the button.
        - spriteOffsetOnClick: A Vector2 representing the offset of the sprite when the button is clicked.
        - name: A string representing the name of the button.
        """
        super().__init__(sprite, pos, name)
        self.clickTypes = [1]
        self.isDown: bool = False
        self.spriteOffsetOnClick: Vec = spriteOffsetOnClick

    def draw(self):
        """
        Draws the button.
        """
        if self.isDown:
            pos = self.pos + self.spriteOffsetOnClick
            self.app.screen.blit(self.sprite, (pos.x, pos.y))
        else:
            super().draw()

    def handleEvents(self, events):
        """
        Handles the events for the button.

        Args:
        - events: A list of pygame events.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                eventPos: Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if not self.isDown:
                    self.updateDownStat()
                    if self.isDown:
                        self.clicked(Vec(event.pos[0], event.pos[1]), event)
            elif event.type == pygame.MOUSEBUTTONUP:
                eventPos: Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if self.isDown:
                    self.updateDownStat()
                    if not self.isDown:
                        self.unclicked(Vec(event.pos[0], event.pos[1]), event)

            elif event.type == pygame.MOUSEMOTION:
                eventPos: Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if not self.isDown:
                    pressedButtons = self.updateDownStat()
                    if self.isDown:
                        self.motionClick(eventPos, event, pressedButtons)
                else:
                    self.updateDownStat()
                    if not self.isDown:
                        self.motionUnclick(eventPos, event)

    def updateDownStat(self):
        """
        Updates the down status of the button.

        Returns:
        - A list of integers representing the pressed buttons.
        """
        pressed = pygame.mouse.get_pressed()
        pressedButtons = []
        for i in self.clickTypes:
            if pressed[i - 1]:
                pressedButtons.append(i)
        pos: Vec = Vec(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - self.pos
        self.isDown = len(pressedButtons) != 0 and self.isTouchingMouse()
        return pressedButtons

    def updatePos(self, newPos: Vec):
        """
        Updates the position of the button.

        Args:
        - newPos: A Vector2 representing the new position of the button.
        """
        self.pos = newPos
        pos: Vec = Vec(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - self.pos
        if not self.isDown:
            pressedButtons = self.updateDownStat()
            if self.isDown:
                self.buttonMovedClick(pos, pressedButtons)
        else:
            self.updateDownStat()
            if not self.isDown:
                self.buttonMovedUnclick(pos)

    def clicked(self, eventPos: Vec, event: pygame.event.Event):
        """
        Called when the button is clicked.

        Args:
        - eventPos: A Vector2 representing the position of the event.
        - event: A pygame event.
        """
        pass

    def unclicked(self, eventPos: Vec, event: pygame.event.Event):
        """
        Called when the button is unclicked.

        Args:
        - eventPos: A Vector2 representing the position of the event.
        - event: A pygame event.
        """
        pass

    def motionClick(self, eventPos: Vec, event: pygame.event.Event, pressedButtons: list[int]):
        pass

    def motionUnclick(self, eventPos: Vec, event: pygame.event.Event):
        pass

    def buttonMovedClick(self, eventPos: Vec, pressedButtons: list[int]):
        pass

    def buttonMovedUnclick(self, eventPos: Vec):
        pass
