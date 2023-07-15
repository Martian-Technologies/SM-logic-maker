import pygame
from screenItem import ScreenItem
from main import App


class ScreenItemManager:
    def __init__(self, app: App):
        self.app = app
        self.items: list[ScreenItem] = []
        self.nextItemID = 0

    def addItem(self, item: ScreenItem, index=-1):
        item.ID = self.nextItemID
        item.app = self.app
        self.nextItemID += 1
        if len(self.items) == 0:
            self.items.append(item)
            return
        elif index > len(self.items) - 1:
            index = len(self.items) - 1
        self.items.insert(index, item)
        item.initInWin()
        return item

    def removeItem(self, ID):
        for item in self.items:
            if item.ID == ID:
                self.items.remove(item)

    def getItemFromID(self, ID):
        for item in self.items:
            if item.ID == ID:
                return item
        return None

    def getItemFromName(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def handleEvents(self, events: list[pygame.event.Event]):
        for item in self.items:
            item.handleEvents(events)

    def draw(self):
        for item in self.items:
            item.draw()

    def update(self):
        for item in self.items:
            item.update()
