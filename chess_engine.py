import chess


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


# Main exe block to test setup
if __name__ == "__main__":
    # Create instance of engine
    engine = ChessEngine()

    # Display the starting board
    engine.display_board()

    # Sample move to show board changing
    # 'e2e4' (UCI format) white pawn from e2 to e4
    try:
        move = chess.Move.from_uci("e2e4")
        if move in engine.board.legal_moves:
            engine.board.push(move)
            print("\n--- After White plays e2e4 ---")
            engine.display_board()
        else:
            print("e2e4 is not legal")
    except ValueError as e:
        print(f"\nError processing move: {e}")

    if engine.board.turn == chess.BLACK:
        print("It is now Black's turn")
