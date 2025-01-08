from high_score import get_high_score, save_high_score

# Helper function to generate the next Fibonacci number in a sequence
def is_fibonacci_mergeable(a, b):
    fib = [1, 1]
    while fib[-1] < max(a, b):
        fib.append(fib[-1] + fib[-2])
    return a in fib and b in fib and abs(fib.index(a) - fib.index(b)) == 1

# Initialize the board
def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    add_random_tile(board)
    add_random_tile(board)
    return board

# Add a random tile (1 or 2) to an empty position on the board
def add_random_tile(board):
    import random
    empty_positions = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if not empty_positions:
        return
    r, c = random.choice(empty_positions)
    board[r][c] = random.choice([1, 2])

# Merge the tiles in a row or column
def merge_line(line):
    new_line = [num for num in line if num != 0]
    for i in range(len(new_line) - 1):
        if is_fibonacci_mergeable(new_line[i], new_line[i + 1]):
            new_line[i] += new_line[i + 1]
            new_line[i + 1] = 0
    return [num for num in new_line if num != 0] + [0] * (len(line) - len(new_line))

# Rotate the board clockwise
def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

# Move the board in a specific direction
def move(board, direction):
    moved = False
    if direction in ['up', 'down']:
        board = rotate_board(board)
    for i in range(4):
        original_line = board[i][:]
        if direction in ['right', 'down']:
            board[i] = merge_line(board[i][::-1])[::-1]
        else:
            board[i] = merge_line(board[i])
        if board[i] != original_line:
            moved = True
    if direction in ['up', 'down']:
        for _ in range(3):
            board = rotate_board(board)
    if moved:
        add_random_tile(board)
    return moved

# Check if the game is over
def is_game_over(board):
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return False
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 4 and 0 <= nc < 4 and is_fibonacci_mergeable(board[r][c], board[nr][nc]):
                    return False
    return True

# Print the board
def print_board(board):
    for row in board:
        print(' '.join(f'{num:4}' if num != 0 else '    ' for num in row))
    print()

# Main game loop
def main():
    board = initialize_board()
    high_score = get_high_score()
    current_score = 0

    print("Welcome to the 2048 Fibonacci Game! Use 'w', 'a', 's', 'd' to move.")
    print(f"High Score: {high_score}")
    
    while True:
        print_board(board)
        print(f"Current Score: {current_score}")
        
        if is_game_over(board):
            print("Game Over! No more moves available.")
            if current_score > high_score:
                print(f"New High Score: {current_score}!")
                save_high_score(current_score)
            break
        
        move_input = input("Your move (w/a/s/d): ").strip().lower()
        if move_input in ['w', 'a', 's', 'd']:
            direction = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}[move_input]
            if move(board, direction):
                current_score += 10  # Example scoring
            else:
                print("Invalid move! Try again.")
        else:
            print("Invalid input! Use 'w', 'a', 's', 'd'.")

if __name__ == "__main__":
    main()
