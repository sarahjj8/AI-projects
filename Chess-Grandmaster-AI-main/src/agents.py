import datetime
import random

import chess

import utiles


class Agent:
    """
        Base class for agents.
    """

    def __init__(self, board: chess.Board, next_player) -> None:
        self.board = board
        self.next_player = next_player

    def get_action(self):
        """
            This method receives a GameState object and returns an action based on its strategy.
        """
        pass

    """
            get possible moves : 
                possibleMoves = board.legal_moves

            create a move object from possible move : 
                move = chess.Move.from_uci(str(possible_move))

            push the move : 
                board.push(move)

            pop the last move:
                board.pop(move)
    """


class RandomAgent(Agent):
    def __init__(self, board: chess.Board, next_player):
        super().__init__(board, next_player)

    def get_action(self):
        return self.random()

    def random(self):
        possible_moves_list = list(self.board.legal_moves)

        random_move = random.choice(possible_moves_list)
        return chess.Move.from_uci(str(random_move))


class MinimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        best_move = self.minimax(self.depth, self.next_player, True)[1]
        return best_move

    def minimax(self, depth, turn, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            return evaluate_board_state(self.board, turn), None

        if is_maximizing:
            max_eval = float("-inf")
            best_move = None
            possible_moves = list(self.board.legal_moves)
            for possible_move in possible_moves:
                move = chess.Move.from_uci(str(possible_move))
                self.board.push(move)       # Pushing a move onto the board to simulate that move and see its consequences.
                eval, _ = self.minimax(depth - 1, turn, False)
                self.board.pop()      # reverting the board back to its previous state
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            possible_moves = list(self.board.legal_moves)
            for possible_move in possible_moves:
                move = chess.Move.from_uci(str(possible_move))
                self.board.push(move)
                eval, _ = self.minimax(depth - 1, turn, True)
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move


class AlphaBetaAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        return self.alpha_beta(self.depth, self.next_player, True, float("-inf"), float("inf"))[1]

    def alpha_beta(self, depth, turn, is_maximizing, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            return evaluate_board_state(self.board, turn), None

        if is_maximizing:
            max_eval = float("-inf")
            best_move = None
            for possible_move in self.board.legal_moves:
                move = chess.Move.from_uci(str(possible_move))
                self.board.push(move)
                eval = self.alpha_beta(depth - 1, turn, False, alpha, beta)[0]
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= max_eval:
                    return max_eval, best_move
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.alpha_beta(depth - 1, turn, True, alpha, beta)[0]
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if min_eval <= alpha:
                    return min_eval, best_move
            return min_eval, best_move


class ExpectimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        return self.expectimax(self.depth, self.next_player, True)[1]
    def expectimax(self, depth, turn, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            return evaluate_board_state(self.board, turn), None

        if is_maximizing:
            max_eval = float("-inf")
            best_move = None
            for possible_move in self.board.legal_moves:
                move = chess.Move.from_uci(str(possible_move))
                self.board.push(move)
                eval = self.expectimax(depth - 1, turn, False)[0]
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            total_eval = 0
            num_moves = 0
            for possible_move in self.board.legal_moves:
                move = chess.Move.from_uci(str(possible_move))
                self.board.push(move)
                eval = self.expectimax(depth - 1, turn, True)[0]
                self.board.pop()
                total_eval += eval
                num_moves += 1
            average_eval = total_eval / num_moves
            return average_eval, None


def evaluate_board_state(board, turn):
    node_evaluation = 0
    node_evaluation += utiles.check_status(board, turn)
    node_evaluation += utiles.evaluationBoard(board)
    node_evaluation += utiles.checkmate_status(board, turn)
    node_evaluation += utiles.good_square_moves(board, turn)
    if turn == 'white':
        return node_evaluation
    return -node_evaluation
