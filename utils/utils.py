from stockfish import Stockfish

def load_setup(_pageSetup, _shape):
    _pageSetup.page_width = _shape.width
    _pageSetup.page_height = _shape.height
    _pageSetup.top_margin = 0
    _pageSetup.left_margin = 0
    _pageSetup.bottom_margin = 0
    _pageSetup.right_margin = 0

def load_stockfish():
    stockfish = Stockfish()
    stockfish.set_depth(10)
    stockfish.set_skill_level(10)
    return stockfish
