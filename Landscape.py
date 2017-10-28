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
first_detect(pos): (* must call this first *)
                    to avoid first position is a mine, the map will be generated after detect a position
detect(pos): if there is a mine in that location, then return -1, else return total mines nearby
'''


class Landscape:

    data = []
    mines_count = area_width = 0

    def _get_all_coordinates(self):
        coordinates = []
        for x in range(self.area_width):
            for y in range(self.area_width):
                coordinates.append((x, y))
        return coordinates

    def __init__(self, area_width, mines_count):
        self.data = numpy.zeros([area_width, area_width])
        self.mines_count = mines_count
        self.area_width = area_width

    def first_detect(self, base_pos):
        self.data = numpy.zeros([self.area_width, self.area_width])
        coordinates = self._get_all_coordinates()
        coordinates.remove(base_pos)
        for i in range(self.mines_count):
            pos = random.choice(coordinates)
            coordinates.remove(pos)
            self.data[pos] = 1
        return self.detect(base_pos)

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
            count += 1 if self.is_mine(pos) else 0
        return count

    def get_all_game_map(self):
        game_map = numpy.zeros(shape=[self.area_width, self.area_width])
        for i in range(self.area_width):
            for j in range(self.area_width):
                game_map[i, j] = self.detect((i, j))
        return game_map

    def detect(self, pos):

        if self.is_mine(pos): return -1
        value = self.get_mines_count(pos)

        prob = .3

        def event_happen(p):
            return p * 100 > random.randint(0, 100)

        if event_happen(prob):
            value += 1
        if event_happen(prob / 2):
            value += 1
        if event_happen(prob / 4):
            value += 1
        return min(value, 8)
