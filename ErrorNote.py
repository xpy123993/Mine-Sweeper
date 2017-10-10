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
Correct Rate(without error-note) |   40%   |   39%   |   41%   |   37%   |  ...  |   42%   |
Correct Rate(with error-note)    |   35%   |   38%   |   36%   |   37%   |  ...  |   38%   |

Recorded 132 rules finally.
'''


class ErrorNote:
    memory = {}
    forbidden = {}

    save_count = 0

    def __init__(self):
        if os.path.exists('save1.txt'):
            self.load()

    def add_note(self, data, result):
        result = 1 if result > 0 else -1
        if self.forbidden.get(data) is None:
            if self.memory.get(data) is None:
                self.memory[data] = result
            elif self.memory[data] != result:
                self.memory.pop(data)
                self.forbidden[data] = 1
        self.save_count += 1
        if self.save_count > 1000:
            self.save_count = 0
            self.check_point()

    def check_point(self):
        store_file = open('save1.txt', 'w')
        for value in self.forbidden.keys():
            store_file.write(value + '\n')
        store_file.close()
        store_file = open('save2.txt', 'w')
        store_file2 = open('save3.txt', 'w')
        for value in self.memory.keys():
            if self.memory.get(value) == 1:
                store_file.write(value + '\n')
            else:
                store_file2.write(value + '\n')
        store_file.close()
        store_file2.close()

    def load(self):
        self.forbidden.clear()
        self.memory.clear()
        store_file = open('save1.txt', 'r')
        values = store_file.readlines()
        for value in values:
            self.forbidden[value] = 1
        store_file.close()
        store_file = open('save2.txt', 'r')
        values = store_file.readlines()
        for value in values:
            self.memory[value] = 1
        store_file.close()
        store_file = open('save3.txt', 'r')
        for value in values:
            self.memory[value] = -1
        store_file.close()

    def get_evaluate(self, data):
        if self.memory.get(data) is None:
            return 0
        return self.memory.get(data)
