from helpers import Helpers
from logicGrid import LogicGridItem
from screenItem import ScreenSpriteItem
from logicGrid import testItem
from pygame import Vector2 as Vec
import pygame

class BlockMenu(ScreenSpriteItem):
    def __init__(self, pos:Vec, pos2:Vec, name:str=None) -> None:
        self.name = name
        self.pos:Vec = pos
        self.pos2:Vec = pos2
        self.scrollPos = 0
        self.items:list[type[LogicGridItem]] = [LogicGridItem, testItem, LogicGridItem]
        self.selectedItem = None
        self.iconSize = 80

    def initInWin(self):
        self.setupSprites()
        
    def handleEvents(self, events:list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEWHEEL and self.isTouchingMouse():
                if event.y > 0 or (len(self.items) - 1 - self.scrollPos)*(self.iconSize + 20) + self.iconSize + 50 > self.size.y:
                    self.scrollPos = self.scrollPos - event.y/10
                if self.scrollPos < 0 or len(self.items) == 0:
                    self.scrollPos = 0
                if (len(self.items) - 1 - self.scrollPos)*(self.iconSize + 20) + self.iconSize + 50 < self.size.y:
                    fixPos = -((self.size.y - self.iconSize - 50) / (self.iconSize + 20) - len(self.items) + 1)
                    if fixPos > 0:
                        self.scrollPos = fixPos
            elif event.type == pygame.WINDOWRESIZED:
                self.setupSprites()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.isTouchingMouse():
                    i = int(self.scrollPos)
                    while i - 10 < self.scrollPos:
                        if len(self.items) <= i:
                            break
                        item = self.items[i]
                        icon = item.getMenuIcon()
                        icon = pygame.transform.scale_by(icon, self.iconSize/max(icon.get_size()[0], icon.get_size()[1]))
                        if (i - self.scrollPos)*(self.iconSize + 20) + 20 > self.size.y:
                            break
                        if Helpers.isSurfAtPosTouchingPos(
                                self.getSurfPosOfItemAtIndex(i),
                                icon, self.screenPosToSurfPos(Helpers.getMousePos())
                            ):
                            if self.selectedItem == item:
                                self.selectedItem = None
                            else:
                                self.selectedItem = item
                            break
                        i += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selectedItem = None
    
    def setupSprites(self):
        self.size:Vec =  Vec(0, self.app.screen.get_size()[1]) + self.pos2 - self.pos
        self.sprite:pygame.surface.Surface = pygame.surface.Surface((self.size.x, self.size.y))
        self.baseSprite:pygame.surface.Surface = pygame.surface.Surface((self.size.x, self.size.y))
        self.baseSprite.fill(pygame.color.Color(150, 150, 150))
    
    def getSurfPosOfItemAtIndex(self, index:int):
        if len(self.items) <= index or len(self.items) < -index:
            return None
        iconSize = Helpers.tulpeToVec(self.items[index].getMenuIcon().get_size())
        iconSize = iconSize * self.iconSize/max(iconSize.x, iconSize.y)
        return Vec(
            (self.size.x - iconSize.x)/2,
            (index - self.scrollPos)*(self.iconSize + 20) + 20 + (self.iconSize - iconSize.y)/2
            )

    def draw(self):
        self.sprite.blit(self.baseSprite, (0, 0))
        i = int(self.scrollPos)
        if i >= 1:
            i -= 1
        while i - 10 < self.scrollPos:
            if len(self.items) <= i:
                break
            item = self.items[i]
            icon = item.getMenuIcon()
            icon = pygame.transform.scale_by(icon, self.iconSize/max(icon.get_size()[0], icon.get_size()[1]))
            if (i - self.scrollPos)*(icon.get_size()[1] + 20) + 20 > self.size.y:
                break
            pos = Helpers.vecToTulpe(self.getSurfPosOfItemAtIndex(i))
            if item == self.selectedItem:
                glow:pygame.surface.Surface = pygame.transform.scale_by(icon, 1.2)
                glow.fill(pygame.color.Color(81, 255, 13))
                glowPos = (pos[0] + (icon.get_size()[0] - glow.get_size()[0])/2,
                              pos[1] + (icon.get_size()[1] - glow.get_size()[1])/2)
                self.sprite.blit(glow, glowPos)

            self.sprite.blit(icon, pos)
            i += 1
        super().draw()
        
    def addItem(self, item:LogicGridItem):
        self.items.append(item)

    def addItems(self, items:list[LogicGridItem]):
        for item in items:
            self.addItem(item)