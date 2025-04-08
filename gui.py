import arcade, arcade.gui
from stockfish import Stockfish
from enum import Enum
import os
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
    "Minimum Thinking Time": 0,
    "Slow Mover": 0,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 40
}

def locate_stockfish():
    for i in os.listdir("."):
        if "stockfish" in i:
            return f"./{i}"
    raise FielNotFoundError
class Window(arcade.Window):
    def __init__(self, sise=1):
        self.sise = sise
        width=480*sise
        height=480*sise
        super().__init__(width=480*sise+sise*240, height=480*sise, title="chess")
        self.board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
        ]
        path = locate_stockfish()
        self.engine = Stockfish(path=path, depth=20, parameters=params) 
        self.load_pieces()
        self.aspect_ration = width/height
        self.original_width = width
        self.original_height = height
        self.guiw = width+(sise*120)
        self.moves = []
        self.draw_moves = []
        self.move_back = 0
        self.get_move(None)
        self.moves = []
        #gui
        self.man = arcade.gui.UIManager()
        box = arcade.gui.UIBoxLayout()
        b = arcade.gui.UIFlatButton(text="get FEN",x=self.guiw, width=sise*240)
        box.add(b)
        self.man.add(box)
        self.state= {"mate":0}


        #test
        self.engine.set_fen_position("8/8/1k6/8/8/8/r7/q2K4 b - - 0 1")
        wld = self.engine.get_wdl_stats()
        print(wld)
    def update_from_fen(self):
        fen = self.engine.get_fen_position()
        fen = fen.split(" ")[1:]
        self.state["move"] = fen[0]
    def on_update(self, dt):
        self.draw_moves = self.moves[:len(self.moves) - self.move_back]
        self.update_from_fen()
    def get_move(self, move):
        if move:  # Если передан ход, добавляем его в список ходов
            self.moves.append(move)
        self.engine.set_position(self.draw_moves)  # Устанавливаем позицию на основе текущих ходов
        m = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }
        s = {v: k for k, v in m.items()}  # Обратное отображение для преобразования чисел в буквы
        for i in range(8):
            for n in range(8):
                square = f"{s[i]}{n + 1}"  # Преобразуем координаты в шахматную нотацию
                piece = self.engine.get_what_is_on_square(square)  # Получаем фигуру на клетке
                self.board[n][i] = piece  # Обновляем доску

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            arcade.close_window()
        if key == arcade.key.SPACE:
            self.engine.set_position(self.draw_moves)  # Устанавливаем текущую позицию
            move = self.engine.get_best_move()  # Получаем лучший ход от Stockfish
            if not move:
                return
            self.get_move(move)  # Добавляем ход в список
        if key == arcade.key.LEFT and self.move_back < len(self.moves):
            self.move_back += 1  # Увеличиваем счётчик отката ходов
        if key == arcade.key.RIGHT and self.move_back > 0:
            self.move_back -= 1  # Уменьшаем счётчик отката ходов
        # Обновляем список ходов для отрисовки
        self.draw_moves = self.moves[:len(self.moves) - self.move_back]
        print(self.moves, self.draw_moves, self.move_back)
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
                if pr is not None:
                    p = self.pieces[pr.name]
                    p.center_x=(self.sise*30)+x*60*self.sise
                    p.center_y = (self.sise*30)+y*60*self.sise
                    p.draw()
        self.man.draw()

        wdl = self.engine.get_wdl_stats()
        if wdl[0]==1000:
            w, h = super().width, super().height
            color = {"b":(0,0,0),"w":(255,255,255)}[self.state["move"]]
            arcade.draw_text("МАТ",start_x=w/2, start_y=h/2, color=color)
    def load_pieces(self):
        self.pieces = {
       "WHITE_ROOK": arcade.Sprite("rl.png", self.sise),  # Белая ладья
       "BLACK_ROOK": arcade.Sprite("rd.png", self.sise),  # Чёрная ладья
       "WHITE_KNIGHT": arcade.Sprite("nl.png", self.sise),  # Белый конь
       "BLACK_KNIGHT": arcade.Sprite("nd.png", self.sise),  # Чёрный конь
       "WHITE_BISHOP": arcade.Sprite("bl.png", self.sise),  # Белый слон
       "BLACK_BISHOP": arcade.Sprite("bd.png", self.sise),  # Чёрный слон
       "WHITE_QUEEN": arcade.Sprite("ql.png", self.sise),  # Белый ферзь
       "BLACK_QUEEN": arcade.Sprite("qd.png", self.sise),  # Чёрный ферзь
       "WHITE_KING": arcade.Sprite("kl.png", self.sise),  # Белый король
       "BLACK_KING": arcade.Sprite("kd.png", self.sise),  # Чёрный король
       "WHITE_PAWN": arcade.Sprite("pl.png", self.sise),  # Белая пешка
       "BLACK_PAWN": arcade.Sprite("pd.png", self.sise),  # Чёрная пешка
}

def main():
    window = Window(sise = 1)
    arcade.run()
if __name__=="__main__":
    main()
