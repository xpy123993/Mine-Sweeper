import numpy
import random

'''
Sweeper

A risk-evaluation based algorithm

Rules:

1. The risk of a cell is basically measured by the probability whether it is a mine
2. To evaluate a cell, we calculate all surrounding uncovered cells, from these cells, we know the probability
    of current position (if a neighbour point has 1 unknown mine and 2 uncovered neighbour, the probability of 
    current location is a mine is 1/2). We use the max probability as the risk value.
3. If a probability of 0 occurred while calculating, which means some of its neighbours are sure that current 
    location is not a mine, then it cannot be mine. We can uncover it.
4. If a probability of 1 occurred while calculating, which means some of its neighbours are sure it is a mine,
    then it must be a mine, we can mark it as a mine directly.
5. If there is no position described in (3) and (4), we choice the minimum risk cell to uncover


Functions:

load(landscape): load a landscape to solve
run():  start to solve, terminated if uncover a mine or all cells are uncovered

'''


class Sweeper:
    problem = None
    problem_width = 0

    explored_map = []
    uncovered_location = []

    remain_mines = 0
    uncovered_count = 0

    def __init__(self):
        pass

    def load(self, problem):
        self.problem = problem
        self.problem_width = len(self.problem.data)

        self.explored_map = numpy.zeros([self.problem_width, self.problem_width])
        self.uncovered_location = numpy.zeros([self.problem_width, self.problem_width])
        self.remain_mines = self.problem.mines_count

    def get_valid_neighbours(self, pos):
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if pos[0] + dx in range(self.problem_width) and pos[1] + dy in range(self.problem_width) \
                        and not (dx == 0 and dy == 0):
                    neighbours.append((pos[0] + dx, pos[1] + dy))
        return neighbours

    def is_uncovered(self, pos):
        return self.uncovered_location[pos[0], pos[1]] == 1

    def get_uncovered_neighbours(self, pos):
        neighbours = self.get_valid_neighbours(pos)
        uncovered_neighbours = []
        for neighbour in neighbours:
            if self.is_uncovered(neighbour):
                uncovered_neighbours.append(neighbour)
        return uncovered_neighbours

    def get_covered_neighbours(self, pos):
        neighbours = self.get_valid_neighbours(pos)
        covered_neighbours = []
        for neighbour in neighbours:
            if not self.is_uncovered(neighbour):
                covered_neighbours.append(neighbour)
        return covered_neighbours

    def get_mines_nearby(self, pos):
        neighbours = self.get_uncovered_neighbours(pos)
        mines = []
        for neighbour in neighbours:
            if self.explored_map[neighbour] == -1:
                mines.append(neighbour)
        return mines

    def evaluate_risk(self, pos):
        # a basic risk is that we know there are certain mines in certain number cells
        risk = self.remain_mines / (self.problem_width * self.problem_width - self.uncovered_count)
        neighbours = self.get_valid_neighbours(pos)
        for neighbour in neighbours:
            if self.is_uncovered(neighbour):
                total_mines = self.explored_map[neighbour]
                known_mines = len(self.get_mines_nearby(neighbour))
                total_cells = len(self.get_valid_neighbours(neighbour))
                known_cells = len(self.get_uncovered_neighbours(neighbour))

                unknown_mines = total_mines - known_mines
                unknown_cells = total_cells - known_cells

                if total_mines != -1:  # this neighbour is not a mine
                    # the risk of a position is the max risk of his uncovered neighbours think on this position
                    if unknown_cells == 0:
                        print('!!!impossible')

                    risk = max(risk, unknown_mines / unknown_cells)
                    # it cannot be a mine if any of its neighbour knows all the mines nearby
                    if unknown_mines == 0:
                        return 0
                    # it must be a mine if any of its neighbour thinks it is a mine
                    if risk == 1:
                        return 1
        return risk

    def mark_as_mine(self, mine_position):
        self.remain_mines -= 1
        self.explored_map[mine_position[0], mine_position[1]] = -1
        self.uncovered_location[mine_position[0], mine_position[1]] = 1
        self.uncovered_count += 1

    def explore(self, pos):
        value = self.problem.detect(pos)
        if value == -1:  # if we detect a mine directly, game lost
            print('LOSE')
            self.explored_map[pos[0], pos[1]] = -2
            return True
        self.explored_map[pos] = value
        self.uncovered_location[pos] = 1
        self.uncovered_count += 1
        return False

    def get_covered_locations(self):
        locations = []
        for x in range(self.problem_width):
            for y in range(self.problem_width):
                if self.uncovered_location[x, y] == 0:
                    locations.append((x, y))
        return locations

    def run(self):
        work_queue = self.get_covered_locations()

        def remove_all_mines_position(risk_values):
            remove_list = []
            for i in range(len(risk_values)):
                if risk_values[i] == 1:
                    mine_point = work_queue[i]
                    self.mark_as_mine(mine_point)
                    remove_list.append(mine_point)
            for mine_point in remove_list:
                work_queue.remove(mine_point)
            return len(remove_list) > 0  # recalculate the risk list if we find some new information

        while len(work_queue) > 0:
            risks = [self.evaluate_risk(pos) for pos in work_queue]

            if remove_all_mines_position(risks):
                risks = [self.evaluate_risk(pos) for pos in work_queue]

            if len(work_queue) > 0:
                min_index = int(numpy.argmin(risks))
                min_risk_point = work_queue[min_index]

                if self.explore(min_risk_point):
                    for point, value in zip(work_queue, risks):
                        print('P', point, '=', value)
                    break
                work_queue.remove(min_risk_point)
                random.shuffle(work_queue)

        correct_count = 0
        error_count = 0  # impossible

        for x in range(self.problem_width):
            for y in range(self.problem_width):
                if self.explored_map[x, y] == -1:
                    if self.problem.data[x, y] == 1:
                        correct_count += 1
                    else:
                        error_count += 1

        print(self.explored_map)
        if self.uncovered_count != self.problem_width * self.problem_width:
            print(self.problem.data)
        print('Mines found:', correct_count, '/', self.problem.mines_count)
        print('Uncovered Cells:', self.uncovered_count, '/', (self.problem_width * self.problem_width))

        if error_count > 0:
            print('!!!Error count:', error_count)
