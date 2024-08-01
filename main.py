from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Line, Ellipse
from kivy.graphics.context_instructions import  Color
from kivy.metrics import dp
from kivymd.uix.button import MDFloatingActionButton, MDIconButton, MDFlatButton, MDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
Builder.load_file("Connect4.kv")


class Game():
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [['.' for col in range(self.columns)] for row in range(self.rows)]
        self.game_over = False
        self.turn = "x"

    def reset_game(self):
        self.turn = "x"
        self.board = [['.' for col in range(self.columns)] for row in range(self.rows)]
        App.Game_Screen.reset_all_buttons()
        for input_btn in App.Game_Screen.input_buttons_list:
            input_btn.disabled = False
        if self.game_over == True:
            self.game_over = False
            App.Game_Screen.winning_line.points = [0, 0, 0, 0]
        App.Game_Screen.update_green_circle("o")

    def take_input(self, col_num):
        col = int(col_num) - 1

        if self.board[0][col] == ".":
            # check if col full or not. if col has empty spaces, then top box
            # must have "."

            # Row will iterate from last row to check for empty squares in the last row
            for row in range(len(self.board)):
                last_row = len(self.board) - row - 1
                if self.board[last_row][col] == ".":
                    self.board[last_row][col] = self.turn
                    App.Game_Screen.update_button(last_row, col)
                    break
                else:
                    continue

            self.check_game_over()
            self.change_turn()

        self.check_if_col_full(col)

    def check_if_col_full(self, col):
        if self.board[0][col] != ".":
            App.Game_Screen.disable_input_button(col)

    def check_game_over(self):
        row_len = len(self.board)
        col_len = len(self.board[0])
        self.board.reverse() # Reverses so that during checking it only enters if col =/= "."
        for row_num, row in enumerate(self.board): # So that I can find the number of iterations also
            i = row_num
            for col_num, col in enumerate(row):
                j = col_num
                if col != ".":
                    # Check top to bottom

                    # row_len - row_num >= 4 So that list index does not go out of range
                    if (row_len-row_num>=4) and (self.board[i][j]==self.board[i+1][j]==self.board[i+2][j]==self.board[i+3][j]):
                        App.Game_Screen.show_winning_dialog(self.turn)
                        App.Game_Screen.update_green_circle(self.turn, wins=True)
                        self.game_over = True
                        App.Game_Screen.draw_winning_line(i, j, i+3, j)
                        App.Game_Screen.disable_all_input_button()

                    # Check Horizontal
                    elif (col_len-col_num>=4) and (self.board[i][j]==self.board[i][j+1]==self.board[i][j+2]==self.board[i][j+3]):
                        App.Game_Screen.show_winning_dialog(self.turn)
                        App.Game_Screen.update_green_circle(self.turn, wins=True)
                        self.game_over = True
                        App.Game_Screen.draw_winning_line(i, j, i, j+3)
                        App.Game_Screen.disable_all_input_button()

                    # Check Diagonals
                    elif (row_len-row_num>=4 and col_len-col_num>=4):
                        if self.board[i][j]==self.board[i+1][j+1]==self.board[i+2][j+2]==self.board[i+3][j+3]:
                            App.Game_Screen.show_winning_dialog(self.turn)
                            App.Game_Screen.update_green_circle(self.turn, wins=True)
                            self.game_over = True
                            App.Game_Screen.draw_winning_line(i, j, i+3, j+3)
                            App.Game_Screen.disable_all_input_button()
                    elif row_num >= 3 and col_len - col_num >= 4:
                        if self.board[i][j]==self.board[i-1][j+1]==self.board[i-2][j+2]==self.board[i-3][j+3]:
                            App.Game_Screen.show_winning_dialog(self.turn)
                            App.Game_Screen.update_green_circle(self.turn, wins=True)
                            self.game_over = True
                            App.Game_Screen.draw_winning_line(i, j, i-3,j+3)
                            App.Game_Screen.disable_all_input_button()

        self.board.reverse()

    def change_turn(self):
        if self.turn == "x":
            self.turn = "o"
        elif self.turn == "o":
            self.turn = "x"

class HomeScreen(MDScreen):
    pass

class LeftEllipse(Widget):
    def __init__(self, **kwargs):
        super(LeftEllipse, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 0, 1)
            self.left_ellipse = Ellipse(size=(75, 50), pos=(150, 500))


