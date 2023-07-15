from pygame import Vector2 as Vec
import pygame
import math


class Helpers:
    @staticmethod
    def getMousePos():
        return Helpers.tulpeToVec(pygame.mouse.get_pos())

    def floorVec(vec: Vec):
        return Helpers.tulpeToVec(Helpers.floor(Helpers.vecToTulpe(vec)))

    def relitivePosIntersectsSurf(pos: Vec, surf: pygame.Surface):
        if pos.x < 0 or pos.y < 0 or pos.x >= surf.get_size()[0] or pos.y >= surf.get_size()[1]:
            return False
        color: pygame.color.Color = surf.get_at(Helpers.floor(Helpers.vecToTulpe(pos)))
        if color.r == 0 and color.g == 0 and color.b == 0 and color.a == 0:
            return False
        return True

    def isSurfAtPosTouchingPos(surfPos: Vec, surf: pygame.Surface, pos: Vec):
        return Helpers.relitivePosIntersectsSurf(pos - surfPos, surf)

    def tulpeToVec(pair: tuple):
        return Vec(pair[0], pair[1])

    def vecToTulpe(vec: Vec):
        return (vec.x, vec.y)

    def round(x: float | int | tuple | list) -> tuple[int] | int:
        if Helpers.isIterable(x):
            return tuple([round(n) for n in x])
        return round(x)

    def floor(x: float | int | tuple | list) -> tuple[int] | int:
        if Helpers.isIterable(x):
            return tuple([math.floor(n) for n in x])
        return math.floor(x)

    def abs(x: float | int | tuple | list) -> tuple[int] | int:
        if Helpers.isIterable(x):
            return tuple([abs(n) for n in x])
        return math.floor(x)

    def isIterable(obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False

    def removeItemsFromList(items: list | tuple | object | None, l: list):
        try:
            if Helpers.isIterable(items):
                for item in items:
                    l.remove(item)
            else:
                l.remove(item)
        except:
            pass

    def isPosInArea(pos: Vec, corner1: Vec, corner2: Vec):
        if (
            pos.x > max(corner1.x, corner2.x)
            or pos.x < min(corner1.x, corner2.x)
            or pos.y > max(corner1.y, corner2.y)
            or pos.y < min(corner1.y, corner2.y)
        ):
            return False
        return True
