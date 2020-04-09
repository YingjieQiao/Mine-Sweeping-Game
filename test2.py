import kivy
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from random import randint
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout

width = 10
height = 10
bombs = 5
size = 60

class Cell():

  def __init__(self):
    self.isBomb = False
    self.isVisible = False
    self.neighbors = None
    self.location = []
    self.button = Button(size = (size, size), size_hint = (None, None))
    self.button.bind(on_touch_down = self.onPressed)

  def build(self, x, y):
    self.location = [x, y]
    self.count_neighbors()

  def onPressed(self, instance, touch):
    if touch.button == 'left':
        self.isVisible = True
        self.button.text = str(self.neighbors)
        if self.neighbors == 0:
          for i in range(-1, 2):
            for j in range(-1, 2):
              if (0 <= self.location[0] + i < width) and (0 <= self.location[1] + j < height):
                if grid[self.location[0] + i][self.location[1] + j].isVisible == False:
                  grid[self.location[0] + i][self.location[1] + j].onPressed(instance, touch)
    #if right_click == True:
      #Toggle state


  def count_neighbors(self):
    if self.isBomb == False:
      count = 0
      for i in range(-1, 2):
        for j in range(-1, 2):
          if (0 <= self.location[0] + i < width) and (0 <= self.location[1] + j < height):
            if grid[self.location[0] + i][self.location[1] + j].isBomb == True:
              count += 1
      self.neighbors = count

class TestApp(App):

  def build(self):
    root = AnchorLayout(anchor_x = 'center', anchor_y = 'center')
    grid_root = RelativeLayout(size = (width * size, height * size), size_hint = (None, None))
    layout = []
    for i in range(height):
      layout.append(BoxLayout(orientation='horizontal', size_hint = (.8, .8), pos = (0, (height - 1) * size - i * size)))
      for j in range(width):
        layout[i].add_widget(grid[j][i].button)
      grid_root.add_widget(layout[i])
    root.add_widget(grid_root)
    return root


def init_grid():
  global grid
  grid = [[Cell() for x in range(width)] for y in range(height)]

  for _ in range(bombs):
    while True:
      x = randint(0, height - 1)
      y = randint(0, width - 1)
      if grid[x][y].isBomb == False:
        grid[x][y].isBomb = True
        break
  for i in range(width):
    for j in range(height):
      grid[j][i].build(j, i)


if __name__ == '__main__':
  init_grid()
  TestApp().run()