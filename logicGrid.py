import pathlib
from pygame import Vector2 as Vec
import pygame
from helpers import Helpers
from screenItem import ScreenSpriteItem

class LogicGridItem:
    icon:pygame.surface.Surface = pygame.surface.Surface((100, 100))
    icon.fill(pygame.color.Color(100, 100, 100))

    def __init__(self, data=None, name:str="base grid class", icon:pygame.surface.Surface=None) -> None:
        self.name = name
        self.ID = None
        self.pos = None
        if icon != None:
            self.icon = icon

    def getIcon(self) -> pygame.Surface:
        return self.icon

    def toData(self):
        pass

    @classmethod
    def getMenuIcon(cls):
        return cls.icon

    @staticmethod
    def dataIsType(data):
        pass

class testItem(LogicGridItem):
    icon:pygame.surface.Surface = pygame.image.load(pathlib.Path("/Users/ben/Documents/GitHub/SM logic maker/mtechloadingscreen.png"))
    #icon.fill(pygame.color.Color(0, 100, 0))
    
    def __init__(self, data=None) -> None:
        super().__init__(data, "testItem", None)
         

class LogicGrid(ScreenSpriteItem):
    nextItemID = 0
    
    def __init__(self, pos1FromTopLeft:Vec, pos2FromBottomRight:Vec, name:str=None) -> None:
        super().__init__(None, pos1FromTopLeft, name)
        self.pos2:Vec = pos2FromBottomRight
        self.sizePix:Vec = None
        self.veiwCenter:Vec = Vec(-1, 1)
        self.zoom:int = 0.5
        self.items:list[LogicGridItem] = []
        self.itemSpacing = 128
        self.iconSize = 100
        self.selectedPos = None
        self.selectIconEdgeThickness = 5

    def initInWin(self):
        self.sizePix:Vec = Vec(self.app.screen.get_size()[0], self.app.screen.get_size()[1]) - self.pos - self.pos2
        self.blockMenu = self.app.mainLoop.itemManager.getItemFromName('block menu')

    def handleEvents(self, events:list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEWHEEL and self.isTouchingMouse():
                self.setZoom(zoom = self.zoom + event.y/10)
            elif event.type == pygame.WINDOWRESIZED:
                self.sizePix:Vec = Vec(self.app.screen.get_size()[0], self.app.screen.get_size()[1]) - self.pos - self.pos2
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isTouchingMouse():
                if event.button == 1:
                    clickedPos = Helpers.floorVec(self.screenPosToGridPos(Helpers.getMousePos()))
                    if self.blockMenu.selectedItem != None:
                        self.addGridItem(self.blockMenu.selectedItem(), clickedPos)
                    else:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.selectedPos != None:
                        if type(self.selectedPos) == tuple:
                            areaSize = self.selectedPos[1] - self.selectedPos[0]
                            corner = self.selectedPos[0].copy()
                            if areaSize.x < 0:
                                areaSize.x = -areaSize.x
                                corner.x -= areaSize.x
                            if areaSize.y < 0:
                                areaSize.y = -areaSize.y
                                corner.y -= areaSize.y
                            areaSize += Vec(1, 1)
                            for x in range(int(areaSize.x)):
                                for y in range(int(areaSize.y)):
                                    print(Vec(x, y) + corner)
                                    self.removeGridItem(pos=Vec(x, y) + corner)
                        else:
                            self.removeGridItem(pos=self.selectedPos)
        
                        
    def update(self):
        movementVec = Vec()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            movementVec.y -= 1/self.zoom
        elif pressed[pygame.K_DOWN]:
            movementVec.y += 1/self.zoom
        if pressed[pygame.K_LEFT]:
            movementVec.x -= 1/self.zoom
        elif pressed[pygame.K_RIGHT]:
            movementVec.x += 1/self.zoom
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            movementVec *= 2
        self.setVeiwCenter(self.veiwCenter + movementVec * self.app.deltaTimeMS / 500)

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
                    pygame.Rect(self.selectIconEdgeThickness / self.zoom,
                                self.selectIconEdgeThickness / self.zoom,
                                self.itemSpacing - self.selectIconEdgeThickness*2/self.zoom,
                                self.itemSpacing - self.selectIconEdgeThickness*2/self.zoom)
                                )
                sprite.blit(pygame.transform.scale_by(selectIcon, self.zoom),
                        Helpers.round(Helpers.vecToTulpe(self.gridPosToSurfPos(self.selectedPos))))
            elif type(self.selectedPos) == tuple:
                size:Vec = self.selectedPos[1] - self.selectedPos[0]
                corner:Vec = self.selectedPos[0].copy()
                if size.x < 0:
                    size.x = -size.x
                    corner.x -= size.x
                if size.y < 0:
                    size.y = -size.y
                    corner.y -= size.y
                size += Vec(1, 1)
                selectIcon = pygame.Surface(Helpers.vecToTulpe(self.itemSpacing*size))
                selectIcon.fill(pygame.Color(50, 50, 50, 100))
                pygame.draw.rect(
                    selectIcon,
                    pygame.color.Color(150, 150, 150, 50),
                    pygame.Rect(self.selectIconEdgeThickness / self.zoom,
                                self.selectIconEdgeThickness / self.zoom,
                                (self.itemSpacing*size.x) - self.selectIconEdgeThickness*2/self.zoom,
                                (self.itemSpacing*size.y) - self.selectIconEdgeThickness*2/self.zoom)
                                )
                sprite.blit(pygame.transform.scale_by(selectIcon, self.zoom),
                        Helpers.round(Helpers.vecToTulpe(self.gridPosToSurfPos(corner))))
        for item in self.items:
            icon:pygame.surface.Surface = item.getIcon()
            icon = pygame.transform.scale_by(icon, self.zoom * self.iconSize/max(icon.get_size()[0], icon.get_size()[1]))
            iconPos = self.gridPosToSurfPos(item.pos) + Vec(self.itemSpacing*self.zoom - icon.get_size()[0], self.itemSpacing*self.zoom - icon.get_size()[1])/2
            sprite.blit(icon, Helpers.round(Helpers.vecToTulpe(iconPos)))
        self.makeGrid(sprite)
        self.sprite = sprite
    
    def makeGrid(self, sprite):
        posScale = self.zoom * self.itemSpacing
        lineCount = self.sizePix / posScale
        lineCount = Vec(int(lineCount.x), int(lineCount.y)) + Vec(2, 2)
        lineStart = -Vec(self.veiwCenter.x % 1, self.veiwCenter.y % 1) * posScale + (self.sizePix / 2) \
            - (Vec(int(lineCount.x / 2), int(lineCount.y / 2)) * posScale)
        for x in range(int(lineCount.x)):
            pygame.draw.line(sprite, pygame.color.Color(0, 0, 0), (x * posScale + lineStart.x, 0), (x * posScale + lineStart.x, self.sizePix.y))
        for y in range(int(lineCount.y)):
            pygame.draw.line(sprite, pygame.color.Color(0, 0, 0), (0, y * posScale + lineStart.y), (self.sizePix.x, y * posScale + lineStart.y))

    def addGridItem(self, item:LogicGridItem, pos:Vec):
        self.removeGridItem(pos=pos)
        item.pos = pos
        item.ID = self.nextItemID
        self.nextItemID += 1
        self.items.append(item)

    def addGridItemFromData(self, itemData:dict, pos:Vec):
        pass

    def removeGridItem(self, ID:int=None, pos:Vec=None):
        try:
            if ID != None:
                self.items.remove(self.getItemWithID(ID))
            else:
                self.items.remove(self.getItemAtPos(pos))
        except:
            pass

    def setVeiwCenter(self, veiwCenter:Vec):
        self.veiwCenter = veiwCenter
    
    def setZoom(self, zoom:float):
        if zoom < 0.05:
            zoom = 0.05
        if zoom > 1:
            zoom = 1
        self.zoom = zoom

    def setVeiwArea(self, veiwCenter:Vec=None, zoom:float=None):
        if veiwCenter != None:
            self.veiwCenter = veiwCenter
        if zoom != None:
            self.zoom = zoom
            
    def screenPosToGridPos(self, pos:Vec):
        return self.surfPosToGridPos(self.screenPosToSurfPos(pos))

    def gridPosToScreenPos(self, pos:Vec):
        return self.surfPosToScreenPos(self.gridPosToSurfPos(pos))

    def surfPosToGridPos(self, pos:Vec):
        return (pos - (self.sizePix / 2)) / (self.zoom * self.itemSpacing) + self.veiwCenter

    def gridPosToSurfPos(self, pos:Vec):
        return (pos - self.veiwCenter) * (self.zoom * self.itemSpacing) + (self.sizePix / 2)

    def getAreaData(self, corner:Vec=None, size:Vec=None):
        pass

    def setAreaData(self, items:list[dict], pos:Vec=Vec(), clearAreaBefore:bool=False):
        pass

    def getItemWithID(self, ID:int):
        for item in self.items:
            if item.ID == ID:
                return item
        return None

    def getItemAtPos(self, pos:Vec):
        for item in self.items:
            if item.pos == pos:
                return item
        return None

