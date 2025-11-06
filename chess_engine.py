import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    # exclude king for now
}

# Score used for checkmate/stalemate to ensure engine prioritizes these outcomes
INF_SCORE = 1000000

# Initial search depth
# Equals half-steps ahead
MAX_DEPTH = 3


class ChessEngine:
    """
    Core class for chess engine
    Manages board state and main logic for AI
    """

    def __init__(self):
        # Init board
        # chess.Board() creates board in standard starting position
        self.board = chess.Board()
        print("Chess Engine Initialized")
        print("Initial FEN: ", self.board.fen())

    def display_board(self):
        # Print current state of board in ASCII form
        print("\n--- Current Board Position ---\n")
        # Lowercase = black pieces, uppercase = white pieces
        print(self.board)
        print("\n----------------------------")

    def evaluate_material(self, board: chess.Board) -> float:
        """
        Calc material score of current board posistion
        Pos score means white is ahead
        Neg score means black is ahead
        """
        score = 0

        # Iterate through all piece types
        for piece_type, value in PIECE_VALUES.items():
            # Count white's pieces
            # self.board.pieces() returns squares where piece type is located
            white_count = len(self.board.pieces(piece_type, chess.WHITE))
            score += white_count * value

            black_count = len(self.board.pieces(piece_type, chess.BLACK))
            score -= black_count * value

        return score

    def minimax(
        self,
        board: chess.Board,
        depth: int,
        alpha: float,
        beta: float,
        is_maximizing_player: bool,
    ) -> float:
        """
        Recursive Minimax search function
        Assumes White tries to maximize the score
        and Black tries to minimize the score
        Alpha is the best score found for maximizing player
        Beta is the best score found for minimizing player
        """
        # Base Case: Game over or depth reached
        if depth == 0:
            return self.evaluate_material(board)

        if board.is_game_over():
            result = board.outcome()

            if result is None:
                # Just to be safe, should never happen
                return 0

            # Checkmate handler
            if board.is_checkmate():
                # Loss for Maximizer is -INF
                # Loss for Minimizer is +INF

                # Winner determined by prev move
                # Reward faster wins and delay faster losses by add/sub the depth
                if result.winner == chess.WHITE:
                    return INF_SCORE + depth
                elif result.winner == chess.BLACK:
                    return -INF_SCORE - depth

            # Stalemate
            return 0

        # Recursive Step
        # Maximizing Player
        if is_maximizing_player:
            max_eval = -INF_SCORE

            # Iter thru ALL legal moves
            for move in board.legal_moves:
                # Make move on the board
                board.push(move)
                # Recursive call minimax, pass cur a and b and switch players
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                # Undo move to restore board state for next move search
                board.pop()

                # Update max score found so fat
                max_eval = max(max_eval, evaluation)

                # Alpha-Beta Pruning
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    # If alpha is better than beta, we prune
                    # Minimizer will never allow game to reach this path
                    return max_eval

            return max_eval

        # Minimizing player
        else:
            min_eval = INF_SCORE

            # Iterate thru ALL legal moves
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                min_eval = min(min_eval, evaluation)

                beta = min(beta, min_eval)
                if alpha >= beta:
                    return min_eval

            return min_eval

    def find_best_move(self, depth: int) -> chess.Move:
        """
        Finds best legal move for current player using minimax algo
        """
        # Score eval from Maximizers perspective
        if self.board.turn == chess.WHITE:
            best_eval = -INF_SCORE
        else:
            best_eval = INF_SCORE

        alpha = -INF_SCORE
        beta = INF_SCORE

        best_move = None

        # Det who current turn is
        is_maximizing_player = self.board.turn == chess.WHITE

        # Loop thru all possible root moves
        for move in self.board.legal_moves:
            # Make move
            self.board.push(move)

            # Call minimax for opponent
            current_eval = self.minimax(
                self.board, depth - 1, alpha, beta, not is_maximizing_player
            )

            # Undo move
            self.board.pop()

            # Check if move is better than cur best
            if is_maximizing_player:
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = move
                alpha = max(alpha, best_eval)
            else:
                if current_eval < best_eval:
                    best_eval = current_eval
                    best_move = move
                beta = min(beta, best_eval)

        print(f"\nSearch complete (Depth {depth}). Best score found: {best_eval}")

        if best_move:
            print(f"Engine selected move: {best_move.uci()} (UCI)")
        else:
            print("No legal moves found")

        return best_move

    def start_game_loop(self):
        """
        Starts terminal-based game loop
        Human player is uppercase pieces
        Chess engine is lowercase pieces
        """
        self.board.set_fen(chess.STARTING_FEN)
        print("\n--- Game Start: Human vs Engine ---")
        print("Enter moves in UCI format (e.g. e2e4). Type 'quit' or 'resign' to end")

        while not self.board.is_game_over():
            self.display_board()

            current_turn = (
                "White (Human)" if self.board.turn == chess.WHITE else "Black (Engine)"
            )
            print(
                f"It is {current_turn}'s turn. Current eval (White's advantage): {self.evaluate_material(self.board):.2f}"
            )

            if self.board.turn == chess.WHITE:
                # Human turn
                while True:
                    try:
                        uci_move = input("Your move: ").strip().lower()

                        # Handle resign
                        if uci_move in ["quit", "resign"]:
                            print("You resigned, Engine wins")
                            return

                        # Handle UCI conversion
                        move = chess.Move.from_uci(uci_move)

                        # Check move legal
                        if move in self.board.legal_moves:
                            self.board.push(move)
                            break
                        else:
                            print("Illegal move. Try again")

                    except ValueError:
                        print("Invalid move format")
            # Engine turn
            else:
                print(f"Engine is thinking (Depth {MAX_DEPTH})...")
                engine_move = self.find_best_move(MAX_DEPTH)

                if engine_move:
                    print(f"Engine plays: {engine_move.uci()}")
                    self.board.push(engine_move)
                else:
                    print("Engine found no legal moves")
                    break

        # Game Over
        self.display_board()

        outcome = self.board.outcome
        if outcome:
            print("Game Over")
            if self.board.is_checkmate():
                winner = (
                    "White (You)" if outcome.winner == chess.WHITE else "Black (Engine)"
                )
                print(f"Checkmate! {winner} wins.")
            else:
                print(f"Game ended in a draw: {outcome.termination.name}")
        else:
            print("Game ended")


# Main exe block to test setup
if __name__ == "__main__":
    # Create instance of engine
    engine = ChessEngine()

    engine.start_game_loop()
