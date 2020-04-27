from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from random import randint
import time
import math
import Global



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
                    self.difficulty.change_to_lose1()
            elif touch.button == "right":
                if self.isFlagged == 0:
                    self.isFlagged = 1
                    self.button.text = "*"
                    self.button.background_color=[42/255, 193/255, 213/255, 1]
                    Global.flagged += 1
                    if self.isMine == 1:
                        Global.effFlag += 1
                    if Global.flagged == self.difficulty.mines:
                        Global.end = time.time()
                        if Global.effFlag == self.difficulty.mines:
                            self.difficulty.change_to_win()
                        else:
                            self.difficulty.change_to_lose2()
                elif self.isFlagged == 1:
                    self.isFlagged = 0
                    self.button.text = " "
                    self.button.background_color = [1, 1, 1, 1]
                    Global.flagged -= 1
                    if self.isMine == 1:
                        Global.effFlag -= 1

    def count_neighbors(self):
        if self.isMine == 0:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (0 <= self.location[0] + i < len(self.difficulty.field)) and (0 <= self.location[1] + j < len(self.difficulty.field[0])):
                        if self.difficulty.field[self.location[0] + i][self.location[1] + j].isMine == 1:
                            count += 1
            self.neighbors = count

    def reveal_zeros(self, gridObj):
        # gridObj is already confirmed to be 0 -- no mines in its surrounding
        for i in range(-1, 2):
            for j in range(-1, 2):
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
        gamemode = GameMode(name="gamemode")
        easy = Easy(name="easy")
        medium = Medium(name="medium")
        hard = Hard(name="hard")

        scrm.add_widget(menu)
        scrm.add_widget(gamemode)
        scrm.add_widget(easy)
        scrm.add_widget(medium)
        scrm.add_widget(hard)

        scrm.current = "menu"
        return scrm


