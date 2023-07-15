import pygame
from pygame.locals import *
from main import App
from screenItemManager import ScreenItemManager
from screenItem import Button
from pygame import Vector2 as Vec
from logicGrid import LogicGrid
from logicGrid import LogicGridItem
from blockMenu import BlockMenu
from pluginManager import PluginManager

class MainLoop:
    def __init__(self, app:App) -> None:
        self.app = app
        app.mainLoop = self
        self.itemManager = ScreenItemManager(app)
        sur = pygame.surface.Surface((40, 40))
        sur.fill(pygame.color.Color(0, 0, 255))
        self.itemManager.addItem(
            Button(
                sur,
                Vec(10, 10)
            )
        )
        self.block_menu = BlockMenu(Vec(50, 100), Vec(150, -60), 'block menu')
        pm = PluginManager(app)
        print(self.block_menu.items)
        self.itemManager.addItem(self.block_menu)

        logicGrid:LogicGrid = self.itemManager.addItem(LogicGrid(Vec(200, 70), Vec(100, 70), 'logic grid'))
        logicGrid.backend.addGridItem(LogicGridItem(), Vec(0, 0))
        logicGrid.backend.addGridItem(LogicGridItem(), Vec(2, 0))
        logicGrid.backend.addGridItem(LogicGridItem(), Vec(0, 2))
        logicGrid.backend.addGridItem(LogicGridItem(), Vec(2, 2))
    
    def loop(self, events:pygame.event.Event):
        """The main loop for the app"""
        self.app.screen.fill(pygame.color.Color(0, 0, 0, ))
        self.itemManager.handleEvents(events)
        self.itemManager.update()
        self.itemManager.draw()
        pygame.display.update()