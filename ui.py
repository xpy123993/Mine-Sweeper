import numpy
import tkinter
import tkinter.scrolledtext
import Landscape
import Algorithms

default_window_size = (950, 600)


class Window:
    main_frame = tkinter.Tk()
    frame_size = default_window_size
    mines_text = dict()
    mines_button = dict()

    game_hint = None
    game_text = None

    sweeper = None
    landscape = None

    work_mode = 'auto'

    map_width = 0
    mines_count = 0

    uncovered_color = '#BBBBBB'

    def set_size(self, window_size):
        par = str(window_size[0]) + 'x' + str(window_size[1])
        self.frame_size = window_size
        self.main_frame.geometry(par)

    def __init__(self, window_size=default_window_size, work_mode='half_auto', map_width=10, mines_count=10):
        self.set_size(window_size)
        self.landscape = Landscape.Landscape(map_width, mines_count)
        self.work_mode = work_mode
        self.sweeper = Algorithms.Sweeper()
        self.sweeper.load(self.landscape)
        self.map_width = map_width
        self.mines_count = mines_count

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
                if bn_state == tkinter.DISABLED:
                    self.mines_button[bn_key]['background'] = self.uncovered_color

    def init_graph(self):

        label = tkinter.Label(self.main_frame)
        label.grid(row=0, column=0, padx=10, pady=10)
        self.game_hint = tkinter.StringVar()
        label['textvariable'] = self.game_hint

        mine_frame = tkinter.Frame(self.main_frame)
        mine_frame.grid(row=1, column=0, padx=10)

        def button_click(i, j):

            is_game_over = self.sweeper.explore((i, j))
            if not is_game_over:
                self.sweeper.demonstrate_half_auto()

            if is_game_over:
                self.game_hint.set('GAME OVER, LOST')
                self.sweeper.explored_map = self.landscape.get_all_game_map()
                self.sweeper.uncovered_location = numpy.ones(
                    shape=[self.landscape.area_width, self.landscape.area_width])
                self.sweeper.uncovered_count = self.landscape.area_width * self.landscape.area_width
            elif self.sweeper.uncovered_count == self.landscape.area_width * self.landscape.area_width:
                self.game_hint.set('GAME OVER, WIN')
            else:
                self.game_hint.set(
                    'Current Status: Playing, Remaining mines: %g' % (self.sweeper.remain_mines))
            self.draw_mines_area()
            self.game_text.insert(tkinter.END, self.sweeper.inference_message)
            self.sweeper.inference_message = ''
            self.game_text.see(tkinter.END)

        for i in range(self.landscape.area_width):
            for j in range(self.landscape.area_width):
                button_title = ' '
                button = tkinter.Button(mine_frame, width=5, height=2,
                                        state=tkinter.NORMAL,
                                        text=button_title, command=lambda i=i, j=j: button_click(i, j))

                button.grid(row=i, column=j)
                var = tkinter.StringVar()
                self.mines_text[str(i) + '_' + str(j)] = var
                button['textvariable'] = var

                self.mines_button[str(i) + '_' + str(j)] = button

        reset_button = tkinter.Button(self.main_frame, text='RESET', command=lambda: self.reset_game())
        reset_button.grid(row=2, column=0, padx=10, pady=10)

        label_frame = tkinter.scrolledtext.ScrolledText(self.main_frame, width=60, height=36)
        label_frame.grid(row=1, column=1, padx=10)
        self.game_text = label_frame

    def dialog(self):
        self.main_frame.mainloop()
