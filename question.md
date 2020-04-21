I've been trying to write a minesweeper game in python with kivy for the GUI. 
I have already got the gaming mechanism working yet I don't know how to implement a **"reset game" / "restart game"** function. 
*I think my problem lies in either creating of the ```Screen``` objects or removing the ```Gird()``` objects.*

The framework of my game is as follows:


I created multiple screens in the game and I have simplified it to show the main structure here. 
The ```menu``` screen is the initial screen when the code is run, 
the ```Easy()``` screen is the game board for the minesweeper game I am working on, 
and the ```Gameover()``` screen is where I am trying to trigger the **"reset game" / "restart game"** function. 
 

I created a ```Grid()``` class with attribute ```Button``` from kivy. 
The ```Grid()``` class is where the majority gaming functions are implemented, 
and the realvent part, which is switiching to ```Gameover``` screen when the win/lose condition is met, 
is shown below.


The ```init_field()``` is a global function to create a nested 2D list to represent a matrix of the minefield, 
which is convenient to implement other gaming functions 
such as "counting number of mines around a certain square", etc. 

The ```build_field``` function, which can be found in the ```Esay()``` class, is used to construct certain attributes of reach ```Grid()``` object stored in the 2D list 
and it is not relavent in implementing the **"reset game" / "restart game"** function, in my opinion.



```
def init_grid(width, height, mines, difficulty):
    grid_field = [[Grid(difficulty) for i in range(width)] for j in range(height)]
    ...
    ...
    return grid_field

class Grid():
    def __init__(self, difficulty, **kwargs):
        self.isMine = 0
        self.isClicked = 0
        ...
        self.button = Button(size=(Global.gridSize, Global.gridSize))
        self.button.bind(on_touch_down=self.onPressed)
        ...

    def onPressed(self, instance, touch):
        if self.button.collide_point(*touch.pos):
        ...
        elif touch.button == "right":
            if Global.flagged == self.difficulty.mines:
                self.difficulty.change_to_gameover()
            
        

class Main(App):
    def build(self):
        sm = ScreenManager()

        ...
        menu = Menu(name="menu)
        easy = Easy(name="easy")
        gameover = Gameover(name="gameover)

        sm.add_widget(menu)
        sm.add_widget(easy)
        sm.add_widget(name="gameover")
        ...

        sm.current = "menu"
        return sm

class Easy(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
        self.width = 10
        self.height = 10
        self.mines = 10
        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)

        for eachRow in self.field:
            for each in eachRow:
                self.layout.add_widget(each.button)
        self.add_widget(self.layout)

    def reinitialize(self):
        print("reinitalizing...")
        self.remove_widget(self.layout)

        self.layout = GridLayout(cols=self.height, rows=self.width)
        self.field = init_grid(self.width, self.height, self.mines, self)
        self.field = build_field(self.field, self.width, self.height)

        for eachRow in self.field:
            for eachGrid in eachRow:
                self.layout.add_widget(eachGrid.button)
        self.add_widget(self.layout)

    def change_to_win(self):
        self.manager.transition.direction = "up"
        self.manager.current = "win"


        
```

I was trying to implement **"reset game" / "restart game"** in the ```Gameover()``` screen, 
and I tried calling the ```reinitialize()``` function I defined in the game board ```Easy()``` screen earlier:

```
class Gameover(Screen, GridLayout):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        GridLayout.__init__(self, **kwargs)
        ...
        self.yes_anotherGame_button = Button(text="another game", on_press=self.yes_anotherGame)
        self.layout.add_widget(self.yes_anotherGame_button)

    def yes_anotherGame(self, value):
        Easy().reinitialize()
```

But it turns out that this function doesn't as expected. 
I've added the print line when I was debugging and the ```reinitlaize()``` function was executed, 
but when I switch to the ```Easy()``` screen again, 
it is still the old layout. 
As in, it is still the minefield of last game with the marking from the last game remaining there, 
which shouldn't be the case as the 2D list containing the ```Grid()``` objects are re-initialized by calling ```init_grid()``` again
and the old ```GridLayouit()``` should have been removed by ```self.remove_widget(self.layout)```.
I have also tried using ```self.clear_widget()``` and this is not removing the old layout either.
