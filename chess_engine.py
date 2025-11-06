import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    # exclude king for now
}


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

    def evaluate_material(self) -> float:
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


# Main exe block to test setup
if __name__ == "__main__":
    # Create instance of engine
    engine = ChessEngine()

    # Display the starting board
    engine.display_board()
    # Initial Evaluation (should be 0 as they are even)
    initial_score = engine.evaluate_material()
    print(f"Material Evaluation (Starting Board): {initial_score}")

    # Sample move to show board changing
    # 'e2e4' (UCI format) white pawn from e2 to e4
    try:
        move_e2e4 = chess.Move.from_uci("e2e4")
        if move_e2e4 in engine.board.legal_moves:
            engine.board.push(move_e2e4)
            print("\n--- After White plays e2e4 ---")
            engine.display_board()
            score_after_e2e4 = engine.evaluate_material()
            # Should still be 0
            print(f"Material Evaluation: {score_after_e2e4}")

        else:
            print("e2e4 is not legal")

        move_d7d5 = chess.Move.from_uci("d7d5")
        if move_d7d5 in engine.board.legal_moves:
            engine.board.push(move_d7d5)
            print("\n--- After Black plays d7d5 (No Capture) ---")
            engine.display_board()
            score_after_d7d5 = engine.evaluate_material()
            # Should still be 0
            print(f"Material Evaluation: {score_after_d7d5}")

        # Capturing move
        # White plays exd5 (pawn capture pawn)
        move_exd5 = chess.Move.from_uci("e4d5")
        if move_exd5 in engine.board.legal_moves:
            engine.board.push(move_exd5)
            print("\n--- After White plays exd5 (Pawn captures Pawn) ---")
            engine.display_board()
            score_after_capture = engine.evaluate_material()
            # Should be 1 (White is winning)
            print(f"Material Evaluation: {score_after_capture}")

    except ValueError as e:
        print(f"\nError processing move: {e}")

    if engine.board.turn == chess.BLACK:
        print("It is now Black's turn")
    else:
        print("It is not White's turn")
