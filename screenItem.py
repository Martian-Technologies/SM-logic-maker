import pygame
from helpers import Helpers
from main import App
from pygame import Vector2 as Vec

class ScreenItem:
    def __init__(self, name=None) -> None:
        self.ID = None
        self.name = name
        self.itemManager = None
        self.app:App = None

    def initInWin(self):
        pass

    def draw(self):
        pass

    def handleEvents(self, events:list[pygame.event.Event]):
        pass

    def update(self):
        pass

class ScreenSpriteItem(ScreenItem):
    def __init__(self, sprite:pygame.surface.Surface, pos:Vec, name:str=None) -> None:
        super().__init__(name)
        self.sprite:pygame.surface.Surface = sprite
        self.pos:Vec = pos

    def screenPosToSurfPos(self, pos):
        return pos - self.pos
        
    def surfPosToScreenPos(self, pos):
        return pos + self.pos

    def intersectsPos(self, pos:Vec):
        pos = self.screenPosToSurfPos(pos)
        if pos.x < 0 or pos.y < 0 or pos.x >= self.sprite.get_size()[0] or pos.y >= self.sprite.get_size()[1]:
            return False
        color:pygame.color.Color = self.sprite.get_at((int(pos.x), int(pos.y)))
        if color.r == 0 and color.g == 0 and color.b == 0 and color.a == 0:
            return False
        return True
    
    def isTouchingMouse(self):
        return self.intersectsPos(Helpers.getMousePos())

    def draw(self):
        self.app.screen.blit(self.sprite, (self.pos.x, self.pos.y))

    def handleEvents(self, events:list[pygame.event.Event]):
        pass

    def update(self):
        pass

    def updatePos(self, newPos:Vec):
        self.pos = newPos

class Button(ScreenSpriteItem):
    def __init__(self, sprite:pygame.surface.Surface, pos:Vec, spriteOffsetOnClick:Vec=Vec(), name:str=None) -> None:
        super().__init__(sprite, pos, name)
        self.clickTypes = [1]
        self.isDown:bool = False
        self.spriteOffsetOnClick:Vec = spriteOffsetOnClick

    def draw(self):
        if self.isDown:
            pos = self.pos + self.spriteOffsetOnClick
            self.app.screen.blit(self.sprite, (pos.x, pos.y))
        else:
            super().draw()


    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                eventPos:Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if not self.isDown:
                    self.updateDownStat()
                    if self.isDown:
                        self.clicked(Vec(event.pos[0], event.pos[1]), event)
            elif event.type == pygame.MOUSEBUTTONUP:
                eventPos:Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if self.isDown:
                    self.updateDownStat()
                    if not self.isDown:
                        self.unclicked(Vec(event.pos[0], event.pos[1]), event)
                
            elif event.type == pygame.MOUSEMOTION:
                eventPos:Vec = Vec(event.pos[0], event.pos[1]) - self.pos
                if not self.isDown:
                    pressedButtons = self.updateDownStat()
                    if self.isDown:
                        self.motionClick(eventPos, event, pressedButtons)
                else:
                    self.updateDownStat()
                    if not self.isDown:
                        self.motionUnclick(eventPos, event)

    def updateDownStat(self):
        pressed = pygame.mouse.get_pressed()
        pressedButtons = []
        for i in self.clickTypes:
            if pressed[i-1]:
                pressedButtons.append(i)
        pos:Vec = Vec(pygame.mouse.get_pos()[0],  pygame.mouse.get_pos()[1]) - self.pos 
        self.isDown = len(pressedButtons) != 0 and self.isTouchingMouse()
        return pressedButtons
    
    def updatePos(self, newPos:Vec):
        self.pos = newPos
        pos:Vec = Vec(pygame.mouse.get_pos()[0],  pygame.mouse.get_pos()[1]) - self.pos 
        if not self.isDown:
            pressedButtons = self.updateDownStat()
            if self.isDown:
                self.buttonMovedClick(pos, pressedButtons)
        else:
            self.updateDownStat()
            if not self.isDown:
                self.buttonMovedUnclick(pos)

    def clicked(self, eventPos:Vec, event:pygame.event.Event):
        pass

    def unclicked(self, eventPos:Vec, event:pygame.event.Event):
        pass

    def motionClick(self, eventPos:Vec, event:pygame.event.Event, pressedButtons:list[int]):
        pass
    
    def motionUnclick(self, eventPos:Vec, event:pygame.event.Event):
        pass

    def buttonMovedClick(self, eventPos:Vec, pressedButtons:list[int]):
        pass
    
    def buttonMovedUnclick(self, eventPos:Vec):
        pass