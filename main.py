import pygame
from pygame.locals import *

class App:
    deltaTimeMS = None
    clock = None
    def __init__(self):
        self.running = True
        self.size = self.weight, self.height = 640, 400
        pygame.init()
        self.screen:pygame.surface.Surface = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.mainLoop = None
        self.start()

    def on_cleanup(self):
        pygame.quit()

    def start(self):
        MainLoop(self)
       
        while self.running:
            self.deltaTimeMS = self.clock.tick()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == VIDEORESIZE:
                    w, h = event.size
                    if w < 400:
                        w = 400
                    if h < 300:
                        h = 300
                    self.screen = pygame.display.set_mode((w, h), HWSURFACE|DOUBLEBUF|RESIZABLE)
            self.mainLoop.loop(events)
        self.on_cleanup()


if __name__ == "__main__":
    from mainLoop import MainLoop
    app = App()
