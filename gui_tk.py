from tkinter import *
import random
import time
import game

WIDTH, HEIGHT = 400, 400
SCL = 100  # how much moved
offset = 200  # space for menus etc

num2color = {2: '#DECCDC', 4: '#D6C0D4', 8: '#C6A7C3',
             16: '#B68EB2', 32: '#A675A1', 64: '#976B93',
             128: '#795676', 256: '#5B4058', 512: '#3D2B3B',
             1024: '#2E202C', 2048: '#25283D'}  # from lightest to darkest


class Board:
    score = 0

    def __init__(self, root):
        """Creates the intial canvas and board elements"""
        self.root = root
        self.canvas = Canvas(root, width=WIDTH, height=(
            HEIGHT + offset), bg='#E9EBED', relief=FLAT)
        self.canvas.pack()
        Board.tiles = {}
        Board.filled = []

        self.init_tiles()
        self.init_binds()
        self.init_labels()

    def init_tiles(self):
        """Creates and places 16 tiles, binding them to their indices, which
            act as keys for the Board.tiles dictionary
        """
        for row in range(4):
            for col in range(4):
                Board.tiles[(row, col)] = None
            # create the grid to play on
            self.canvas.create_line(row*SCL, offset,
                                    row*SCL, (400 + offset), fill='white', width=2)
            self.canvas.create_line(0, (row*SCL + offset),
                                    400, (row*SCL + offset), fill='white', width=2)

    def init_binds(self):
        """Assigns game functions to keyboard presses"""
        self.canvas.focus_set()
        self.canvas.bind('<Left>', game.create_dir('L', self))
        self.canvas.bind('<Right>', game.create_dir('R', self))
        self.canvas.bind('<Up>', game.create_dir('U', self))
        self.canvas.bind('<Down>', game.create_dir('D', self))

    def init_labels(self):
        """Creates the game title and scoring system"""
        Label(self.canvas, text='2 0 4 8', font=('Helvetica', '50'),
              fg='#A675A1', bg='#E9EBED').place(x=100, y=25)
        Board.score_board = Label(self.canvas, text=f'SCORE:{Board.score}',
                                  font=('Helvetica', '15'), fg='white', bg='#C6A7C3')
        Board.score_board.place(x=140, y=130)
        Board.againbtn = Button(self.canvas, text="P L A Y  A G A I N", command=self.play_again,
                                font=('Helvetica Bold', '30'), bd=0, fg='white', bg='#795676', relief=FLAT)

    def computer(self):
        """Gives computer player the controls"""  # allows computer to play, but doesn't update on the screen
        directions = {1: game.create_dir('L', self),
                      2: game.create_dir('R', self),
                      3: game.create_dir('U', self),
                      4: game.create_dir('D', self)}
        return directions

    def start_game(self):
        """Initiates the start of the board with 2 random tiles filled"""
        places = list(Board.tiles.keys())
        r1 = random.choice(places)
        places.remove(r1)
        r2 = random.choice(places)
        self.create_tile(r1)
        self.create_tile(r2)

        self.change_tile_appearance(r1, 2)
        self.change_tile_appearance(r2, 2)

    ######################
    # tile modifications #
    ######################

    def create_tile(self, key):
        """Creates a tile and places to the board, adding its key to the filled list"""
        Board.tiles[key] = Label(self.canvas, height=100,
                                 width=100, fg='white',
                                 bd=0, relief=FLAT, font=('Helvetica', '30'))
        Board.tiles[key].place(height=98, width=98,
                               x=(2 + 100 * key[1]), y=(100 * key[0] + 200))
        if key not in Board.filled:
            Board.filled.append(key)

    def remove_tile(self, key):
        """Removes the tile from the board and removes its key from the filled list"""
        if key in Board.filled:
            Board.filled.remove(key)
        Board.tiles[key].place_forget()

    def merge(self, curr_key, new_key, merge_ls):
        """Check if merge is appropriate. Make two tiles into one tile with corresponding text and color"""
        new = Board.tiles[new_key]
        curr = Board.tiles[curr_key]
        if (new != curr) and (new['text'] == curr['text']) and new['text']:
            combined = 2 * new['text']
            Board.score += combined
            Board.score_board['text'] = f'SCORE: {Board.score}'
            self.change_tile_appearance(new_key, combined)
            self.remove_tile(curr_key)
            merge_ls.append(new_key)
            return True
        else:
            return False

    def change_tile_appearance(self, key, new, update=False):
        """Changes the tile to display text and change its corresponding color to match"""
        tile = Board.tiles[key]
        if update:
            new = Board.tiles[new]['text']
        tile['text'] = new
        if new >= 2048:
            tile['font'] = ('Helvetica', '20')
            if new >= 326768:
                tile['font'] = ('Helvetica', '15')
            tile['bg'] = num2color[2048]
        else:
            tile['bg'] = num2color[new]

    def test(self):
        """Stuff for test cases: go ahead and max out the scores"""
        k1 = (0, 0)
        k2 = (1, 0)
        k3 = (2, 0)
        k4 = (3, 0)

        def make(key, num):
            self.create_tile(key)
            self.change_tile_appearance(key, num)
        """ 
        self.create_tile(k1)
        self.create_tile(k2)
        self.create_tile(k3)
        self.create_tile(k4)

        self.change_tile_appearance(k1, 2048)
        self.change_tile_appearance(k2, 2048)
        self.change_tile_appearance(k3, 2048)
        self.change_tile_appearance(k4, 2048)
        """

        for key in Board.tiles:
            make(key, 326768)

    #################
    # Game menu funcs
    #################

    def play_again(self):
        """Kills the current game and resets all tiles"""
        for key, tile in Board.tiles.items():
            if tile:
                tile.place_forget()
        Board.filled = []
        Board.score = 0
        Board.score_board['text'] = f'SCORE: {Board.score}'
        time.sleep(0.5)
        Board.againbtn.place_forget()
        self.start_game()

    def end_game(self):
        """Ends the game and displays the play again button"""
        Board.againbtn.place(width=400, height=400, x=0, y=200)
        Board.againbtn.tkraise()


if __name__ == '__main__':
    root = Tk()
    root.title('2048')
    root.geometry('404x600')
    root.resizable(0, 0)
    b = Board(root)
    b.start_game()

    root.mainloop()