class Menu(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        title_text="[color=ff8000][size=64]MineSweeper!\n[/size][size=48]Crafted by Yingjie[/size][/color]"
        self.title = Label(text=title_text, markup=True, valign="middle")
        self.start_button = Button(text="Start Game", font_size=48, on_press=self.change_to_gamemode)
        self.scoreboard_button = Button(text="Scoreboard", font_size=48, on_press=self.change_to_scoreboard)
        self.exit_button = Button(text="Exit Game", font_size=48, on_press=self.exit_game)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.scoreboard_button)
        self.layout.add_widget(self.exit_button)
        self.add_widget(self.layout)

    def change_to_gamemode(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_scoreboard(self, value):
        self.scrbd_popup = ScoreBoard(self)
        self.scrbd_popup.open()

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()


class ScoreBoard(Popup):
    def __init__(self, obj, **kwargs):
        # prepare interview about this passing obj here
        Popup.__init__(self, **kwargs)
        self.init(obj)

    def init(self, obj):
        self.layout = BoxLayout(orientation='vertical')
        self.top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        self.bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        self.data_grid = GridLayout(cols=3)
        self.title = "ScoreBoard"
        self.obj = obj

        self.scoreboard_label = Label(text="Scoreboard -- Hall of Fame", font_size=48, color=[213/255, 116/255, 42/255, 1])
        self.menu_button = Button(text="Back to Menu", font_size=48, on_press=self.change_to_menu)
        self.top_bar.add_widget(self.scoreboard_label)
        self.layout.add_widget(self.top_bar)

        data = []
        with open("scores_local.txt") as file:
            lines = file.readlines()
            for line in lines:
                segments = line.split()
                name = " "
                if len(segments) >= 2:
                    mode, score = segments[-2], segments[-1]
                    if len(segments) == 3:
                        name = segments[0]
                    elif len(segments) > 3:
                        name = name.join(segments[:-2])
                    else:
                        name = "[SYSTEM]: INPUT WAS EMPTY"
                    data.append([name, mode, float(score)])
                else:
                    pass
        data.sort(key=lambda x: x[2], reverse=True) ### explain

        self.name = Label(text="[color=492ad5][b]Name[/b][/color]", markup=True)
        self.mode = Label(text="[color=492ad5][b]Difficulty[/b][/color]", markup=True)
        self.score = Label(text="[color=492ad5][b]Score[/b][/color]", markup=True)
        self.data_grid.add_widget(self.name)
        self.data_grid.add_widget(self.mode)
        self.data_grid.add_widget(self.score)
        for line in data:
            self.label1 = Label(text=str(line[0]))
            self.label2 = Label(text=str(line[1]))
            self.label3 = Label(text=str(line[2]))
            self.data_grid.add_widget(self.label1)
            self.data_grid.add_widget(self.label2)
            self.data_grid.add_widget(self.label3)
        self.layout.add_widget(self.data_grid)
        self.bottom_bar.add_widget(self.menu_button)
        self.layout.add_widget(self.bottom_bar)
        self.add_widget(self.layout)

    def change_to_menu(self, value):
        self.obj.manager.transition.direction = "down"
        self.obj.manager.current = "menu"
        self.dismiss()


class GameMode(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        self.layout = GridLayout(cols=1)
        self.gamemode_label = Label(text="Select Difficulty", font_size=48, color=[213/255, 116/255, 42/255, 1])
        self.easy_button = Button(text="Easy", font_size=48, on_press=self.change_to_easy)
        self.medium_button = Button(text="Medium", font_size=48, on_press=self.change_to_medium)
        self.hard_button = Button(text="Hard", font_size=48, on_press=self.change_to_hard)
        self.menu_button = Button(text="Back to Menu", font_size=48, on_press=self.change_to_menu)

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
        self.mines = 10
        self.win_popup = Win(self)
        self.lose1_popup = Lose1(self)
        self.lose2_popup = Lose2(self)
        self.init()

    def init(self):
        self.root_layout = BoxLayout(orientation="vertical")
        self.layout = GridLayout(cols=10, rows=10)
        self.bottom_bar = BoxLayout(orientation="horizontal", size_hint_y=0.125)
        self.change_to_menu_button = Button(text="Give up this game, back to menu", font_size=24,
                                            background_color=[228/255, 201/255, 27/255, 1], on_press=self.change_to_menu)
        self.field = []
        self.init_grid()

        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.root_layout.add_widget(self.layout)

        self.bottom_bar.add_widget(self.change_to_menu_button)
        self.root_layout.add_widget(self.bottom_bar)

        self.add_widget(self.root_layout)

    def reinitialize(self):
        self.clear_widgets()
        Global.first = True
        Global.flagged = 0
        Global.effFlag = 0
        Global.current = ""
        self.init()

    def init_grid(self):
        for j in range(10):
            new = []
            for i in range(10):
                new.append(Grid(self))
            self.field.append(new)

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

    def change_to_menu(self, value):
        self.reinitialize()
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_menu_win(self):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_win(self):
        self.win_popup.open()

    def change_to_gamemode(self):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_lose1(self):
        self.lose1_popup.open()

    def change_to_lose2(self):
        self.lose2_popup.open()


class Medium(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.width = 18
        self.height = 18
        self.mines = 32
        self.win_popup = Win(self)
        self.lose1_popup = Lose1(self)
        self.lose2_popup = Lose2(self)
        self.init()

    def init(self):
        self.root_layout = BoxLayout(orientation="vertical")
        self.layout = GridLayout(cols=18, rows=18)
        self.bottom_bar = BoxLayout(orientation="horizontal", size_hint_y=0.125)
        self.change_to_menu_button = Button(text="Give up this game, back to menu", font_size=24,
                                            background_color=[228/255, 201/255, 27/255, 1], on_press=self.change_to_menu)
        self.field = []
        self.init_grid()

        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.root_layout.add_widget(self.layout)

        self.bottom_bar.add_widget(self.change_to_menu_button)
        self.root_layout.add_widget(self.bottom_bar)

        self.add_widget(self.root_layout)

    def reinitialize(self):
        self.clear_widgets()
        Global.first = True
        Global.flagged = 0
        Global.effFlag = 0
        Global.current = ""
        self.init()

    def init_grid(self):
        for j in range(18):
            new = []
            for i in range(18):
                new.append(Grid(self))
            self.field.append(new)

        mineCount = 0
        while mineCount < self.mines:
            j = randint(0, 17)
            i = randint(0, 17)
            if self.field[j][i].isMine == 0:
                self.field[j][i].isMine = 1
                mineCount += 1

        for i in range(18):
            for j in range(18):
                self.field[j][i].build(j, i)

    def change_to_menu(self, value):
        self.reinitialize()
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_menu_win(self):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_win(self):
        self.win_popup.open()

    def change_to_gamemode(self):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_lose1(self):
        self.lose1_popup.open()

    def change_to_lose2(self):
        self.lose2_popup.open()


class Hard(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.width = 24
        self.height = 24
        self.mines = 99
        self.win_popup = Win(self)
        self.lose1_popup = Lose1(self)
        self.lose2_popup = Lose2(self)
        self.init()

    def init(self):
        self.root_layout = BoxLayout(orientation="vertical")
        self.layout = GridLayout(cols=24, rows=24)
        self.bottom_bar = BoxLayout(orientation="horizontal", size_hint_y=0.125)
        self.change_to_menu_button = Button(text="Give up this game, back to menu", font_size=24,
                                            background_color=[228 / 255, 201 / 255, 27 / 255, 1],
                                            on_press=self.change_to_menu)
        self.field = []
        self.init_grid()

        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.root_layout.add_widget(self.layout)

        self.bottom_bar.add_widget(self.change_to_menu_button)
        self.root_layout.add_widget(self.bottom_bar)

        self.add_widget(self.root_layout)

    def reinitialize(self):
        self.clear_widgets()
        Global.first = True
        Global.flagged = 0
        Global.effFlag = 0
        Global.current = ""
        self.init()

    def init_grid(self):
        for j in range(24):
            new = []
            for i in range(24):
                new.append(Grid(self))
            self.field.append(new)

        mineCount = 0
        while mineCount < self.mines:
            j = randint(0, 23)
            i = randint(0, 23)
            if self.field[j][i].isMine == 0:
                self.field[j][i].isMine = 1
                mineCount += 1

        for i in range(24):
            for j in range(24):
                self.field[j][i].build(j, i)

    def change_to_menu(self, value):
        self.reinitialize()
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_menu_win(self):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

    def change_to_win(self):
        self.win_popup.open()

    def change_to_gamemode(self):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_lose1(self):
        self.lose1_popup.open()

    def change_to_lose2(self):
        self.lose2_popup.open()


class Win(Popup):
    def __init__(self, diffi, **kwargs):
        Popup.__init__(self, **kwargs)
        self.title = "Congratulations! You win!"
        self.init(diffi)

    def init(self, diffi):
        self.layout = GridLayout(cols=1)
        self.win_label = Label(text="Congratulations! You win!", font_size=48, color=[213/255, 116/255, 42/255, 1])
        self.score_button = Button(text="Click to continue", font_size=36, on_press=self.score)
        self.hi_noNewScore = Label(text="Play again?", font_size=48, color=[213 / 255, 116 / 255, 42 / 255, 1])
        self.exit_button = Button(text="exit game", font_size=36, on_press=self.exit_game)

        self.scoreAchieved = 0
        self.diffi = diffi
        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)
        self.add_widget(self.layout)

    def score(self, value):
        self.layout.remove_widget(self.win_label)
        self.layout.remove_widget(self.score_button)
        scoreAchieved = 5000/(Global.end-Global.start)
        self.scoreAchieved = scoreAchieved
        string = "Your score is " + str(self.scoreAchieved) + " !"
        self.score_label = Label(text=string,font_size=24, color=[213/255, 116/255, 42/255, 1])

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
                    name = "[SYSTEM]: INPUT WAS EMPTY"
                if first:
                    if mode == Global.current:
                        highest = [name, mode, score]
                        first = False
                    else:
                        pass
                if score > highest[-1] and mode == highest[-2]:
                    highest = [name, mode, score]

        if scoreAchieved > highest[-1] and Global.current == highest[-2]:
            newHighScore = True

        if newHighScore == True:
            self.hi_label = Label(text="You have reached a new high score in this difficulty!\n"
                                       "Would you like to put your name onto the scoreboard?",  font_size=24, color=[213/255, 116/255, 42/255, 1])
            self.yes_button = Button(text="Yes!", font_size=36, on_press=self.yes)
            self.no_button = Button(text="Nah...", font_size=36, on_press=self.no)

            self.layout.add_widget(self.score_label)
            self.layout.add_widget(self.hi_label)
            self.layout.add_widget(self.yes_button)
            self.layout.add_widget(self.no_button)
            self.layout.add_widget(self.exit_button)
        else:
            self.anotherGame_button = Button(text="Yes! Another game!", font_size=36, on_press=self.anotherGame)
            self.menu_button = Button(text="Nah...Back to menu", font_size=36, on_press=self.change_to_menu)

            self.layout.add_widget(self.score_label)
            self.layout.add_widget(self.hi_noNewScore)
            self.layout.add_widget(self.anotherGame_button)
            self.layout.add_widget(self.menu_button)
            self.layout.add_widget(self.exit_button)

    def yes(self, value):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_label)
        self.layout.remove_widget(self.yes_button)
        self.layout.remove_widget(self.no_button)
        self.layout.remove_widget(self.exit_button)

        self.name_label = Label(text="Your name:", font_size=24, color=[213/255, 116/255, 42/255, 1])
        self.name_input = TextInput()
        self.yes_anotherGame_button = Button(text="another game", font_size=36, on_press=self.yes_anotherGame)
        self.record_exit_button = Button(text="exit game", font_size=36, on_press=self.record_exit_game)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.yes_anotherGame_button)
        self.layout.add_widget(self.record_exit_button)

    def no(self, value):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_label)
        self.layout.remove_widget(self.yes_button)
        self.layout.remove_widget(self.no_button)
        self.layout.remove_widget(self.exit_button)

        self.no_anotherGame_button = Button(text="another game", font_size=36, on_press=self.no_anotherGame)
        self.layout.add_widget(self.hi_noNewScore)
        self.layout.add_widget(self.no_anotherGame_button)
        self.layout.add_widget(self.exit_button)


    def anotherGame(self, value):
        self.layout.remove_widget(self.score_label)
        self.layout.remove_widget(self.hi_noNewScore)
        self.layout.remove_widget(self.anotherGame_button)
        self.layout.remove_widget(self.menu_button)
        self.layout.remove_widget(self.exit_button)

        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)

        self.diffi.reinitialize()
        self.diffi.change_to_menu_win()
        self.dismiss()

    def yes_anotherGame(self, value):
        self.layout.remove_widget(self.name_label)
        self.layout.remove_widget(self.name_input)
        self.layout.remove_widget(self.yes_anotherGame_button)
        self.layout.remove_widget(self.record_exit_button)

        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)

        self.record_highscore()
        self.diffi.reinitialize()
        self.diffi.change_to_gamemode()
        self.dismiss()

    def no_anotherGame(self, value):
        self.layout.remove_widget(self.hi_noNewScore)
        self.layout.remove_widget(self.no_anotherGame_button)
        self.layout.remove_widget(self.exit_button)

        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.score_button)

        self.diffi.reinitialize()
        self.diffi.change_to_gamemode()
        self.dismiss()

    def change_to_menu(self, value):
        self.diffi.manager.transition.direction = "up"
        self.diffi.manager.current = "menu"
        self.diffi.reinitialize()
        self.dismiss()

    def record_highscore(self):
        with open("scores_local.txt", "a") as file:
            string = "\n" + str(self.name_input.text) + " " + str(Global.current) + " " + str(self.scoreAchieved)
            file.write(string)

    def record_exit_game(self, value):
        self.record_highscore()
        App.get_running_app().stop()
        Window.close()

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()