class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.red_img_src = "Assets/Red.jpeg"
        self.black_img_src = "Assets/Black.jpeg"
        self.yellow_img_src = "Assets/Yellow.jpeg"

        self.grid_buttons = []

        self.input_buttons_list = []
        self.winning_line = None


        self.winning_line_drawn_once = False # If true, then only the position will change for the subsequent games. It
        # is needed for reset

        self.right_circle = None
        self.left_circle = None



    def on_enter(self, *args):
        self.grid = self.ids.grid_layout
        self.input_buttons = self.ids.input_buttons
        for i in range(game.rows):
            row_buttons = []
            for j in range(game.columns):
                btn = Button(background_disabled_normal=self.black_img_src)
                btn.disabled = True

                row_buttons.append(btn)
                self.grid.add_widget(btn)
            self.grid_buttons.append(row_buttons)

        # Buttons for taking input
        for i in range(game.columns):
            btn = MDIconButton(text=str(i + 1), size_hint=(1, 1), icon="arrow-down-bold", text_color=[0, 0, 0, 0])
            btn.bind(on_press=self.take_input)
            self.input_buttons_list.append(btn)
            self.input_buttons.add_widget(btn)

        self.draw_left_circle()
        self.draw_right_circle()

    def show_winning_dialog(self, winner):
        winner_ = ""
        if winner == "x":
            winner_ = "Red"
        elif winner == "o":
            winner_ = "Yellow"

        self.dialog = MDDialog(
            text = f"{winner_} wins!",
            buttons=[
                MDFlatButton(text="Close", on_press=self.close_winning_dialog),
                MDFlatButton(text="Play Again", on_press=App.reset_game)
            ]
        )
        self.dialog.open()
    def close_winning_dialog(self, dialog):
        self.dialog.dismiss()

    def draw_left_circle(self):
        left_turn = self.ids.left_turn # Left Relative Layout
        size_ = left_turn.size[0] * 0.5, left_turn.size[0] * 0.5
        pos_= left_turn.size[0] * 0.5 - (left_turn.size[0] * 0.5)/2, left_turn.size[1] - (left_turn.size[0] * 0.65)
        with left_turn.canvas:
            self.left_ellipse_color = Color(1, 0, 0, 1)
            self.left_ellipse = Ellipse(size=size_, pos=pos_)
            self.left_circle_line_color = Color(0, 1, 0, 1)
            self.left_circle_line = Line(circle=(size_[0]/2 + pos_[0], size_[1]/2 + pos_[1], size_[0]/2), width=dp(3))

    def draw_right_circle(self):
        right_turn = self.ids.right_turn
        size_ = right_turn.size[0] * 0.5, right_turn.size[0] * 0.5
        pos_ = right_turn.size[0] * 0.5 - (right_turn.size[0] * 0.5)/2, right_turn.size[1] - (right_turn.size[0] * 0.65)
        with right_turn.canvas:
            self.right_ellipse_color = Color(238/255, 245/255, 60/245, 1)
            self.right_ellipse = Ellipse(size = size_, pos=pos_)
            self.right_circle_line_color = Color(0, 1, 0, 0)
            self.right_circle_line = Line(circle=(size_[0]/2 + pos_[0], size_[1]/2 + pos_[1], size_[0]/2), width=dp(3))

    def update_green_circle(self, turn, wins=False):
        if wins == False:
            if turn == "x":
                self.left_circle_line_color.rgba = [0, 1, 0, 0]
                self.right_circle_line_color.rgba = [0, 1, 0, 1]
            elif turn == "o":
                self.left_circle_line_color.rgba = [0, 1, 0, 1]
                self.right_circle_line_color.rgba = [0, 1, 0, 0]
        elif wins == True:
            if turn == "o":
                self.left_circle_line_color.rgba = [0, 1, 0, 0]
                self.right_circle_line_color.rgba = [43/255, 255/255, 0, 1]
            elif turn == "x":
                self.left_circle_line_color.rgba = [43/255, 255/255, 0, 1]
                self.right_circle_line_color.rgba = [0, 1, 0, 0]

    def take_input(self, btn):
        self.update_green_circle(App.game.turn)
        game.take_input(btn.text)

    def disable_input_button(self, btn_col):
        self.input_buttons_list[btn_col].disabled = True

    def disable_all_input_button(self):
        for btn in self.input_buttons_list:
            btn.disabled = True

    def update_button(self, row, col):
        btn = self.grid_buttons[row][col]
        # btn.text = game.board[row][col]
        if game.board[row][col] == "x":
            btn.background_disabled_normal = self.red_img_src
        elif game.board[row][col] == "o":
            btn.background_disabled_normal = self.yellow_img_src

    def reset_all_buttons(self):
        for row in self.grid_buttons:
            for btn in row:
                btn.background_disabled_normal = self.black_img_src

    def draw_winning_line(self, row1, col1, row2, col2):
        self.grid_buttons.reverse()
        x1, y1 = self.grid_buttons[row1][col1].center
        x2, y2 = self.grid_buttons[row2][col2].center
        self.grid_buttons.reverse()
        # Reversing Because when checking for win, the board was reversed.
        if self.winning_line_drawn_once == False:
            with self.canvas:
                self.winning_line_color = Color(0, 1, 0, 1)
                self.winning_line = Line(points=[x1, y1, x2, y2], width=dp(3.5))
            self.winning_line_drawn_once = True
        else:
            self.winning_line.points = [x1, y1, x2, y2]


class Connect4App(MDApp):
    def build(self):
        Window.size = (315, 700)
        self.game = game
        self.width = Window.width
        self.height = Window.height

        self.theme_cls.theme_style = "Light"
        self.Home_Screen = HomeScreen(name="home_screen")
        self.Game_Screen = GameScreen(name="game_screen")
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.Home_Screen)
        self.screen_manager.add_widget(self.Game_Screen)

        return self.screen_manager
    def reset_game(self, here_for_fixing_dialog=None):
        if here_for_fixing_dialog is not None:
            self.Game_Screen.close_winning_dialog(None)
        self.game.reset_game()
    def change_screen(self):

        self.screen_manager.current = "game_screen"

if __name__ == "__main__":
    game = Game()
    App = Connect4App()
    App.run()