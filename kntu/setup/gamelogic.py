import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{0}:{1}".format(self.x, self.y)


class Logic:
    def __init__(self, turn):
        self.turn = turn
        self.score = 0

    def heuristic(self, board):
        opponent = 2
        if self.turn == 2:
            opponent = 1
        our_score = self._score(board, self.turn)
        opponent_score = self._score(board, opponent)
        return our_score - opponent_score

    def _score(self, board, turn):
        score = 0
        for x in board:
            for y in x:
                if y == turn:
                    score += 1
        return score

    def print(self, board):
        for x in board:
            for y in x:
                print(y, end=" ")
            print()

    def get_moves(self, move_arr, x, y, dr, dc, turn, board):
        if dr+x >= 8 or dr+x < 0 or dc+y >= 8 or dc+y < 0:
            return

        if turn == 1:
            turn = 2
        if turn == 2:
            turn = 1

        if turn == board[x+dr][y+dc]:
            return
        if board[x+dr][y+dc] == 0:
            move_arr.append(Point(x+dr, y+dc))
            return

        self.get_moves(move_arr, x+dr, y+dc, dr, dc, turn, board)

    def get_valid_move(self, board, turn):
        opponent = 2
        if turn == 2:
            opponent = 1
        move_arr = []
        for (index_x, x) in enumerate(board):
            for (index_y, y) in enumerate(x):
                if y == turn:
                    for k in range(index_x - 1, index_x + 2):
                        for j in range(index_y - 1, index_y + 2):
                            if board[k][j] == opponent:
                                self.get_moves(move_arr, index_x, index_y, k-index_x, j-index_y, turn, board)

        for x in move_arr:
            print(str(x.x) + " " + str(x.y))

        return move_arr

    def minimax_decision(self, board, turn):
        valid_moves = self.get_valid_move(board, turn)
        self.print(board)
        if len(valid_moves) == 0:
            return False
        else:
            value = -9999
            best_move = valid_moves[0]
            for x in valid_moves:
                board_temp = board.copy()
                board_temp[x.x][x.y] = turn
                self.make_move(board_temp, x)
                self.print(board_temp)
                val = self.minimax_value(board_temp, turn, 2 if turn == 1 else 2, 1)
                if val > value:
                    value = val
                    best_move = x

            return best_move

    def minimax_value(self, temp_board, turn, opponent, depth):
        if depth == 5 or not self.game_over(temp_board):
            return self._score(temp_board, turn)

        valid_moves = self.get_valid_move(temp_board, turn)
        if len(valid_moves):
            return self.minimax_value(temp_board, opponent, turn, depth+1)
        else:
            best_move_value = -9999
            if turn != self.turn:
                best_move_value = 9999
            for x in valid_moves:
                temp_board2 = temp_board.copy()
                temp_board2[x.x][x.y] = turn
                self.make_move(temp_board2, x)
                print(temp_board2)
                value = self.minimax_value(temp_board2, opponent, turn, depth+1)

                if turn == self.turn:
                    if best_move_value < value:
                        best_move_value = value
                else:
                    if best_move_value > value:
                        best_move_value = value

            return best_move_value

    def make_move(self, board, point):
        board[point.x][point.y] = self.turn
        print("*******************************")
        self.print(board)
        print(str(point.x))
        opponent = 2
        if self.turn == 2:
            opponent = 1

        for k in range(point.x-1, point.x+2):
            for j in range(point.y-1, point.y+2):
                if board[k][j] == opponent:
                    if self.is_right_path(board, point.x, point.y, k-point.x, j-point.y, opponent):
                        self.set_moves(point.x, point.y, k-point.x, j-point.y, self.turn, board)

    def is_right_path(self, board, x, y, dr, dc, opponent):
        while True:
            if dr + x > 8 or dr + x < 0 or dc + y > 8 or dc + y < 0:
                return False
            # print("heloo")
            # print("x is: " + str(x))
            # print("y is :" + str(y))
            # print("hello")
            # board[x+dr][y+dc] = self.turn
            self.print(board)
            if board[x+dr][y+dc] == 0:
                return False
            if board[x + dr][y + dc] == self.turn:
                return True
            if board[x+dr][y+dc] == opponent:
                x = x + dr
                y += dc

    def set_moves(self, x, y, dr, dc, turn, board):
        if dr + x > 8 or dr + x < 0 or dc + y > 8 or dc + y < 0:
            return
        print("inside set move")

        board[x+dr][y+dc] = turn

        if turn == board[x + dr][y + dc]:
            return

        if board[x + dr][y + dc] == 0:
            return

        self.set_moves(x + dr, y + dc, dr, dc, turn, board)

    def game_over(self, board):
        for x in board:
            for y in x:
                if y == 0:
                    return False
        return True