class Lose1(Popup):
    def __init__(self, diffi, **kwargs):
        Popup.__init__(self, **kwargs)
        self.title = "Awww, wish you have better luck next time..."
        self.init(diffi)

    def init(self, diffi):
        self.layout = GridLayout(cols=1)
        self.diffi = diffi
        self.lose_label1 = Label(text="You clicked on a mine... :(", font_size=24, color=[213/255, 116/255, 42/255, 1])
        self.lose_label2 = Label(text="Good luck next time!", font_size=24, color=[213/255, 116/255, 42/255, 1])
        self.anotherGame_button = Button(text="another game", font_size=36, on_press=self.anotherGame)
        self.exit_button = Button(text="exit game", font_size=36, on_press=self.exit_game)

        self.layout.add_widget(self.lose_label1)
        self.layout.add_widget(self.lose_label2)
        self.layout.add_widget(self.anotherGame_button)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def anotherGame(self, value):
        self.diffi.reinitialize()
        self.diffi.change_to_gamemode()
        self.dismiss()

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()

class Lose2(Popup):
    def __init__(self, diffi, **kwargs):
        Popup.__init__(self, **kwargs)
        self.title = "Awww, wish you have better luck next time..."
        self.init(diffi)

    def init(self, diffi):
        self.layout = GridLayout(cols=1)
        self.diffi = diffi
        self.lose_label1 = Label(text="You misflagged a safe grid, and you didn't find out in the end... :(",
                                 font_size=24, color=[213/255, 116/255, 42/255, 1])
        self.lose_label2 = Label(text="Good luck next time!", font_size=24, color=[213/255, 116/255, 42/255, 1])
        self.anotherGame_button = Button(text="another game", font_size=36, on_press=self.anotherGame)
        self.exit_button = Button(text="exit game", font_size=36, on_press=self.exit_game)

        self.layout.add_widget(self.lose_label1)
        self.layout.add_widget(self.lose_label2)
        self.layout.add_widget(self.anotherGame_button)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def anotherGame(self, value):
        self.diffi.reinitialize()
        self.diffi.change_to_gamemode()
        self.dismiss()

    def exit_game(self, value):
        App.get_running_app().stop()
        Window.close()


if __name__ == '__main__':
    MineSweep().run()

