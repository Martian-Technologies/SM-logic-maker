
import pathlib
from pygame import Vector2 as Vec
import pygame
from helpers import Helpers
from screenItem import ScreenSpriteItem
from keybindManager import keybinds


class LogicGridItem:
    """
    Base class for items that can be placed on a LogicGrid.
    """

    icon: pygame.surface.Surface = pygame.surface.Surface((100, 100))
    icon.fill(pygame.color.Color(100, 100, 100))

    def __init__(
        self, data=None, name: str = "base grid class", icon: pygame.surface.Surface = None
    ) -> None:
        """
        Initializes a new instance of the LogicGridItem class.

        Args:
        - data: The data to initialize the item with.
        - name: The name of the item.
        - icon: The icon to display for the item.
        """
        self.name: str = name
        self.ID: int = None
        self.pos: Vec = None
        if icon != None:
            self.icon = icon

    def getIcon(self) -> pygame.Surface:
        """
        Gets the icon for the item.

        Returns:
        - The icon for the item.
        """
        return self.icon

    def toData(self):
        """
        Converts the item to data.
        """
        pass

    @classmethod
    def getMenuIcon(cls):
        """
        Gets the icon to display in the menu for the item.

        Returns:
        - The icon to display in the menu for the item.
        """
        return cls.icon

    @staticmethod
    def dataIsType(data):
        """
        Determines if the data is of the correct type.

        Args:
        - data: The data to check.

        Returns:
        - True if the data is of the correct type, False otherwise.
        """
        pass


class testItem(LogicGridItem):
    """
    A test item that can be placed on a LogicGrid.
    """

    icon: pygame.surface.Surface = pygame.image.load(
        pathlib.Path(__file__).parent.absolute() / "assets" / "mtechloadingscreen.png"
    )
    # icon.fill(pygame.color.Color(0, 100, 0))

    def __init__(self, data=None) -> None:
        """
        Initializes a new instance of the testItem class.

        Args:
        - data: The data to initialize the item with.
        """
        super().__init__(data, "testItem", None)



