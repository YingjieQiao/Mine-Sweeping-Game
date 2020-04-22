from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from random import randint
import Global
import time
import math

##TODO: position and size
##understand layouts


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
        ## SM class the whole thing
        if self.button.collide_point(*touch.pos):
            if Global.first:
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
                    # more intuitive font and color and like "!!!"
                    self.difficulty.change_to_lose1()
            elif touch.button == "right":
                if self.isFlagged == 0:
                    self.isFlagged = 1
                    self.button.text = "*"
                    # more intuitive font and color and like "***"
                    Global.flagged += 1
                    if self.isMine == 1:
                        Global.effFlag += 1
                    if Global.flagged == self.difficulty.mines:
                        Global.end = time.time()
                        if Global.effFlag == self.difficulty.mines:
                            self.difficulty.change_to_win()
                        else:
                            self.difficulty.change_to_lose2()
                    # color change
                elif self.isFlagged == 1:
                    self.isFlagged = 0
                    self.button.text = " "
                    Global.flagged -= 1
                    if self.isMine == 1:
                        Global.effFlag -= 1
                    # color change
                # self.color = (225,225,126,1)
                # difference between background color and color attr
                # why it fixed the white at top right color bug

    def count_neighbors(self):
        if self.isMine == 0:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (0 <= self.location[0] + i < len(self.difficulty.field)) and (0 <= self.location[1] + j < len(self.difficulty.field[0])):
                        if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                            count += 1
                    '''
                    if Global.current = "easy":
                        if (0 <= self.location[0] + i < 10) and (0 <= self.location[1] + j < 10):
                            if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                                count += 1
                    elif Global.current = "medium":
                        if (0 <= self.location[0] + i < 18) and (0 <= self.location[1] + j < 18):
                            if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                                count += 1
                    else:
                        if (0 <= self.location[0] + i < 24) and (0 <= self.location[1] + j < 24):
                            if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                                count += 1
                    '''
            self.neighbors = count

    def reveal_zeros(self, gridObj):
        # gridObj is already confirmed to be 0 -- no mines in its surrounding
        for i in range(-1, 2):
            for j in range(-1, 2):
                #if (0 <= gridObj.location[0] + i < self.difficulty.width) and (0 <= gridObj.location[1] + j < self.difficulty.height):
                if (0 <= gridObj.location[0] + i < len(self.difficulty.field)) and (0 <= gridObj.location[1] + j < len(self.difficulty.field[0])):
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
        #win = Win(name="win")
        lose1 = Lose1(name="lose1")
        lose2 = Lose2(name="lose2")

        scrm.add_widget(menu)
        scrm.add_widget(gamemode)
        scrm.add_widget(easy)
        scrm.add_widget(medium)
        scrm.add_widget(hard)
        scrm.add_widget(scoreboard)
        #scrm.add_widget(win)
        scrm.add_widget(lose1)
        scrm.add_widget(lose2)

        scrm.current = "menu"
        return scrm


