import os.path
import Landscape

'''

An attempt to improve the accuracy
Record all failed steps to avoid making the same mistakes

No significant improvement :(
Take the following problem-set as an example:

In every case, we solve 1000 5*5 cells with 5 mines.

Iteration counts                 |    1    |    2    |    3    |    4    |  ...  |   100   |
---------------------------------|---------|---------|---------|---------|  ...  |---------|
Correct Rate(with error-note)    |   40%   |   39%   |   41%   |   37%   |  ...  |   42%   |
Correct Rate(without error-note) |   35%   |   38%   |   36%   |   37%   |  ...  |   38%   |

Recorded 132 rules finally.
'''


class ErrorNote:
    memory = {}
    save_count = 0

    def __init__(self):
        if os.path.exists('key.txt'):
            self.load()

    def add_note(self, data, result):
        if result == -1:  # is a mine
            risk = 1
        else:
            risk = -1
        # the goal is to increase the risk when the result is -1, in other word, a mine
        if self.memory.get(data) is None:
            self.memory[data] = (risk, 1)
        else:
            self.memory[data] = (self.memory[data][0] + risk, self.memory[data][1] + 1)
            if self.memory[data][1] > 1000000:  # too big too store
                self.memory[data][0] /= 2
                self.memory[data][1] /= 2
        self.save_count += 1
        if self.save_count > 1000:
            self.save_count = 0
            self.check_point()

    def check_point(self):
        key_file = open('key.txt', 'w')
        data_file = open('data.txt', 'w')
        for key in self.memory.keys():
            key_file.write(key + '\n')
            data_file.write(str(self.memory[key][0]) + '\n')
            data_file.write(str(self.memory[key][1]) + '\n')
        key_file.close()
        data_file.close()

    def load(self):
        self.memory.clear()
        key_file = open('key.txt', 'r')
        data_file = open('data.txt', 'r')
        lines = key_file.readlines()
        for line in lines:
            if len(line) == 0: continue
            count, amount = int(data_file.readline()), int(data_file.readline())
            self.memory[line[:len(line) - 1]] = (count, amount)
        key_file.close()
        data_file.close()
        print('%g items loaded' % len(self.memory.keys()))

    def get_evaluate(self, data):
        if self.memory.get(data) is None:
            return 0
        pack = self.memory.get(data)
        if pack[1] < 100:
            return 0
        return 0.2 * pack[0] / pack[1]
