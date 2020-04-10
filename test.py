from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class CreateButton(Button):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "right":
                print(self.id, "right mouse clicked")
            elif touch.button == "left":
                print(self.id, "left mouse clicked")
            else:
                print(self.id)
            return True
        return super(CreateButton, self).on_touch_down(touch)


class OnTouchDownDemo(GridLayout):

    def __init__(self, **kwargs):
        super(OnTouchDownDemo, self).__init__(**kwargs)
        self.build_board()

    def build_board(self):
        # make 9 buttons in a grid
        for i in range(0, 9):
            button = CreateButton(id=str(i))
            self.add_widget(button)


class OnTouchDownApp(App):

    def build(self):
        return OnTouchDownDemo()


if __name__ == '__main__':
    OnTouchDownApp().run()