from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.label import Label
from kivy.interactive import InteractiveLauncher
from kivy.uix.textinput import TextInput  # name for scoreboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from random import randint
import Global

##TODO: position and size
##understand layouts


def init_grid(width, height, mines, difficulty):
    # "difficulty" is the game screen object
    # Initiate the gird field with empty grids
    grid_field = [[Grid(difficulty) for i in range(width)] for j in range(height)]
    '''
    Interprete the grid field as a MATRIX
    the i above is the column index, which adds up to WIDTH
    the j above is the row index, which adds up to HEIGHT
    '''
    # ======================================================
    '''
    grid_field[y][x]
    j is the row index, which adds up to HEIGHT
    i is the column index, which adds up to WIDTH
    '''
    # generate mines
    mineCount = 0
    while mineCount < mines:
        i = randint(0, height - 1)
        j = randint(0, width - 1)
        if grid_field[j][i].isMine == 0:
            grid_field[j][i].isMine = 1
            mineCount += 1
    return grid_field

def build_field(grid_field, width, height):
    # fill mines into the grid field
    for i in range(width):
        for j in range(height):
            grid_field[j][i].build(j, i)
    return grid_field

class Grid():
    def __init__(self, difficulty, **kwargs):
        self.isMine = 0
        self.isClicked = 0
        self.isFlagged = 0
        self.neighbors = 0
        self.location = []  # (height_index, width_index)
        self.button = Button(size=(Global.gridSize, Global.gridSize))
        self.button.bind(on_touch_down=self.onPressed)
        self.difficulty = difficulty

    def build(self, x, y):
        self.location = [x, y]
        self.count_neighbors()

    def onPressed(self, instance, touch):
        #global flagged
        if self.button.collide_point(*touch.pos):
            if touch.button == "left":
                self.isClicked = 1
                if self.isMine == 0:
                    self.button.text = str(self.neighbors)
                    if self.neighbors == 0:
                        global neighbor_grids
                        neighbor_grids = []
                        neighbor_grids.append(self)
                        while len(neighbor_grids) > 0:
                            self.reveal_zeros(neighbor_grids[0])
                            neighbor_grids.remove(neighbor_grids[0])
                    else:
                        self.button.text = str(self.neighbors)
                else:
                    self.button.text = "!"
                    # more intuitive font and colr and like "!!!"
                    ### trigger lose
                    print("game over!")
            elif touch.button == "right":
                if self.isFlagged == 0:
                    self.isFlagged = 1
                    self.button.text = "*"
                    # more intuitive font and colr and like "***"
                    Global.flagged += 1
                    if Global.flagged == Global.mines:
                        self.difficulty.change_to_win()
                    # color change
                elif self.isFlagged == 1:
                    self.isFlagged = 0
                    self.button.text = " "
                    Global.flagged -= 1
                    # color change
                # self.color = (225,225,126,1)
                # difference between background color and color attr
                # why it fixed the white at top right color bug

    def count_neighbors(self):
        if self.isMine == 0:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (0 <= self.location[0] + i < self.difficulty.width) and (0 <= self.location[1] + j < self.difficulty.height):
                        if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                            count += 1
            self.neighbors = count

    def reveal_zeros(self, gridObj):
        # gridObj is already confirmed to be 0 -- no mines in its surrounding
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= gridObj.location[0] + i < Global.width) and (0 <= gridObj.location[1] + j < Global.height):
                    check = self.difficulty.field[gridObj.location[0] + i][gridObj.location[1] + j]
                    if check.isClicked == 0 and check.neighbors == 0 and check.isMine == 0:
                        check.button.text = str(check.neighbors)
                        check.isClicked = 1
                        if check not in neighbor_grids:
                            neighbor_grids.append(check)


class MineSweep(App):
    def build(self):
        scrm = ScreenManager()

        menu = Menu(name="menu")
        scoreboard = ScoreBoard(name="scoreboard")
        gamemode = GameMode(name="gamemode")
        easy = Easy(name="easy")
        medium = Medium(name="medium")
        hard = Hard(name="hard")
        win = Win(name="win")
        lose = Lose(name="lose")

        scrm.add_widget(menu)
        scrm.add_widget(gamemode)
        scrm.add_widget(easy)
        scrm.add_widget(medium)
        scrm.add_widget(hard)
        scrm.add_widget(scoreboard)
        scrm.add_widget(win)
        scrm.add_widget(lose)

        scrm.current = "menu"
        return scrm


class Menu(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.start_button = Button(text="Start Game", on_press=self.change_to_gamemode)
        self.scoreboard_button = Button(text="scoreboard", on_press=self.change_to_scoreboard)
        # why here no paranthesis??
        self.quit_button = Button(text="Quit", on_press=self.quit_app)

        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.scoreboard_button)
        self.layout.add_widget(self.quit_button)

        self.add_widget(self.layout)

    def change_to_gamemode(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_scoreboard(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "scoreboard"

    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()


class ScoreBoard(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.scoreboard_label = Label(text="Score Board")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.scoreboard_label)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def change_to_menu(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"


class GameMode(Screen, GridLayout):   ## SM here!
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.gamemode_label = Label(text="Select Difficulty")
        self.easy_button = Button(text="Easy", on_press=self.change_to_easy)
        self.medium_button = Button(text="Medium", on_press=self.change_to_medium)
        self.hard_button = Button(text="Hard", on_press=self.change_to_hard)
        self.customize_button = Button(text="Customized Game", on_press=self.change_to_customize)
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.gamemode_label)
        self.layout.add_widget(self.easy_button)
        self.layout.add_widget(self.medium_button)
        self.layout.add_widget(self.hard_button)
        self.layout.add_widget(self.customize_button)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def change_to_menu(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_easy(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "easy"

    def change_to_medium(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "medium"

    def change_to_hard(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "hard"

    def change_to_customize(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "customize"




class Easy(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.width = 10
        self.height = 10
        self.mines = 1
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def change_to_win(self):
        self.manager.transition.direction = "up"
        self.manager.current = "win"

class Medium(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.width = 18
        self.height = 18
        self.mines = 1
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def change_to_win(self):
        self.manager.transition.direction = "up"
        self.manager.current = "win"

class Hard(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.width = 24
        self.height = 24
        self.mines = 1
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def change_to_win(self):
        self.manager.transition.direction = "up"
        self.manager.current = "win"


class Win(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.win_label = Label(text="You fucking win")

        self.layout.add_widget(self.win_label)
        self.add_widget(self.layout)


class Lose(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)


if __name__ == '__main__':
    MineSweep().run()


