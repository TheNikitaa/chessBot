import chess
import chess.svg
import aspose.words as aw
from utils.utils import *

class Chess():
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Chess, cls).__new__(cls)
            cls._instance.is_initiated = False

        return cls._instance

    def __init__(self):
        if not self.is_initiated:
            self.is_initiated = True

        self.stockfish = load_stockfish()
        self.board = chess.Board()
        self.doc = aw.Document()
        self.fileName = 'board'
        self.svg = None
        self.builder = None
        self.shape = None
        self.pageSetup = None

    def __repr__(self):
        return self.board

    def save_svg(self):
        self.svg = chess.svg.board(self.board, size=550)
        
        with open(f'{self.fileName}.svg', 'w') as file:
            file.seek(0)
            file.write(self.svg)
            file.close()
    
    def render_png(self):
        if self.builder is None:
            self.builder = aw.DocumentBuilder(self.doc)
        
        if self.pageSetup is None:
            self.pageSetup = self.builder.page_setup

        self.shape = self.builder.insert_image(f'{self.fileName}.svg')
        load_setup(self.pageSetup, self.shape)
        self.doc.save(f'{self.fileName}.png')
    
    def move(self, position: str): 
        try:
            self.board.push_san(position)
        except ValueError:
            return 'Uncorrect move'       

    def check_position(self):
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_evaluation()


game = Chess()
mv = 'Nf3'
a = game.move(mv)

if a != None:
    print(a)
else:
    game.move(mv)

game.save_svg()
game.render_png()
print(game.check_position())
