from enum import Enum
from random import choice
from time import sleep
import os
import copy
import sys
import argparse


def cls():
    os.system('cls' if os.name == 'nt' else 'clear') 


objectSymbols = {
    "FISH": "\U0001f420",
    "SHRIMP": "\U0001f990",
    "ROCK": "\u26f0",
    "WATER": "\U0001f30a"
}


class Type(Enum):
    FISH = 0
    SHRIMP = 1
    ROCK = 2
    WATER = 3


class OceanObject:
    def __init__(self, obj_type: Type):
        self.type = obj_type
        self.symbol = objectSymbols[obj_type.name]


class Ocean:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.oceanMap = [[OceanObject(choice(list(Type))) for x in range(width)] for y in range(height)]

    def update(self):
        new_ocean = copy.deepcopy(self.oceanMap)    #используем метод deepcopy, который создает новый составной объект, и затем рекурсивно вставляет в него копии объектов, а не ссылки находящихся в оригинале
        for y in range(self.height):
            for x in range(self.width):
                ocean_tile = self.oceanMap[y][x]
                if ocean_tile.type == Type.ROCK:
                    continue
                elif ocean_tile.type == Type.FISH or ocean_tile.type == Type.SHRIMP:
                    alive = self.check_creature_neighbours(ocean_tile, x, y)
                    if alive:
                        continue
                    else:
                        new_ocean[y][x] = OceanObject(Type.WATER)
                else:
                    new_ocean[y][x] = self.check_water_neighbours(x, y)
        self.oceanMap = copy.deepcopy(new_ocean)

    def check_creature_neighbours(self, tile, x, y):
        tile_type = tile.type
        neighbours_count = 0
        for n_y in range(y - 1, y + 2):
            for n_x in range(x - 1, x + 2):
                try:
                    if n_x == x and n_y == y or n_x < 0 or n_y < 0:
                        continue
                    if self.oceanMap[n_y][n_x].type == tile_type:
                        neighbours_count += 1
                except IndexError:
                    continue
        if ((neighbours_count == 2) or (neighbours_count == 3)):
            return True
        else:
            return False

    def check_water_neighbours(self, x, y):
        shrimps_count = 0
        fish_count = 0
        for n_y in range(y - 1, y + 2):
            for n_x in range(x - 1, x + 2):
                try:
                    if n_x == x and n_y == y or n_x < 0 or n_y < 0:
                        continue
                    if self.oceanMap[n_y][n_x].type == Type.SHRIMP:
                        shrimps_count += 1
                    elif self.oceanMap[n_y][n_x].type == Type.FISH:
                        fish_count += 1
                except IndexError:
                    continue
        if fish_count == 3:
            return OceanObject(Type.FISH)
        elif shrimps_count == 3:
            return OceanObject(Type.SHRIMP)
        else:
            return OceanObject(Type.WATER)

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.oceanMap[y][x].symbol, end=" ")
            print()
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulates life in an ocean. Draws creatures and objects with unicode emoji.")
    parser.add_argument("--width", type=int, help="width of the ocean map")
    parser.add_argument("--height", type=int, help="height of the ocean map")
    args = vars(parser.parse_args())
    if args["width"] is None:   #если аргументы не заданы, по умолчанию поле будет 20х20
        args["width"] = 20
    if args["height"] is None:
        args["height"] = 20
    ocean = Ocean(args["width"], args["height"])
    while True:
        cls()   #очистка
        ocean.draw() 
        sleep(100)  #периодичность изменений в океане
        ocean.update()
