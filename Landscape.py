import random
import numpy

'''
Landscape

A class to describe a landscape with certain number mines

Initialize:

Landscape(area_width, mines_count)
area_width: the width of the mines area[width, width]
mines_count: total mines in this area

Functions:
detect(pos): if there is a mine in that location, then return -1, else return total mines nearby


'''


class Landscape:
    data = []
    mines_count = 0

    def __init__(self, area_width, mines_count):
        self.data = numpy.zeros([area_width, area_width])
        self.mines_count = mines_count

        coordinates = []

        for x in range(area_width):
            for y in range(area_width):
                coordinates.append((x, y))
        while mines_count > 0:
            mines_count -= 1
            pos = random.choice(coordinates)
            coordinates.remove(pos)
            self.data[pos] = 1

    def print(self):
        print(self.data)

    def get_valid_neighbours(self, pos):
        width = len(self.data)
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if pos[0] + dx in range(width) and pos[1] + dy in range(width):
                    neighbours.append((pos[0] + dx, pos[1] + dy))
        neighbours.remove(pos)
        return neighbours

    def is_mine(self, pos):
        return self.data[pos] == 1

    def get_mines_count(self, pos):
        neighbours = self.get_valid_neighbours(pos)
        count = 0
        for pos in neighbours:
            if self.is_mine(pos):
                count += 1
        return count

    def detect(self, pos):
        if self.is_mine(pos) == 1:
            return -1
        return self.get_mines_count(pos)


def test_drive():
    minesArea = Landscape(10, 10)
    for x in range(10):
        line = [minesArea.detect((x, y)) for y in range(10)]
        print(line)
