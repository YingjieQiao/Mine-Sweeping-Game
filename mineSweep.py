from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.label import Label
from kivy.interactive import InteractiveLauncher
from kivy.uix.textinput import TextInput #name for scoreboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window 
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from random import randint


##TODO: position and size
##understand layouts


def init_grid(width, height, mines):
    global grid_field
    # Initiate the gird field with empty grids
    grid_field = [[Grid() for i in range(width)] for j in range(height)]
    ## (maybe) TODO
    ## incorporate other O(N) things here!!!!!!!!!!


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
        i = randint(0, height-1)
        j = randint(0, width-1)
        if grid_field[j][i].isMine == 0:
            grid_field[j][i].isMine = 1
            mineCount += 1

    # fill mines into the grid field
    for i in range(width):
        for j in range(height):
            grid_field[j][i].build(j, i)


def reveal_zeros(gridObj):
    # gridObj is already confirmed to be 0 -- no mines in its surrounding
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (0 <= gridObj.location[0] + i < width) and (0 <= gridObj.location[1] + j < height):
                check = grid_field[gridObj.location[0] + i][gridObj.location[1] + j]
                if check.isClicked == 0 and check.neighbors == 0:
                    check.button.text = str(check.neighbors)
                    check.isClicked = 1
                    if check not in neighbor_grids:
                        neighbor_grids.append(check)
                    #neighbor_grids.remove(gridObj)
                    # why this one gives ValueError: list.remove(x): x not in list???

class Grid():
    def __init__(self):
        self.isMine = 0
        self.isClicked = 0
        self.isFlagged = 0
        self.neighbors = 0
        self.location = [] # (height_index, width_index)
        self.button = Button(size=(gridSize, gridSize))
        # gridSize is the global variable defined at the beginning of each gamemode
        self.button.bind(on_touch_down=self.onPressed)

    def build(self, x, y):
        self.location = [x, y]
        self.count_neighbors()

    def onPressed(self, instance, touch):
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
                            reveal_zeros(neighbor_grids[0])
                            neighbor_grids.remove(neighbor_grids[0])

                    else:
                        self.button.text = str(self.neighbors)
                else:
                    self.button.text = "!"
            elif touch.button == "right":
                if self.isFlagged == 0:
                    self.isFlagged = 1
                    self.button.text = "*"
                    # color change
                elif self.isFlagged == 1:
                    self.isFlagged = 0
                    self.button.text = " "
                    # color change
                # self.color = (225,225,126,1)
                # difference between background color and color attr
                # why it fixed the white at top right color bug




    def count_neighbors(self):
        if self.isMine == 0:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (0 <= self.location[0] + i < width) and (0 <= self.location[1] + j < height):
                        if grid_field[self.location[0] + i][self.location[1] + j].isMine == 1:
                            count += 1
            self.neighbors = count



class MineSweep(App):
    def build(self):
        scrm = ScreenManager()
        
        menu = Menu(name="menu")
        options = Options(name="options")
        gamemode = GameMode(name="gamemode")
        easy = Easy(name="easy")
        medium = Medium(name="medium")
        hard = Hard(name="hard")
        customize = Customize(name="customize")
        
        scrm.add_widget(menu)
        scrm.add_widget(options)
        scrm.add_widget(gamemode)
        scrm.add_widget(easy)
        scrm.add_widget(medium)
        scrm.add_widget(hard)
        scrm.add_widget(customize)
        scrm.current = "menu"
        return scrm

    

class Menu(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
        
        self.layout = GridLayout(cols=1)
        self.start_button = Button(text="Start Game", on_press=self.change_to_gamemode)
        self.options_button = Button(text="Options", on_press=self.change_to_options)
        self.quit_button = Button(text="Quit", on_press=self.quit_app)
        
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.options_button)
        self.layout.add_widget(self.quit_button)
        
        self.add_widget(self.layout)
        
    def change_to_gamemode(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "gamemode"

    def change_to_options(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "options"

    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()

class Options(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
                
        self.layout = GridLayout(cols=1)
        self.options_label = Label(text="Options")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)
        
        self.layout.add_widget(self.options_label)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def change_to_menu(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"
        
class GameMode(Screen,GridLayout):
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
        self.manager.transition.direction = "down"
        self.manager.current = "easy"
        
    def change_to_medium(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "medium"
        
    def change_to_hard(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "hard"
        
    def change_to_customize(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "customize"

class Easy(Screen, GridLayout):
    # init_grid(width, height, mines)
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

        self.layout = GridLayout(cols=10, rows=10)

        global width, height, mines, gridSize
        width = 10
        height = 10
        mines = 10 # to few mines will result in exceeding of maximum recursion !!!!!!!!!!!!
        gridSize = 60
        init_grid(width, height, mines)

        # TODO
        # position and sizes to be modified to create a better UI
        for eachRow in grid_field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

class Medium(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)


class Hard(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
     
        
class Customize(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)

if __name__ =='__main__':
    MineSweep().run()

    
