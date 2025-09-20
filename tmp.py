import pygame as pg
from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite


class holder:
    def __init__(self, group: Group) -> None:
        self.group = group

    def add(self):
        Sprite(self.group)


group = Group()

sprite = Sprite(group)

print(group)

h=holder(group)

h.add()

print(group)

group.update()

# sprite.kill()

print(group)

ls=[sprite]

print(len(ls))

print(ls[0])

del sprite

print(len(ls))

print("A",ls[0])