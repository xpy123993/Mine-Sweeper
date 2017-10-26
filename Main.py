import Landscape
import Algorithms
import ui


def test_function(sweeper):
    print('*' * 20)
    print('Begin function correctness test')
    error_occurred = False
    for x in range(5):
        for y in range(5):
            pos = (x, y)
            if sweeper.get_valid_neighbours_number(pos) != len(sweeper.get_valid_neighbours(pos)):
                print(x, y)
                error_occurred = True
            if sweeper.get_uncovered_neighbours_number(pos) != len(sweeper.get_uncovered_neighbours(pos)):
                print(x, y)
                error_occurred = True
            if sweeper.get_covered_neighbours_number(pos) != len(sweeper.get_covered_neighbours(pos)):
                print(x, y)
                error_occurred = True
            if sweeper.get_mines_nearby_number(pos) != len(sweeper.get_mines_nearby(pos)):
                print(x, y)
                error_occurred = True
    if error_occurred:
        print('ERROR FOUND!!!')
    else:
        print('Check pass')
    print('Over')
    print('*' * 20)


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
    window = ui.Window(mines_count=15)
    window.init_graph()
    window.sweeper.error_note_enabled = True
    window.dialog()


drive()
