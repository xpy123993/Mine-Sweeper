import Landscape
import Algorithms
import ui


'''
Game-Set

Easy: 9*9 with 9 mines
Medium: 16*16 with 40 mines
Hard: 16*30 with 90 mines

'''


def batch_drive():
    case_number = 1000
    number_per_case = 1000

    sweeper = Algorithms.Sweeper()
    sweeper.error_note_enabled = True  # enable auto self-correct mode
    import random
    for i in range(case_number):
        success_count = 0
        cache_total_count = cache_correct_count = 0
        for case_i in range(number_per_case):
            landscape = Landscape.Landscape(area_width=random.randint(5, 10), mines_count=random.randint(5, 20))
            sweeper.load(landscape)
            success = sweeper.run()
            cache_total_count += sweeper.error_total_count
            cache_correct_count += sweeper.error_correct_count
            if success:
                success_count += 1
        print('Correct Rate = %g%%' % round(100.0 * success_count / number_per_case, 2))

        # test_function(sweeper)


def drive():
    window = ui.Window(mines_count=18)
    window.init_graph()
    window.sweeper.error_note_enabled = True
    window.dialog()


batch_drive()
