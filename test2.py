class classA():
    # a class my code is at when the error arises,
    # which is not the starting "current" screen class
    # but a different class that serves a certain purpose to my program
    def __init__(self, **kwargs):
        ...
        ...
        ScreenA().change_to_B()
        ##### This is the line that gives the error message #####

    ...


...


class ScreenA(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        ...
        ...

    def change_to_B(self):
        self.manager.transition.direction = "left"
        self.manager.current = "screenB"


...


class ScreenB(Screen):
    ...


if __name__ == '__main__':
    Main().run()