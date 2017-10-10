import numpy
import random
import ErrorNote

# import sys
# sys.setrecursionlimit(1000000)

'''
Sweeper

A risk-evaluation based algorithm

Rules:

1. The risk of a cell is basically measured by the probability whether it is a mine
2. To evaluate a cell, we concern all surrounding uncovered cells, from these cells, we know the probability
    of current position (if a neighbour point has 1 unknown mine and 2 covered neighbours, the probability of 
    current location is a mine is 1/2). We use the max probability as the risk value.
3. If a probability of 0 occurred while calculating, which means some of its neighbours are sure that current 
    location is not a mine, then it cannot be mine. We can uncover it.
4. If a probability of 1 occurred while calculating, which means some of its neighbours are sure it is a mine,
    then it must be a mine, we can mark it as a mine directly.
5. If there is no position described in (3) and (4), we choice the minimum risk cell to uncover

P.S: After several attempts to improve the accuracy, I finally realize the fact that only rule 3 and 4 work. It
    does not change too much how the risk of a position is evaluated. =_=
    
    The following case cannot be solved using logical model only:
    [[ ?.  ?.  ?.
     [ ?.  1.  ?.
     [ ?.  ?.  ?. ]]

Known problems:

The following case can be solved manually, but the algorithm failed while testing

[[ 0.  0.  0.  0.  0.]
 [ 1.  2.  1.  1.  0.]
 [-1.  3. -1.  1.  0.]
 [ ?.  *.  3.  3.  2.]
 [ 1.  ?.  2. -1. -1.]]
 
(Only 1 mine left in this region. After evaluation on unknown positions (those marked as '*' and '?'),
 the algorithm found the remaining 3 unknown positions are all with a risk of .5. So it randomly decided 
 to uncover '*' position, which is actually a mine. However, as we can see, to satisfy both 3 nearby, '*' 
 must be a mine. In this case algorithm can do nothing but guess.
 The problem is we cannot try all the possible cases where remaining mines can be, we cannot afford the
 space and time cost)

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

    error_note = ErrorNote.ErrorNote()

    def __init__(self):
        pass

    def load(self, problem):
        self.problem = problem
        self.problem_width = len(self.problem.data)

        self.explored_map = numpy.zeros([self.problem_width, self.problem_width])
        self.uncovered_location = numpy.zeros([self.problem_width, self.problem_width])
        self.remain_mines = self.problem.mines_count
        self.uncovered_count = 0

    def get_valid_neighbours(self, pos):
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if pos[0] + dx in range(self.problem_width) and pos[1] + dy in range(self.problem_width) \
                        and not (dx == 0 and dy == 0):
                    neighbours.append((pos[0] + dx, pos[1] + dy))
        return neighbours

    def get_valid_neighbours_number(self, pos):
        if pos[0] in (0, self.problem_width - 1) and pos[1] in (0, self.problem_width - 1):
            return 3
        if pos[0] in (0, self.problem_width - 1) or pos[1] in (0, self.problem_width - 1):
            return 5
        return 8

    def is_uncovered(self, pos):
        return self.uncovered_location[pos[0], pos[1]] == 1

    def get_uncovered_neighbours(self, pos):
        neighbours = self.get_valid_neighbours(pos)
        uncovered_neighbours = []
        for neighbour in neighbours:
            if self.is_uncovered(neighbour):
                uncovered_neighbours.append(neighbour)
        return uncovered_neighbours

    def get_uncovered_neighbours_number(self, pos):
        count = 0
        for dx in (-1, 0, 1):
            _x = pos[0] + dx
            for dy in (-1, 0, 1):
                _y = pos[1] + dy
                if _x in range(self.problem_width) and _y in range(self.problem_width) and (_x, _y) != pos:
                    if self.uncovered_location[_x, _y] == 1:
                        count += 1
        return count

    def get_covered_neighbours(self, pos):
        neighbours = self.get_valid_neighbours(pos)
        covered_neighbours = []
        for neighbour in neighbours:
            if not self.is_uncovered(neighbour):
                covered_neighbours.append(neighbour)
        return covered_neighbours

    def get_covered_neighbours_number(self, pos):
        return self.get_valid_neighbours_number(pos) - self.get_uncovered_neighbours_number(pos)

    def get_mines_nearby(self, pos):
        neighbours = self.get_uncovered_neighbours(pos)
        mines = []
        for neighbour in neighbours:
            if self.explored_map[neighbour] == -1:
                mines.append(neighbour)
        return mines

    def make_error_key(self, pos):
        data = ''
        for dx in (-1, 0, 1):
            x = dx + pos[0]
            for dy in (-1, 0, 1):
                y = dy + pos[1]
                if x in range(self.problem_width) and y in range(self.problem_width):
                    pos = (x, y)
                    if self.is_uncovered(pos):
                        data += str(self.explored_map[pos] - self.get_mines_nearby_number(pos))
                    else:
                        data += str(-2)
                else:
                    data += str(-3)
        return data

    def record_note(self, pos, result):
        self.error_note.add_note(self.make_error_key(pos), result)

    def get_mines_nearby_number(self, pos):
        count = 0
        for dx in (-1, 0, 1):
            _x = pos[0] + dx
            for dy in (-1, 0, 1):
                _y = pos[1] + dy
                if _x in range(self.problem_width) and _y in range(self.problem_width) and (_x, _y) != pos:
                    if self.explored_map[_x, _y] == -1:
                        count += 1
        return count

    def evaluate_risk(self, pos):
        # a basic risk is that we know there are certain mines in certain number cells

        risk = self.remain_mines / (self.problem_width * self.problem_width - self.uncovered_count)
        neighbours = self.get_valid_neighbours(pos)
        for neighbour in neighbours:
            if self.is_uncovered(neighbour):
                total_mines = self.explored_map[neighbour]
                known_mines = self.get_mines_nearby_number(neighbour)
                total_cells = self.get_valid_neighbours_number(neighbour)
                known_cells = self.get_uncovered_neighbours_number(neighbour)

                unknown_mines = total_mines - known_mines
                unknown_cells = total_cells - known_cells

                if total_mines != -1:  # this neighbour is not a mine
                    # the risk of a position is the max risk of his uncovered neighbours think on this position
                    if unknown_cells == 0:
                        print('!!!impossible!!! evaluate_risk')

                    risk = max(risk, unknown_mines / unknown_cells)
                    # it cannot be a mine if any of its neighbour knows all the mines nearby
                    if unknown_mines == 0:
                        return 0
                    # it must be a mine if any of its neighbour thinks it is a mine
                    if unknown_mines == unknown_cells:
                        return 1
        return round(risk, 2)

    def mark_as_mine(self, mine_position):
        self.remain_mines -= 1
        self.explored_map[mine_position[0], mine_position[1]] = -1
        self.uncovered_location[mine_position[0], mine_position[1]] = 1
        self.uncovered_count += 1

    def explore(self, pos):
        if self.uncovered_count == 0:
            value = self.problem.first_detect(pos)
        else:
            value = self.problem.detect(pos)
        if value == -1:  # if we detect a mine directly, game lost
            # print('LOSE')
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
        # hit = 0
        count = 0

        def remove_all_confirmed_position(risk_values):
            remove_list = []
            for i in range(len(risk_values)):
                if risk_values[i] == 1:
                    mine_point = work_queue[i]
                    self.mark_as_mine(mine_point)
                    remove_list.append(mine_point)
                elif risk_values[i] == 0:
                    self.explore(work_queue[i])
                    remove_list.append(work_queue[i])
            for ptn in remove_list:
                work_queue.remove(ptn)
            return len(remove_list) > 0  # recalculate the risk list if we find confirmed some new locations

        while len(work_queue) > 0:
            # risks = [self.evaluate_risk(pos) for pos in work_queue]
            risks = [self.evaluate_risk(pos) + .3 * self.error_note.get_evaluate(self.make_error_key(pos)) for pos in
                     work_queue]

            if remove_all_confirmed_position(risks):
                continue

            if len(work_queue) > 0:
                min_index = int(numpy.argmin(risks))
                min_risk_point = work_queue[min_index]

                if self.explore(min_risk_point):

                    for point, value in zip(work_queue, risks):
                        '''
                        print('P', point, '=', value)
                        
                        if (self.error_note.get_evaluate(point) > 0) == (self.problem.data[point] == 0):
                            hit += 1
                        count += 1
                        '''

                        self.record_note(point, self.problem.data[point])

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
        '''
        print(self.explored_map)
        if self.uncovered_count != self.problem_width * self.problem_width:
            print(self.problem.data)
        print('Mines found:', correct_count, '/', self.problem.mines_count)
        print('Uncovered Cells:', self.uncovered_count, '/', (self.problem_width * self.problem_width))
        '''

        if error_count > 0:
            print('!!!Error count:', error_count)
        if count == 0: count = -1
        return self.uncovered_count == self.problem_width * self.problem_width
