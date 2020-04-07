import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.interactive import InteractiveLauncher
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window 

##TODO: position and size
##understand layouts


class MineSweep(App):
    def build(self):
        sm = ScreenManager()
        menu = Menu(name="menu")
        options = Options(name="options")
        game = Game(name="game")
        sm.add_widget(menu)
        sm.add_widget(options)
        sm.add_widget(game)
        sm.current = "menu"
        return sm
    
class Menu(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
        
        self.layout = GridLayout(cols=1)
        self.start_button = Button(text="Start Game", on_press=self.start_game)
        self.options_button = Button(text="Options", on_press=self.change_to_options)
        self.quit_button = Button(text="Quit", on_press=self.quit_app)
        
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.options_button)
        self.layout.add_widget(self.quit_button)
        
        self.add_widget(self.layout)
        
    def start_game(self, value):
        self.manager.transition.direction = "up"
        self.manager.current = "game"
        
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
        
class Game(Screen,GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
                
        self.layout = GridLayout(cols=1)
        ## TODO
        self.game_label = Label(text="Game")
        self.menu_button = Button(text="Back to Menu", on_press=self.change_to_menu)
        self.layout.add_widget(self.game_label)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)
        
    def change_to_menu(self, value):
        self.manager.transition.direction = "down"
        self.manager.current = "menu"

if __name__ =='__main__':
    MineSweep().run()

    
    
    