from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.label import Label
from kivy.interactive import InteractiveLauncher
from kivy.uix.textinput import TextInput #name for scoreboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
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


class Grid():
    def __init__(self):
        self.isMine = 0
        # self.isVisible = False
        self.neighbors = 0
        self.location = None
        self.button = Button(size=(gridSize, gridSize))
        # size is the global variable defined at the beginning of each gamemode
        self.button.bind(on_touch_down=self.onPressed)


    def onPressed(self, instance, touch):
        if touch.button == "left":
            print("left click")
        elif touch.button == "right":
            print("right click")
            # self.color = (225,225,126,1)
            # difference between background color and color attr
            # why it fixed the white at top right color bug
'''
class MyButton(Button,EventDispatcher):
    isMine = NumericProperty(0)
    def __init__(self, **kwargs):
        Button.__init__(self,**kwargs)
        #self.isMine = 0
        self.bind(on_touch_down=self.onPressed)

    def onPressed(self, instance, touch):
        if touch.button == "left":
            print("left click")
        elif touch.button == "right":
            print("right click")
            self.color = (225,225,126,1)
            # difference between background color and color attr
            # why it fixed the white at top right color bug
'''
    

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


class Easy(Screen,FloatLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        FloatLayout.__init__(self, **kwargs)
        
        self.layout = FloatLayout(size=(300, 300))
        coordinates = {}
        mines = 10
        mineTotal = 0
        
        # TODO
        # position and sizes to be modified to create a better UI
        for x in range(10):
            for y in range(10):
                ifMine = randint(0,1)
                if ifMine and mineTotal < mines:
                    self.btn = MyButton(isMine=1,size_hint=(10/300,10/300),pos=(100+x*30,100+y*30))
                    self.layout.add_widget(self.btn)
                    mineTotal += 1
                    coordinates[(x*30,y*30)] = 1
                else:
                    self.btn = MyButton(isMine=0,size_hint=(10/300,10/300),pos=(100+x*30,100+y*30))
                    self.layout.add_widget(self.btn)
                    coordinates[(x*30,y*30)] = 0
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

    