class LogicGrid(ScreenSpriteItem):
    def __init__(self, pos1FromTopLeft: Vec, pos2FromBottomRight: Vec, name: str = None) -> None:
        super().__init__(None, pos1FromTopLeft, name)
        self.pos2: Vec = pos2FromBottomRight
        self.sizePix: Vec = None
        self.viewCenter: Vec = Vec(-1, 1)
        self.zoom: float = 0.5
        self.itemSpacing = 128
        self.iconSize = 100
        self.selectedPos = None
        self.selectIconEdgeThickness = 5
        self.drag_reference = None
        self.eventFunctions: list = [
            self.doPlacementEvents,
            self.doSelectionEvents,
            self.centerCameraEvent,
        ]
        self.backend: LogicGridBackend = LogicGridBackend()

    def initInWin(self):
        self.sizePix: Vec = (
            Vec(self.app.screen.get_size()[0], self.app.screen.get_size()[1]) - self.pos - self.pos2
        )
        self.blockMenu = self.app.mainLoop.block_menu
        self.centerCameraOnArea()

    def handleEvents(self, events: list[pygame.event.Event]):
        i = 0
        while i < len(events):
            delEvent = False
            for eventFunction in self.eventFunctions:
                if eventFunction(events[i]):
                    delEvent = True
                    break
            if delEvent:
                events.remove(events[i])
                continue

            event = events[i]
            if event.type == pygame.WINDOWRESIZED:
                self.sizePix: Vec = (
                    Vec(self.app.screen.get_size()[0], self.app.screen.get_size()[1])
                    - self.pos
                    - self.pos2
                )
            elif event.type == pygame.MOUSEWHEEL and self.isTouchingMouse():
                self.setZoom(self.zoom * (2 ** (event.y / 4)), True)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isTouchingMouse():
                if event.button == 3:
                    self.drag_reference = self.screenPosToGridPos(Helpers.getMousePos())
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.drag_reference = None
            elif event.type == pygame.MOUSEMOTION and self.drag_reference != None:
                self.viewCenter += self.drag_reference - self.screenPosToGridPos(
                    Helpers.getMousePos()
                )

            i += 1

    def centerCameraEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == keybinds.get("centerCamera"):
                if self.selectedPos != None and type(self.selectedPos) == tuple:
                    min_x = min(self.selectedPos[0].x, self.selectedPos[1].x)
                    max_x = max(self.selectedPos[0].x, self.selectedPos[1].x)
                    min_y = min(self.selectedPos[0].y, self.selectedPos[1].y)
                    max_y = max(self.selectedPos[0].y, self.selectedPos[1].y)
                elif len(self.backend.items) == 0:
                    min_x = None
                    max_x = None
                    min_y = None
                    max_y = None
                else:
                    min_x = min([item.pos.x for item in self.backend.items])
                    max_x = max([item.pos.x for item in self.backend.items])
                    min_y = min([item.pos.y for item in self.backend.items])
                    max_y = max([item.pos.y for item in self.backend.items])
                self.centerCameraOnArea(min_x, max_x, min_y, max_y)
                return True
        return False

    def centerCameraOnArea(self, min_x=None, max_x=None, min_y=None, max_y=None):
        if min_x == None:
            min_x = -2
        if max_x == None:
            max_x = 2
        if min_y == None:
            min_y = -2
        if max_y == None:
            max_y = 2
        vzoom = self.sizePix.x / (max_x - min_x + 5) / self.itemSpacing
        hzoom = self.sizePix.y / (max_y - min_y + 5) / self.itemSpacing
        self.setViewArea(
            Vec((min_x + max_x) / 2 + 0.5, (min_y + max_y) / 2 + 0.5), min(vzoom, hzoom) * 0.9
        )

    def doPlacementEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.isTouchingMouse():
            if event.button == 1:
                clickedPos = Helpers.floorVec(self.screenPosToGridPos(Helpers.getMousePos()))
                if self.blockMenu.selectedItem != None:
                    self.backend.addGridItem(self.blockMenu.selectedItem(), clickedPos)
                    return True
        return False

    def doSelectionEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.isTouchingMouse():
            clickedPos = Helpers.floorVec(self.screenPosToGridPos(Helpers.getMousePos()))
            if event.button == 1:
                if self.selectedPos == clickedPos:
                    self.selectedPos = None
                else:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and self.selectedPos != None:
                        if type(self.selectedPos) == tuple:
                            self.selectedPos = (self.selectedPos[0], clickedPos)
                        else:
                            self.selectedPos = (self.selectedPos, clickedPos)
                    else:
                        self.selectedPos = clickedPos
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.selectedPos != None:
                    if type(self.selectedPos) == tuple:
                        Helpers.removeItemsFromList(
                            self.backend.getItemsBetweenPos(
                                self.selectedPos[0], self.selectedPos[1]
                            ),
                            self.backend.items,
                        )
                    else:
                        self.backend.removeGridItem(pos=self.selectedPos)
                    return True
        return False

    def update(self):
        movementVec = Vec()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            movementVec.y -= 1 / self.zoom
        elif pressed[pygame.K_DOWN]:
            movementVec.y += 1 / self.zoom
        if pressed[pygame.K_LEFT]:
            movementVec.x -= 1 / self.zoom
        elif pressed[pygame.K_RIGHT]:
            movementVec.x += 1 / self.zoom
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            movementVec *= 2
        self.setVeiwCenter(self.viewCenter + movementVec * self.app.deltaTimeMS / 500)

    def draw(self):
        self.updateSprite()
        super().draw()

    def updateSprite(self):
        sprite = pygame.surface.Surface((self.sizePix.x, self.sizePix.y))
        sprite.fill(pygame.color.Color(200, 200, 200))
        if self.selectedPos != None:
            if type(self.selectedPos) == Vec:
                selectIcon = pygame.Surface((self.itemSpacing, self.itemSpacing))
                selectIcon.fill(pygame.Color(50, 50, 50, 100))
                pygame.draw.rect(
                    selectIcon,
                    pygame.color.Color(150, 150, 150, 50),
                    pygame.Rect(
                        self.selectIconEdgeThickness / self.zoom,
                        self.selectIconEdgeThickness / self.zoom,
                        self.itemSpacing - self.selectIconEdgeThickness * 2 / self.zoom,
                        self.itemSpacing - self.selectIconEdgeThickness * 2 / self.zoom,
                    ),
                )
                sprite.blit(
                    pygame.transform.scale_by(selectIcon, self.zoom),
                    Helpers.round(Helpers.vecToTulpe(self.gridPosToSurfPos(self.selectedPos))),
                )
            elif type(self.selectedPos) == tuple:
                size: Vec = self.selectedPos[1] - self.selectedPos[0]
                corner: Vec = self.selectedPos[0].copy()
                if size.x < 0:
                    size.x = -size.x
                    corner.x -= size.x
                if size.y < 0:
                    size.y = -size.y
                    corner.y -= size.y
                size += Vec(1, 1)
                rectSize = self.itemSpacing * size * self.zoom
                pos = Helpers.round(Helpers.vecToTulpe(self.gridPosToSurfPos(corner)))
                pygame.draw.rect(
                    sprite,
                    pygame.Color(50, 50, 50, 100),
                    pygame.Rect(pos[0], pos[1], rectSize.x, rectSize.y),
                )
                pygame.draw.rect(
                    sprite,
                    pygame.color.Color(150, 150, 150, 50),
                    pygame.Rect(
                        self.selectIconEdgeThickness + pos[0],
                        self.selectIconEdgeThickness + pos[1],
                        (self.itemSpacing * size.x * self.zoom) - self.selectIconEdgeThickness * 2,
                        (self.itemSpacing * size.y * self.zoom) - self.selectIconEdgeThickness * 2,
                    ),
                )
        for item in self.backend.items:
            icon: pygame.surface.Surface = item.getIcon()
            icon = pygame.transform.scale_by(
                icon, self.zoom * self.iconSize / max(icon.get_size()[0], icon.get_size()[1])
            )
            iconPos = (
                self.gridPosToSurfPos(item.pos)
                + Vec(
                    self.itemSpacing * self.zoom - icon.get_size()[0],
                    self.itemSpacing * self.zoom - icon.get_size()[1],
                )
                / 2
            )
            sprite.blit(icon, Helpers.round(Helpers.vecToTulpe(iconPos)))
        self.makeGrid(sprite)
        self.sprite = sprite

    def makeGrid(self, sprite):
        posScale = self.zoom * self.itemSpacing
        lineCount = self.sizePix / posScale
        lineCount = Vec(int(lineCount.x), int(lineCount.y))
        scaling = 1
        while posScale < 10:
            posScale *= 3
            lineCount /= 3
            scaling *= 3
        lineCount += Vec(3, 3)
        lineStart = (
            -Vec(self.viewCenter.x / scaling % 1, self.viewCenter.y / scaling % 1) * posScale
            + (self.sizePix / 2)
            - (Vec(int(lineCount.x / 2), int(lineCount.y / 2)) * posScale)
        )
        for x in range(int(lineCount.x)):
            pygame.draw.line(
                sprite,
                pygame.color.Color(128, 128, 128),
                (x * posScale + lineStart.x, 0),
                (x * posScale + lineStart.x, self.sizePix.y),
            )
        for y in range(int(lineCount.y)):
            pygame.draw.line(
                sprite,
                pygame.color.Color(128, 128, 128),
                (0, y * posScale + lineStart.y),
                (self.sizePix.x, y * posScale + lineStart.y),
            )

    def setVeiwCenter(self, veiwCenter: Vec):
        self.viewCenter = veiwCenter

    def setZoom(self, zoom: float, fromMousePos=False):
        if zoom > 1:
            zoom = 1
        if zoom < 0.001:
            zoom = 0.001
        if fromMousePos:
            self.viewCenter += (
                (Helpers.getMousePos() - self.pos - self.sizePix / 2) / self.zoom / self.itemSpacing
            )
            self.zoom = zoom
            self.viewCenter -= (
                (Helpers.getMousePos() - self.pos - self.sizePix / 2) / self.zoom / self.itemSpacing
            )
        else:
            self.zoom = zoom

    def setViewArea(self, veiwCenter: Vec = None, zoom: float = None):
        self.setVeiwCenter(veiwCenter)
        self.setZoom(zoom)

    def screenPosToGridPos(self, pos: Vec):
        return self.surfPosToGridPos(self.screenPosToSurfPos(pos))

    def gridPosToScreenPos(self, pos: Vec):
        return self.surfPosToScreenPos(self.gridPosToSurfPos(pos))

    def surfPosToGridPos(self, pos: Vec):
        return (pos - self.sizePix / 2) / self.zoom / self.itemSpacing + self.viewCenter

    def gridPosToSurfPos(self, pos: Vec):
        return (pos - self.viewCenter) * (self.zoom * self.itemSpacing) + (self.sizePix / 2)


