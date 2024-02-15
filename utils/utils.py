from stockfish import Stockfish

def load_stockfish(strength, depth):
    stockfish = Stockfish()
    stockfish.set_skill_level(strength)
    stockfish.set_depth(depth)
    return stockfish