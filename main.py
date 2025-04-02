from stockfish import Stockfish
pars = {
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 2, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 2048, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 4000
}
stockfish = Stockfish(path="./stockfish", depth=20, parameters=pars)

def add_pieces(board: str):
    pieces = {
        "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
        "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟"
    }
    for key, value in pieces.items():
        board = board.replace(key, value)  # Reassign modified string
    return board
stockfish.set_elo_rating(1)
for i in range(10):
    stockfish.make_moves_from_current_position([stockfish.get_best_move()])
    print(add_pieces(stockfish.get_board_visual()))



