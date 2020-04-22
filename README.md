# Mine-Sweeping-Game


ok i know kinda want to do a shooting range one


3D minesweep? --- after I finish 2D version.


### TODO

Framework done. To polish up after everything (this is important. you dont want the prof say you just copy starter code for your UI)

"Easy" expansion algo done. Do for "Medium" and "Hard" first. Do "Customize" last.

smaller gird board to give space for 1) timer 2) the happy smiling face?? 3) number of mines left

quit to menu in the middle

**Work out scoring system and scoreborad with local file saved and "one more game machanism**

figure out how to incorporate sm class into it (very important, bonus mark)

create a method class contain all the `change to xxx` functions, etc (don't repeat code) (try to do it)

# Important

### Compile three difficulty level into one. Writing 3 individually is not impressive enough

### Note

1. You shouldn't use one `grid_field` global variable to store all the grids, because you excecute `init_grid` three times,
all of which give the result list to `grid_field`, so in the end, only the last list (the one for hard mode) is stored 
and thus there is no reaction when you click on the UI of easy or medium. 

2. `prototype2.py` is the current working version. `prototype1.py` is for compling game screen experiment: Can I create a new `Screen` widget in the middle of the code? `prototype3.py` is experimenting resetting the game.

3. or maybe I can make the whole thing into a state machine. input is "easy", "medium", "hard". But I still need to figure out how to add in screen in the middle

4. you can make the menu page a state machine

5. redo the data reading part. the first `highest` value

6. about the 10/18/24 instead of self.data thing: I started off using these two, even thought the 2 attrs are
untouched, as in un mdified, but in the easy mode, which I expeirments, they are changed to 800.....

### ref

adding new attr: https://subscription.packtpub.com/book/application_development/9781783987382/1/ch01lvl1sec12/declaring-properties-within-a-class 

clicking problem that takes me 2 days: https://stackoverflow.com/questions/45934429/bind-a-function-to-multiple-dynamically-created-buttons-in-kivy

screen switch by calling it outside the class: https://stackoverflow.com/questions/61211225/switching-screens-using-kivy-attributeerror-nonetype-object-has-no-attribute/61213984?noredirect=1#comment108308582_61213984

https://stackoverflow.com/questions/61356660/how-to-reinitialize-a-screen-in-kivy-with-python

(thanks to open source community omg)

(when u run into a problem, GOOGLE first)