class Menu(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

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
        #self.manager.switch_to(gamemode, direction='up')

    def change_to_scoreboard(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "scoreboard"

    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()


class ScoreBoard(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        '''
        I think one way to implement with one scoreboard screen is:
        use a global function in the __init__
        no, __init__ is called only once when creating the obj
        so you need something that can be called over and over again in the scoreboard screen class
        '''
        print("init...")
        ############################ The UI here has to be better lmao ########################################

        self.layout = GridLayout(cols=1)
        self.scoreboard_label = Label(text="Score Board")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.scoreboard_label)

        data = []
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                # l0, l1, l2 = line.split()[0], line.split()[-2], line.split()[-1]
                segments = line.split()
                name = " "
                mode, score = segments[-2], segments[-1]
                if len(segments) == 3:
                    name = segments[0]
                elif len(segments) > 3:
                    name = name.join(segments[:-2])
                else:
                    name = "INPUT WAS EMPTY"
                data.append([name, mode, float(score)])
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

        self.layout = GridLayout(cols=1)
        self.scoreboard_label = Label(text="Score Board")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)

        self.layout.add_widget(self.scoreboard_label)

        data = []
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                # l0, l1, l2 = line.split()[0], line.split()[-2], line.split()[-1]
                segments = line.split()
                name = " "
                mode, score = segments[-2], segments[-1]
                if len(segments) == 3:
                    name = segments[0]
                elif len(segments) > 3:
                    name = name.join(segments[:-2])
                else:
                    name = "INPUT WAS EMPTY"
                data.append([name, mode, float(score)])
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


class GameMode(Screen):   ## SM here!
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

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
        self.manager.transition.direction = "up"
        self.manager.current = "easy"

    def change_to_medium(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "medium"

    def change_to_hard(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "hard"



class Easy(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.width = 10
        self.height = 10
        self.mines = 1
        self.layout = GridLayout(cols=10, rows=10)
        self.field = []
        self.init_grid()
        self.win_popup = Win(self)
        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def reinitialize(self):
        self.clear_widgets()
        print("reinitalizing...")
        '''
                for eachRow in self.field:
                    for each in eachRow:
                        each.button.text = " "
                        each.button.isMine = 0
                        each.button.isClicked = 0
                        each.button.isFlagged = 0
        '''
        Global.first = True
        self.field = []
        self.layout = GridLayout(cols=10, rows=10)
        self.init_grid()
        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def init_grid(self):
        for j in range(10):
            print("j= ", j)
            new = []
            for i in range(10):
                print("i=", i)
                new.append(Grid(self))
            self.field.append(new)

        #self.field = [[Grid(self) for i in range(self.width)] for j in range(self.height)]

        mineCount = 0
        while mineCount < self.mines:
            j = randint(0, 9)
            i = randint(0, 9)
            if self.field[j][i].isMine == 0:
                self.field[j][i].isMine = 1
                mineCount += 1

        for i in range(10):
            for j in range(10):
                self.field[j][i].build(j, i)
        print(len(self.field))
        print(len(self.field[0]))

    def change_to_win(self):

        #self.manager.transition.direction = "up"
        #self.manager.current = "win"
        #self.reinitialize()
        self.win_popup.open()

    def change_to_lose1(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose1"

    def change_to_lose2(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose2"

class Medium(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

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


    def change_to_lose1(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose1"

    def change_to_lose2(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose2"

class Hard(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

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

    def change_to_lose1(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose1"

    def change_to_lose2(self):
        self.manager.transition.direction = "up"
        self.manager.current = "lose2"

'''
class HeaderLabel
# for the name input part, bigger font
# can also do similar thing for other parts when polishing the UI
'''

class Win(Popup):
    def __init__(self, diffi, **kwargs):
        Popup.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.win_label = Label(text="Congratulations! You win!")
        self.score_button = Button(text="Click to continue", on_press=self.score)
        self.scoreAchieved = 0
        self.diffi = diffi

        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)
        self.add_widget(self.layout)


    def score(self, value):
        # you must add the "value" argument here lmfao
        self.layout.remove_widget(self.win_label)
        self.layout.remove_widget(self.score_button)
        scoreAchieved = 3000000*(Global.end-Global.start)
        self.scoreAchieved = scoreAchieved
        string = "Your score is " + str(scoreAchieved) + " !"
        self.score_label = Label(text=string)

        newHighScore = False
        highest = ["", "", 0]
        first = True

        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                segments = line.split()
                name = " "
                mode, score = segments[-2], float(segments[-1])
                if len(segments) == 3:
                    name = segments[0]
                elif len(segments) > 3:
                    name = name.join(segments[:-2])
                else:
                    name = "INPUT WAS EMPTY"
                if first:
                    highest = [name, mode, score]
                    first = False
                if score > highest[-1] and Global.current == highest[-2]:
                    highest = [name, mode, score]
        print(highest, scoreAchieved)
        if scoreAchieved > highest[-1] and Global.current == highest[-2]:
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
        self.highscore_button = Button(text="view scoreboard", on_press=self.change_to_scoreboard)
        self.yes_anotherGame_button = Button(text="another game", on_press=self.yes_anotherGame)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.highscore_button)
        self.layout.add_widget(self.yes_anotherGame_button)

    def change_to_scoreboard(self, value):
        with open("scores_local.txt", "a") as file:
            string = "\n" + str(self.name_input.text) + " " + str(Global.current) + " " + str(self.scoreAchieved)
            file.write(string)
        ScoreBoard().reinit()
        self.manager.transition.direction = "up"
        self.manager.current = "scoreboard"

    def no(self, value):
        self.no_anotherGame()

    def yes_anotherGame(self, value):
        self.layout.remove_widget(self.name_label)
        self.layout.remove_widget(self.name_input)
        self.layout.remove_widget(self.highscore_button)
        self.layout.remove_widget(self.yes_anotherGame_button)
        self.diffi.reinitialize()
        self.dismiss()
        #App.get_running_app().root.ids.Easy.reinitialize() ###
        #self.manager.transition.direction = "up"
        #self.manager.current = "gamemode"

    def no_anotherGame(self):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_label)
        self.layout.remove_widget(self.yes_button)
        self.layout.remove_widget(self.no_button)
        # TODO: reset the game

class Lose1(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = GridLayout(cols=1)

        self.lose_label1 = Label(text="You clicked on a mine... :(")
        self.lose_label2 = Label(text="Good luck next time!")
        self.exit_button = Button(text="exit game", on_press=self.exit_game)

        self.layout.add_widget(self.lose_label1)
        self.layout.add_widget(self.lose_label2)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()

class Lose2(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = GridLayout(cols=1)

        self.lose_label1 = Label(text="You misflagged a safe grid, and you didn't find out in the end... :(")
        self.lose_label2 = Label(text="Good luck next time!")
        self.exit_button = Button(text="exit game", on_press=self.exit_game)

        self.layout.add_widget(self.lose_label1)
        self.layout.add_widget(self.lose_label2)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()

## do a popup window

if __name__ == '__main__':
    MineSweep().run()


