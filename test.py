# test.py
from kivy.app import App
from kivy.interactive import InteractiveLauncher
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config

Red = [1, 0, 0, 1]
Normal = [1, 1, 1, 1]
Blue = [0, 0, 1, 1]
class TestApp(App):
    def build (self):
        return Gui()
class MyButton (Button):
    def __init__(self):
        super(MyButton, self).__init__()
    def on_touch_down(self, touch):
        if touch.button == 'left':
            if self.background_color == Red:
                self.background_color = Normal
            else:
                self.background_color = Red
        elif touch.button == 'right':
            if self.background_color == Blue:
                self.background_color = Normal
            else:
                self.background_color = Blue
class Gui(BoxLayout):
    grid = ObjectProperty(None)
    def __init__(self, ** kwargs):
        super ().__init__(** kwargs)
        for i in range(5):
            for j in range(5):
                self.grid.add_widget(MyButton())
if __name__ == '__main__':
    #Config.set('input', 'mouse', 'mouse, disable_multitouch')
    Window.size = (1500, 1000)
    TestApp().Run()