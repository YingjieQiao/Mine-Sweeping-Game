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
from random import randint
import Global
import time
import math
import copy

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
        if self.button.collide_point(*touch.pos):
            if Global.first:
                # for scoring
                Global.start = time.time()
                Global.current = self.difficulty.name
                Global.first = False
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
                    if Global.flagged == self.difficulty.mines:
                        Global.end = time.time()
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
        game = Game(name="game")
        win = Win(name="win")
        lose = Lose(name="lose")

        scrm.add_widget(menu)
        scrm.add_widget(gamemode)
        scrm.add_widget(game)
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

        '''
        I think one way to implement with one scoreboard screen is:
        use a global function in the __init__
        no, __init__ is called only once
        so you need something that can be called over and over again in the scoreboard screen class
        '''
        print("init...")
        ############################ The UI here has to be better lmfao ########################################

        self.layout = GridLayout(cols=1)
        self.scoreboard_label = Label(text="Score Board")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.scoreboard_label)

        data = []
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                l0, l1, l2 = line.split()[0], line.split()[1], line.split()[2]
                ## Catch the error: name can be empty
                data.append([l0, l1, float(l2)])
        data.sort(key=lambda x: x[2], reverse=True)

        for line in data:
            string = str(line[0]) + " " + str(line[1]) + " " + str(line[2])
            self.score_label = Label(text=string)
            self.layout.add_widget(self.score_label)

        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def reinit(self, **kwargs):
        print("reinit...")
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        '''
        I think one way to implement with one scoreboard screen is:
        use a global function in the __init__
        no, __init__ is called only once
        so you need something that can be called over and over again in the scoreboard screen class
        '''

        ############################ The UI here has to be better lmfao ########################################

        self.layout = GridLayout(cols=1)
        self.scoreboard_label = Label(text="Score Board")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.scoreboard_label)

        data = []
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                l0, l1, l2 = line.split()[0], line.split()[1], line.split()[2]
                data.append([l0, l1, float(l2)])
        data.sort(key=lambda x: x[2], reverse=True)

        for line in data:
            string = str(line[0]) + " " + str(line[1]) + " " + str(line[2])
            self.score_label = Label(text=string)
            self.layout.add_widget(self.score_label)

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
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.gamemode_label)
        self.layout.add_widget(self.easy_button)
        self.layout.add_widget(self.medium_button)
        self.layout.add_widget(self.hard_button)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def change_to_menu(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_easy(self, value):
        Game().init_easy()
        self.manager.transition.direction = "up"
        self.manager.current = "game"

    def change_to_medium(self, value):
        Game().init_medium()
        self.manager.transition.direction = "up"
        self.manager.current = "game"

    def change_to_hard(self, value):
        Game().init_hard()
        self.manager.transition.direction = "up"
        self.manager.current = "game"

class Game(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

    def init_easy(self):
        self.width = 10
        self.height = 10
        self.mines = 1
        self.field = []
        self.initialize()

    def init_medium(self):
        self.width = 18
        self.height = 18
        self.mines = 1
        self.field = []
        self.initialize()

    def init_hard(self):
        self.width = 24
        self.height = 24
        self.mines = 1
        self.field = []
        self.initialize()

    def initialize(self):
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)
        print("initializing...")

    def reinitialize(self):
        print("reinitalizing...")
        self.remove_widget(self.layout)
        #self.layout = GridLayout(cols=self.height, rows=self.width)
        '''
        
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)
        '''
        #self.label = Label(text="god damn it")
        #self.layout.add_widget(self.label)

    def change_to_win(self):
        self.manager.transition.direction = "up"
        self.manager.current = "win"



'''
class HeaderLabel
# for the name input part, bigger font
# can also do similar thing for other parts when polishing the UI
'''

class Win(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.win_label = Label(text="Congratulations! You win!")
        self.score_button = Button(text="Click to continue", on_press=self.score)
        self.scoreAchieved = 0

        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)
        self.add_widget(self.layout)


    def score(self, value):
        # you must add the "value" argument here lmfao
        self.layout.remove_widget(self.win_label)
        self.layout.remove_widget(self.score_button)
        scoreAchieved = 30000/(Global.end-Global.start)
        self.scoreAchieved = scoreAchieved
        string = "Your score is " + str(scoreAchieved) + " !"
        self.score_label = Label(text=string)

        newHighScore = False
        highest = ["", "", 0]
        dic = {}
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                name, mode, score = line.split()[0], line.split()[1], float(line.split()[2])
                if score > highest[2] and Global.current == highest[1]:
                    highest = [name, mode, score]
        if scoreAchieved > highest[2]:
            newHighScore = True
        if newHighScore == True:
            self.hi_label = Label(text="You have reached a new high score in this difficulty! Would you like to put your name onto the scoreboard?")
            self.yes_button = Button(text="Yes!", on_press=self.yes)
            self.no_button = Button(text="Nah...", on_press=self.no)
            self.layout.add_widget(self.score_label)
            self.layout.add_widget(self.hi_label)
            self.layout.add_widget(self.yes_button)
            self.layout.add_widget(self.no_button)
        else:
            #anotherGame
            self.anotherGame_button = Button(text="another game")
            self.menu_button = Button(text="Back to menu", on_press=self.change_to_menu)
            # TODO: reset the game
            self.layout.add_widget(self.score_label)
            self.layout.add_widget(self.anotherGame_button)
            self.layout.add_widget(self.menu_button)

    def change_to_menu(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "menu"

    def yes(self, value):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_label)
        self.layout.remove_widget(self.yes_button)
        self.layout.remove_widget(self.no_button)

        self.name_label = Label(text="Your name:")
        self.name_input = TextInput()
        #self.highscore_button = Button(text="view scoreboard", on_press=self.change_to_scoreboard)
        self.yes_anotherGame_button = Button(text="another game", on_press=self.yes_anotherGame)
        self.menu_button = Button(text="Back to menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        #self.layout.add_widget(self.highscore_button)
        self.layout.add_widget(self.yes_anotherGame_button)
        self.layout.add_widget(self.menu_button)
    '''
    def change_to_scoreboard(self, value):
        with open("scores_local.txt", "a") as file:
            string = "\n" + str(self.name_input.text) + " " + str(Global.current) + " " + str(self.scoreAchieved)
            file.write(string)
        ScoreBoard().reinit()
        self.manager.transition.direction = "up"
        self.manager.current = "scoreboard"
    '''
    def no(self, value):
        self.no_anotherGame()

    def yes_anotherGame(self, value):
        Global.first = False

        self.layout.remove_widget(self.name_label)
        self.layout.remove_widget(self.name_input)
        #self.layout.remove_widget(self.highscore_button)
        self.layout.remove_widget(self.yes_anotherGame_button)
        Easy().reinitialize()
        # doesn't work

        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def no_anotherGame(self):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_label)
        self.layout.remove_widget(self.yes_button)
        self.layout.remove_widget(self.no_button)
        # TODO: reset the game
        self.anotherGame_button = Button(text="another game?")
        self.menu_button = Button(text="Back to menu", on_press=self.change_to_menu)
        self.layout.add_widget(self.anotherGame_button)
        self.layout.add_widget(self.menu_button)

class Lose(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)


if __name__ == '__main__':
    MineSweep().run()


