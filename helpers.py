from pygame import Vector2 as Vec
import pygame
import math

class Helpers:
    @staticmethod
    def getMousePos():
        return Vec(pygame.mouse.get_pos()[0],  pygame.mouse.get_pos()[1])
    
    @staticmethod
    def floorVec(vec:Vec):
        return Vec(math.floor(vec.x), math.floor(vec.y))