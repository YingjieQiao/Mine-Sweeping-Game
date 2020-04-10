import random

class Minesweeper:

    def __init__(self,width=9,height=10,mine_numbers=12):
        # Table generate: change via tables_ize()
        self.width = width
        self.height = height
        self.mine_numbers = mine_numbers
        self.table = [None]*self.width*self.height
        # User cell input
        self.user_cell = False
        self.user_row = False
        self.user_column = False
        self.user_reveal = []
        '''
        {user_reveal} is changed by
        - {game_create()}: reset user_reveal
        - {user_input()}: append input cell, cannot reveal all adjacent 0 here (first turn - table not yet generated)
        - {adjacent_zero()}: reveal all adjacent 0
        - {end_game()}: append all mines
        '''
        '''
        {*_user_*},{user_cell} = {[column][row]}, index is 1 more than {*_cell_*} index
        {*_cell_*} = {[row][column]}, index is 1 less than {*_user_*} index
        '''


    def game_create(self):
        print(f'Default size is {self.width}*{self.height}, {self.mine_numbers} mines')
        default_size = input('Play default size?(Y/N): ')
        if default_size.lower() == 'n':
            correct_input = False
            while not correct_input:
                try:
                    self.width = int(input('Enter width: '))
                    self.height = int(input('Enter height: '))
                    self.mine_numbers = int(input('Enter number of mines: '))
                    if self.mine_numbers >= self.width*self.height or self.mine_numbers == 0:
                        print('ERROR: Number of mines can not be 0 or equal/exceed table size')
                    elif self.width > 99 or self.height > 99:
                        print('ERROR: Maximum table size is 99*99')
                    else:
                        self.table = [None]*self.width*self.height
                        self.user_reveal = []
                        correct_input = True
                        return self.width,self.height,self.mine_numbers,self.table,self.user_reveal
                except ValueError:
                    print('ERROR: Try again, number only')
        else:
            self.table = [None]*self.width*self.height
            self.user_reveal = []
            return self.width,self.height,self.mine_numbers,self.table,self.user_reveal


    def user_input(self):
        correct_input = False
        while not correct_input:
            try:
                self.user_cell = input('Enter {[column][row]} in 4 digits eg. 0105: ')
                int(self.user_cell)
                if len(self.user_cell) != 4:
                    print('ERROR: Only 4 digits allowed')
                elif int(self.user_cell[2:]) > self.height or self.user_cell[2:] == '00':
                    print('ERROR: Row out of range')
                elif int(self.user_cell[:2]) > self.width or self.user_cell[:2] == '00':
                    print('ERROR: Column of range')
                elif self.user_cell in self.user_reveal:
                    print('ERROR: Already revealed')
                else:
                    correct_input = True
            except ValueError:
                print('ERROR: Try again, number only')

        self.user_row = int(self.user_cell[2:])
        self.user_column = int(self.user_cell[:2])
        if self.user_cell:
            self.user_reveal.append(self.user_cell)
        return self.user_cell,self.user_row,self.user_column


    def mines_generator(self):
        # Exclude first cell from mines generator
        user_location = ((self.user_row-1)*self.width)+self.user_column-1
        possible_location = [i for i in range(self.width*self.height) if i != user_location]
        mines_location = random.sample(possible_location,self.mine_numbers)

        # Assign 'Location with mine' with 9
        for i in mines_location:
            self.table[i] = 9
        return self.table


    def two_dimension_array(self):
        # Save table into 2D array
        for i in range(self.height):
            self.table[i] = self.table[0+(self.width*i):self.width+(self.width*i)]

        # Remove unnessessary elements
        del self.table[self.height:]
        return self.table


    def complete_table(self):
        # Create temporary 2D array
        temporary_table = [[None for _ in range(self.width)] for _ in range(self.height)]
        # For every table[i][j]
        for i in range(self.height):
            for j in range(self.width):
                # If table[i][j] is bomb, continue
                if self.table[i][j] == 9:
                    temporary_table[i][j] = 9
                    continue
                else:
                    counter = 0
                    # For every adjacent neighbor arrays
                    for k in range(i-1,i+2):
                        # Error handling: list index out of range
                        if 0 <= k <= self.height-1:
                            for l in range(j-1,j+2):
                                # Error handling: list index out of range
                                if 0 <= l <= self.width-1:
                                    # Count every adjacent mines
                                    if self.table[k][l] == 9:
                                        counter += 1
                                        continue
                    temporary_table[i][j] = counter
        self.table = temporary_table
        return self.table


    def adjacent_zero(self,zero_cell):
        # If value is 0
        if self.table[int(zero_cell[2:])-1][int(zero_cell[:2])-1] == 0:
            # For all neighbor elements
            for i in range(int(zero_cell[2:])-1-1,int(zero_cell[2:])-1+2):
                # Error handling: index out of range
                if 0 <= i < self.height:
                    for j in range(int(zero_cell[:2])-1-1,int(zero_cell[:2])-1+2):
                        if 0 <= j < self.width:
                            # If neighbor element of 0 is not yet append, append all adjacent element
                            if str(j+1).zfill(2)+str(i+1).zfill(2) not in self.user_reveal:
                                self.user_reveal.append(str(j+1).zfill(2)+str(i+1).zfill(2))
                                # If neighbor is also 0, do a recursion
                                if self.table[i][j] == 0:
                                    self.adjacent_zero(str(j+1).zfill(2)+str(i+1).zfill(2))


    def first_turn(self):
        self.user_input()
        self.mines_generator()
        self.two_dimension_array()
        self.complete_table()
        self.adjacent_zero()


    def print_table(self):
        # Clear UI
        print('\n'*10)
        for row in range(self.height+1):
            cell = '|'
            for column in range(self.width+1):
                # Top-row label
                if row == 0:
                    cell += f'{column:2}|' # (Note: try 02 instead of 2)
                    continue
                # First column label
                elif column == 0:
                    cell += f'{row:2}|'
                    continue
                # Revealed cell
                elif str(column).zfill(2)+str(row).zfill(2) in self.user_reveal:
                    cell += f'{self.table[row-1][column-1]:2}|'
                    continue
                # Not yet revealed cell
                else:
                    cell += '{:>3}'.format('|')
            print(cell)


    def end_game(self):

        # If end: reveal all mines, nested function
        def reveal_mine():
            for i,j in enumerate(self.table):
                for k,l in enumerate(j):
                    if l == 9:
                        self.table[i][k] = ‘XX’
                        if str(k+1).zfill(2)+str(i+1).zfill(2) not in self.user_reveal:
                            self.table[i][k] = ‘**’
                            self.user_reveal.append(str(k+1).zfill(2)+str(i+1).zfill(2))

        # If user choose cell: check if end
        if self.user_cell:
            if self.table[self.user_row-1][self.user_column-1] == 9:
                end_game = True
                reveal_mine()
                self.print_table()
                print('YOU LOSE!')
            elif len(self.user_reveal) == (self.width*self.height)-self.mine_numbers:
                end_game = True
                reveal_mine()
                self.print_table()
                print('YOU WIN!')
            else:
                end_game = False
        # If no cell selected: end = False
        else:
            end_game = False

        return end_game


    def restart_game(self):
        restart = input('Restart?(Y/N): ')
        if restart.lower() == 'y':
            return True
        else:
            return False


def main():

    minesweeper = Minesweeper()

    while True:
        minesweeper.game_create()
        minesweeper.print_table()
        minesweeper.first_turn()

        while not minesweeper.end_game():
            minesweeper.print_table()
            minesweeper.user_input()
            minesweeper.adjacent_zero(minesweeper.user_cell)

        if not minesweeper.restart_game():
            break


if __name__ == '__main__':
    main()