import random
import chess
import chess.svg
import aspose.words as aw
from utils.utils import *

class Chess():
    def __new__(cls, *args):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Chess, cls).__new__(cls)
        return cls._instance

    def __init__(self, strength=1, depth=1):
        self.stockfish = load_stockfish(strength, depth)
        self.board = chess.Board()
        self.color = None
        self.doc = None
        self.svg = None
        self.builder = None
        self.shape = None
        self.pageSetup = None

    def __repr__(self):
        return self.board
    
    def render_png(self):
        if not self.color:
            self.svg = chess.svg.board(self.board, size=550, flipped=True)
        else:
            self.svg = chess.svg.board(self.board, size=550)

        with open('board.svg', 'w') as file:
            file.seek(0)
            file.write(self.svg)
            file.close()
        
        self.doc = aw.Document()
        self.builder = aw.DocumentBuilder(self.doc)

        self.shape = self.builder.insert_image('board.svg')
        self.pageSetup = self.builder.page_setup
        self.pageSetup.page_width = self.shape.width
        self.pageSetup.page_height = self.shape.height
        self.pageSetup.top_margin = 0
        self.pageSetup.left_margin = 0
        self.pageSetup.bottom_margin = 0
        self.pageSetup.right_margin = 0

        self.doc.save('board.png')
    
    def move(self, position: str): 
        try:
            self.board.push_san(position)
        except ValueError:
            return 1
        
    def stockfish_move(self):
        self.stockfish.set_fen_position(self.board.fen())
        moves = self.stockfish.get_top_moves(num_top_moves=3)
        rnd = random.sample(moves, 1)
        self.board.push_uci(rnd[0]['Move'])
        return rnd[0]['Move']

    def check_position(self):
        self.stockfish.set_fen_position(self.board.fen())
        rate = self.stockfish.get_evaluation()
        if rate['value'] < 0:
            return (rate['value'], 0)
        else:
            return (rate['value'], 1)
    
    def state(self):
        if self.board.is_checkmate():
            return 1
        elif self.board.is_stalemate():
            return 2
        
    def choose_color(self, color=str):
        if color == "White":
            self.board.turn = chess.WHITE
            self.color = 1
        elif color == "Black":
            self.board.turn = chess.BLACK
            self.color = 0
