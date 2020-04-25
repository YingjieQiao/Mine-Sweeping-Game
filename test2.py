import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.interactive import InteractiveLauncher


class AlternateApp(App):

    def build(self):
        self.label = Label(text="Programming is fun", font_size=48)

        return self.label



myapp = AlternateApp()
myapp.run()
