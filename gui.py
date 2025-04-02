import arcade
from stockfish import Stockfish

params = {
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
    "UCI_Elo": 40000
} 

class Window(arcade.Window):
    def __init__(self, sise=1):
        self.sise = sise
        super().__init__(width=480*sise, height=480*sise, title="chess")
        self.board = [
        ["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
        ["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
        ["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]
        ]
        self.engine = Stockfish(path="./stockfish", depth=20, parameters=params) 
        self.engine.set_fen_position("8/6P1/8/8/8/1K1k4/8/8 w - - 0 1")
        self.load_pieces()
    def on_update(self, dt):
        self.get_move(None)
    def get_move(self, move):
        self.engine.make_moves_from_current_position(move)
        m = {
            "a":0,
            "b":1,
            "c":2,
            "d":3,
            "e":4,
            "f":5,
            "g":6,
            "h":7
        }
        s = {}
        for i in m:
            s[m[i]] = i
        for i in range(8):
            for n in range(8):
                k= s[i]
                self.board[n][i] = type(self.engine.get_what_is_on_square(f"{k}{n+1}"))

    def on_key_press(self, *argvs):#on_update(self, dt):
        move = self.engine.get_best_move()
        if not move:
            return
        self.get_move(move)
        self.engine.make_moves_from_current_position([move])
    def on_draw(self):
        arcade.start_render()
        for x in range(8):
            for y in range(8):
                xp = (30*self.sise)+x*60*self.sise
                yp = (self.sise*30)+y*60*self.sise
                if (y%2==0 and x%2==0) or (y%2==1 and x%2==1):
                    color = (118,150,85)
                else:
                    color = (238,238,210)
                arcade.draw_rectangle_filled(center_x=xp, center_y=yp, width=60*self.sise, height=60*self.sise, color = color)
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                pr = self.board[y][x]
                if not pr:
                    continue
                p = self.pieces[pr]
                p.center_x=(self.sise*30)+x*60*self.sise
                p.center_y = (self.sise*30)+y*60*self.sise
                p.draw()
    def load_pieces(self):
        self.pieces = {
        Stockfish.Piece.WHITE_ROOK: arcade.Sprite("rl.png", self.sise),  # Белая ладья
        Stockfish.Piece.BLACK_ROOK: arcade.Sprite("rd.png", self.sise),  # Чёрная ладья
        Stockfish.Piece.WHITE_KNIGHT: arcade.Sprite("nl.png", self.sise),  # Белый конь
    Stockfish.Piece.BLACK_KNIGHT: arcade.Sprite("nd.png", self.sise),  # Чёрный конь
    Stockfish.Piece.WHITE_BISHOP: arcade.Sprite("bl.png", self.sise),  # Белый слон
    Stockfish.Piece.BLACK_BISHOP: arcade.Sprite("bd.png", self.sise),  # Чёрный слон
    Stockfish.Piece.WHITE_QUEEN: arcade.Sprite("ql.png", self.sise),  # Белый ферзь
    Stockfish.Piece.BLACK_QUEEN: arcade.Sprite("qd.png", self.sise),  # Чёрный ферзь
    Stockfish.Piece.WHITE_KING: arcade.Sprite("kl.png", self.sise),  # Белый король
    Stockfish.Piece.BLACK_KING: arcade.Sprite("kd.png", self.sise),  # Чёрный король
    Stockfish.Piece.WHITE_PAWN: arcade.Sprite("pl.png", self.sise),  # Белая пешка
    Stockfish.Piece.BLACK_PAWN: arcade.Sprite("pd.png", self.sise),  # Чёрная пешка
}

def main():
    window = Window(sise = 1)
    arcade.run()
if __name__=="__main__":
    main()
