import Landscape
import Algorithms


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


def drive():
    case_number = 100
    number_per_case = 1000

    sweeper = Algorithms.Sweeper()

    for i in range(case_number):
        sum = 0
        for case_i in range(number_per_case):
            landscape = Landscape.Landscape(area_width=5, mines_count=5)
            sweeper.load(landscape)
            success = sweeper.run()
            if success:
                sum += 1

        print('Correct Rate = ', round(100.0 * sum / number_per_case, 2), '%')
        # test_function(sweeper)


drive()
