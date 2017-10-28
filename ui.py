import numpy
import tkinter
import tkinter.scrolledtext
import Landscape
import Algorithms

'''
UI FORM

class Window

def __init__(window_size, map_width, mines_count):
window_size: the pixel size of this window
map_width: the width of mines landscape
mines_count: the number of mines the landscape has

def dialog():   show this window as a dialog
'''

default_window_size = (950, 650)


class Window:
    main_frame = tkinter.Tk()
    frame_size = default_window_size
    mines_text = dict()
    mines_button = dict()

    risk_hint = None
    game_hint = None
    game_text = None

    sweeper = None
    landscape = None

    map_width = 0
    mines_count = 0

    uncovered_color = '#EEEEEE'
    covered_color = '#FF0000'

    instruction_hint = 'INSTRUCTIONS\nPlease press next.\nthe program explore the cells by itself.\n' \
                       'When the program can decide which cell to uncover next, \nit will explore automatic. \n' \
                       'When the program cannot decide which cell to reveal next by given clues, \nit will suspend. ' \
                       '\nThen the user needs to click the next button, \n' \
                       'the program will use evaluate the risk to uncover a cell of the information is not enough, \n' \
                       'the program will continue.\n'

    available_moves = []
    moves_probability = []
    moves_e_probability = []

    def set_size(self, window_size):
        par = str(window_size[0]) + 'x' + str(window_size[1])
        self.frame_size = window_size
        self.main_frame.geometry(par)

    def __init__(self, window_size=default_window_size, map_width=10, mines_count=10):
        self.set_size(window_size)
        self.landscape = Landscape.Landscape(map_width, mines_count)
        self.sweeper = Algorithms.Sweeper()
        self.sweeper.load(self.landscape)
        self.map_width = map_width
        self.mines_count = mines_count
        self.init_graph()

    def reset_game(self):
        self.landscape = Landscape.Landscape(self.map_width, self.mines_count)
        for key in self.mines_button.keys():
            self.mines_button[key]['background'] = self.main_frame['background']
            self.mines_button[key]['state'] = tkinter.NORMAL
            self.mines_text[key].set(' ')
        self.sweeper.load(self.landscape)
        self.game_text.delete(0.0, tkinter.END)

    def draw_mines_area(self):
        # mines_data = numpy.zeros(shape=[10, 10])

        for i in range(self.landscape.area_width):
            for j in range(self.landscape.area_width):
                bn_key = str(i) + '_' + str(j)
                bn_state = tkinter.NORMAL
                bn_title = ' '
                if self.sweeper.uncovered_location[i, j] == 1:
                    bn_state = tkinter.DISABLED

                    e_v = self.sweeper.explored_map[i, j]
                    if e_v == -1:
                        bn_title = '*'
                    elif e_v == -2:
                        bn_title = 'X'
                    elif e_v > 0:
                        bn_title = str(e_v)
                else:
                    bn_state = tkinter.NORMAL
                self.mines_text[bn_key].set(bn_title)
                self.mines_button[bn_key]['state'] = bn_state
                self.mines_button[bn_key]['background'] = self.covered_color
                if bn_state == tkinter.DISABLED:
                    self.mines_button[bn_key]['background'] = self.uncovered_color

    def init_graph(self):

        label = tkinter.Label(self.main_frame)
        label.grid(row=0, column=0, padx=10, pady=10)
        self.game_hint = tkinter.StringVar()
        label['textvariable'] = self.game_hint

        self.risk_hint = tkinter.StringVar()
        slabel = tkinter.Label(self.main_frame)
        slabel['textvariable'] = self.risk_hint
        slabel.grid(row=0, column=1, padx=10, pady=10)

        mine_frame = tkinter.Frame(self.main_frame)
        mine_frame.grid(row=1, column=0, padx=10)
        self.main_frame.title('MineSweeper')

        def button_click(i, j):

            is_game_over = self.sweeper.explore((i, j))
            if not is_game_over:
                self.available_moves, self.moves_probability, self.moves_e_probability = \
                    self.sweeper.demonstrate_half_auto()

            if is_game_over:
                self.game_hint.set('GAME OVER, LOST')
                self.sweeper.explored_map = self.landscape.get_all_game_map()
                self.sweeper.uncovered_location = numpy.ones(
                    shape=[self.landscape.area_width, self.landscape.area_width])
                self.sweeper.uncovered_count = self.landscape.area_width * self.landscape.area_width
                self.draw_mines_area()
                for key in self.mines_button.keys():
                    self.mines_button[key]['background'] = '#ffbbbb'
            elif self.sweeper.uncovered_count == self.landscape.area_width * self.landscape.area_width:
                self.game_hint.set('GAME OVER, WIN')
                self.draw_mines_area()
                for key in self.mines_button.keys():
                    self.mines_button[key]['background'] = '#bbffbb'
            else:
                self.draw_mines_area()
                self.game_hint.set(
                    'Current Status: Playing, Remaining mines: %g' % self.sweeper.remain_mines)
        def auto_explore():

            is_game_over = self.sweeper.stepbystep() != 1

            if not is_game_over:
                self.available_moves, self.moves_probability, self.moves_e_probability = \
                    self.sweeper.demonstrate_half_auto()

            if self.sweeper.uncovered_count == self.landscape.area_width * self.landscape.area_width:
                self.game_hint.set('GAME OVER, WIN')
                self.draw_mines_area()
                for key in self.mines_button.keys():
                    self.mines_button[key]['background'] = '#bbffbb'
            elif is_game_over:

                self.game_hint.set('GAME OVER, LOST')
                self.sweeper.explored_map = self.landscape.get_all_game_map()
                self.sweeper.uncovered_location = numpy.ones(
                    shape=[self.landscape.area_width, self.landscape.area_width])
                self.sweeper.uncovered_count = self.landscape.area_width * self.landscape.area_width
                self.draw_mines_area()
                for key in self.mines_button.keys():
                    self.mines_button[key]['background'] = '#ffbbbb'
            else:
                self.draw_mines_area()
                self.game_hint.set(
                    'Current Status: Playing, Remaining mines: %g' % self.sweeper.remain_mines)

            self.game_text.insert(tkinter.END, self.sweeper.inference_message)
            self.sweeper.inference_message = ''
            self.game_text.see(tkinter.END)

        def button_hover(i, j):
            position_hint = 'Current Position:(%g, %g)' % (i, j)
            self.risk_hint.set('%s' % position_hint)
            for k in range(len(self.available_moves)):
                x, y = self.available_moves[k]
                if x == i and y == j:
                    risk_hint = 'Evaluated Risk: %g%% (%s%g%% by experience)' \
                                % (round(100 * self.moves_probability[k], 2),
                                   '+' if self.moves_e_probability[k] >= 0 else '',
                                   round(100 * self.moves_e_probability[k], 2))
                    self.risk_hint.set('%s, %s' % (position_hint, risk_hint))

        for i in range(self.landscape.area_width):
            for j in range(self.landscape.area_width):
                button_title = ' '
                button = tkinter.Button(mine_frame, width=2, height=2,
                                        state=tkinter.NORMAL,
                                        text=button_title, command=lambda i=i, j=j: button_click(i, j))
                button.bind('<Enter>', lambda event, i=i, j=j: button_hover(i, j))
                button.grid(row=i + 1, column=j + 1)
                var = tkinter.StringVar()
                self.mines_text[str(i) + '_' + str(j)] = var
                button['textvariable'] = var

                self.mines_button[str(i) + '_' + str(j)] = button
        for i in range(self.landscape.area_width):
            label = tkinter.Label(mine_frame, text=str(i))
            label.grid(row=0, column=i + 1)
            label = tkinter.Label(mine_frame, text=str(i))
            label.grid(row=i + 1, column=0)
        label = tkinter.Label(mine_frame, text='POS')
        label.grid(row=0, column=0)

        reset_button = tkinter.Button(self.main_frame, text='Restart', command=lambda: self.reset_game())
        reset_button.grid(row=2, column=0, padx=10, pady=10)

        next_button = tkinter.Button(self.main_frame, text='Next', command=lambda: auto_explore())
        next_button.grid(row=2, column=1, padx=10, pady=10)

        label_frame = tkinter.scrolledtext.ScrolledText(self.main_frame, width=60, height=38)
        label_frame.grid(row=1, column=1, padx=10)
        self.game_text = label_frame
        label_frame.insert(tkinter.END, self.instruction_hint)

    def dialog(self):
        self.main_frame.mainloop()
