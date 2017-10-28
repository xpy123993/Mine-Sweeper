import Landscape
import Algorithms
import ui
import random
#import sys

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


def MineSweeperOnce(area_width,minesnum,check):
    sweeper = Algorithms.Sweeper()
    sweeper.learning_mode = False
    landscape = Landscape.Landscape(area_width, minesnum)
    sweeper.load(landscape)
    flag,result = sweeper.run()
    if flag:
        return flag,result,landscape
    return False,0,""

def learning_patterns( number_per_case=1000):
    width = 9
    mines = 18
    check = False
    while mines > 0:
        Dict = {}
        success_count = 0
        for case_i in range(number_per_case):
            if case_i % 20 == 0:
                check = True
            flag,chainlen,mapdata = MineSweeperOnce(width,mines,check)
            if flag:
                success_count += 1
                Dict[chainlen] = mapdata
        Goal = sorted(Dict.items(),key = lambda x:x[0])
        #print(Goal)
        print("the longest length of chain:%s" % Goal[-1][0])
        print("the minemap with the longest chain:\n", Goal[-1][1].data)
        print('Width:%s,Mines:%s,Correct Rate = %g%%' % (width,mines,round(100.0 * success_count / number_per_case, 2)))
        print()
        mines -= 1

def drive():
    window = ui.Window(mines_count=18, map_width=10)
    window.dialog()


if __name__ == "__main__":
     learning_patterns()
#    arg = sys.argv[1]
#    if "semiauto" == arg:
#        drive()
#    elif "auto" == arg:
#        learning_patterns()
#    else:
#        print("wrong argument!")
