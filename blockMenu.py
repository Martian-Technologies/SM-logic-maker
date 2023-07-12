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

    def initInWin(self):
        self.setupSprites()
        
    def handleEvents(self, events:list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEWHEEL and self.isTouchingMouse():
                if event.y > 0 or (len(self.items) - self.scrollPos - 1)*(self.items[0].getMenuIcon().get_size()[1] + 20) + 100 > self.size.y:
                    self.scrollPos = self.scrollPos - event.y/10
                if self.scrollPos < 0 or len(self.items) == 0:
                    self.scrollPos = 0
                if (len(self.items) - self.scrollPos - 1)*(self.items[0].getMenuIcon().get_size()[1] + 20) + 100 < self.size.y:
                    self.scrollPos = -((self.size.y - 100) / (self.items[0].getMenuIcon().get_size()[1] + 20) - len(self.items) + 1)
            elif event.type == pygame.WINDOWRESIZED:
                self.setupSprites()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.isTouchingMouse():
                    i = int(self.scrollPos)
                    while i - 10 < self.scrollPos:
                        if len(self.items) <= i:
                            break
                        item = self.items[i]
                        icon = pygame.transform.scale_by(item.getMenuIcon(), self.itemScale)
                        if (i - self.scrollPos)*(icon.get_size()[1] + 20) + 20 > self.size.y:
                            break
                        if self.isSurfAtPosTouchingPos(
                                Vec((self.size.x - icon.get_size()[0])/2, (i - self.scrollPos)*(icon.get_size()[1] + 20) + 20),
                                icon, self.screenPosToSurfPos(Helpers.getMousePos())
                            ):
                            if self.selectedItem == item:
                                self.selectedItem = None
                            else:
                                self.selectedItem = item
                            print(self.selectedItem)
                            break
                        i += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selectedItem = None

    def isSurfAtPosTouchingPos(self, surfPos:Vec, surf:pygame.surface.Surface, pos:Vec):
        pos -= surfPos
        if pos.x < 0 or pos.y < 0 or pos.x >= surf.get_size()[0] or pos.y >= surf.get_size()[1]:
            return False
        color:pygame.color.Color = surf.get_at((int(pos.x), int(pos.y)))
        if color.r == 0 and color.g == 0 and color.b == 0 and color.a == 0:
            return False
        return True
    
    def setupSprites(self):
        self.size:Vec =  Vec(0, self.app.screen.get_size()[1]) + self.pos2 - self.pos
        self.sprite:pygame.surface.Surface = pygame.surface.Surface((self.size.x, self.size.y))
        self.baseSprite:pygame.surface.Surface = pygame.surface.Surface((self.size.x, self.size.y))
        self.baseSprite.fill(pygame.color.Color(150, 150, 150))
        self.itemScale:float = (self.size.x - 20) / 128
    
    def draw(self):
        self.sprite.blit(self.baseSprite, (0, 0))
        i = int(self.scrollPos)
        if i >= 1:
            i -= 1
        while i - 10 < self.scrollPos:
            if len(self.items) <= i:
                break
            item = self.items[i]
            icon = pygame.transform.scale_by(item.getMenuIcon(), self.itemScale)
            if (i - self.scrollPos)*(icon.get_size()[1] + 20) + 20 > self.size.y:
                break
            pos = ((self.size.x - icon.get_size()[0])/2, (i - self.scrollPos)*(icon.get_size()[1] + 20) + 20)
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