class LogicGridBackend:
    nextItemID = 0

    def __init__(self) -> None:
        self.items: list[LogicGridItem] = []

    def addGridItem(self, item: LogicGridItem, pos: Vec):
        self.removeGridItem(pos=pos)
        item.pos = pos
        item.ID = self.nextItemID
        self.nextItemID += 1
        self.items.append(item)

    def addGridItemFromData(self, itemData: dict, pos: Vec):
        pass

    def removeGridItem(self, ID: int = None, pos: Vec = None):
        try:
            if ID != None:
                self.items.remove(self.getItemWithID(ID))
            else:
                self.items.remove(self.getItemAtPos(pos))
        except:
            pass

    def getAreaData(self, corner: Vec = None, size: Vec = None):
        pass

    def setAreaData(self, items: list[dict], pos: Vec = Vec(), clearAreaBefore: bool = True):
        """DOES NOT WORK BECAUSE LogicGridItem DOES NOT IMPEMENT ANY OF THE FUNCTIONS CALLED"""
        allItemClasses: list[type[LogicGridItem]] = [LogicGridItem, testItem]
        for itemData in items:
            for itemClass in allItemClasses:
                itemClass = itemClass
                if itemClass.dataIsType(itemData):
                    item: LogicGridItem = itemClass(itemData)
                    self.addGridItem(item, item.pos + pos)
                    break

    def getItemWithID(self, ID: int):
        for item in self.items:
            if item.ID == ID:
                return item
        return None

    def getItemAtPos(self, pos: Vec):
        for item in self.items:
            if item.pos == pos:
                return item
        return None

    def getItemsBetweenPos(self, corner1: Vec, corner2: Vec):
        itemsInArea = []
        for item in self.items:
            if Helpers.isPosInArea(item.pos, corner1, corner2):
                itemsInArea.append(item)
        return itemsInArea
