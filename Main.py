import Landscape
import Algorithms
import ui
import random

'''
Game-Set

Easy: 9*9 with 9 mines
Medium: 16*16 with 40 mines
Hard: 16*30 with 90 mines

win_rate_test:
batch play to measure the rate algorithm clear the landscape

drive:
pop a window to demonstrate

'''


def learning_patterns(case_number=10, number_per_case=101):
    sweeper = Algorithms.Sweeper()
    sweeper.learning_mode = False
    for i in range(5, case_number):
        success_count = 0
        for case_i in range(number_per_case):
            landscape = Landscape.Landscape(area_width=7, mines_count=5)
            sweeper.load(landscape)
            if sweeper.run():
                success_count += 1
        print('%g%%' % round(100.0 * success_count / number_per_case, 2))
        sweeper.inference_message = ''


def drive():
    window = ui.Window(mines_count=50, map_width=20, window_size=(1000, 800))
    window.dialog()


# learning_patterns()
drive()
