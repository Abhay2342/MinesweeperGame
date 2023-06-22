import random

class MinesweeperGame:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.num_cells = size * size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mine_positions = []
        self.is_game_over = False

    def initialize_board(self, initial_row, initial_col):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        positions.remove((initial_row, initial_col))
        self.mine_positions = random.sample(positions, self.num_mines)
        self.open_cell(initial_row, initial_row)

    def count_adjacent_mines(self, row, col):
        count = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size and (r, c) in self.mine_positions:
                count += 1
        return count

    def display_board(self):
        print(' ' + ' '.join(str(i) for i in range(self.size)))
        print(' +' + '-' * self.size)
        for i, row in enumerate(self.board):
            print(f"{i}|{' '.join(str(cell) for cell in row)}|")
        print(' +' + '-' * self.size)

    def play(self):
        print('Minesweeper Game')
        print('----------------')
        self.display_board()

        while not self.is_game_over:
            row = self.get_valid_input('Enter row: ')
            col = self.get_valid_input('Enter column: ')
            action = self.get_valid_action()

            if self.board[row][col] == ' ' and action == 'open':
                if (row, col) in self.mine_positions:
                    self.is_game_over = True
                    self.show_mines()
                    print('Game Over! You hit a mine.')
                else:
                    self.open_cell(row, col)
                    self.check_victory()
            elif self.board[row][col] == ' ' and action == 'mark':
                self.mark_cell(row, col)
            elif self.board[row][col] == 'X' and action == 'unmark':
                self.unmark_cell(row, col)
            else:
                print('Invalid move! Please try again.\n')

            self.display_board()

    def open_cell(self, row, col):
        if (row, col) in self.mine_positions:
            return

        count = self.count_adjacent_mines(row, col)
        self.board[row][col] = str(count)

        if count == 0:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == ' ':
                    self.open_cell(r, c)


    def mark_cell(self, row, col):
        if self.num_mines <= 0:
            print('No more mines to mark!')
        else:
            self.board[row][col] = 'X'
            self.num_mines -= 1

    def unmark_cell(self, row, col):
        if (row, col) in self.mine_positions:
            self.board[row][col] = ' '
            self.num_mines += 1

    def show_mines(self):
        for row, col in self.mine_positions:
            self.board[row][col] = 'M'

    def check_victory(self):
        for row in self.board:
            if 'M' in row:
                return
        self.is_game_over = True
        print('Congratulations! You won the game.')


    def get_valid_input(self, message):
        while True:
            try:
                value = int(input(message))
                if 0 <= value < self.size:
                    return value
                print('Invalid input! Please enter a valid value.')
            except ValueError:
                print('Invalid input! Please enter a valid integer.')

    def get_valid_action(self):
        while True:
            action = input('Enter action (open, mark, unmark): ').lower()
            if action in ['open', 'mark', 'unmark']:
                return action
            print('Invalid action! Please enter a valid action.')


size = int(input('Enter the size of the board: '))
while True:
    num_mines = int(input('Enter the number of mines: '))
    if num_mines <= ((size**2) // 2):
        break
    else:
        print(f"Invalid input! Please enter a valid value. (1 - {size**2 // 2})")


game = MinesweeperGame(size, num_mines)
initial_row = game.get_valid_input('Enter initial row (0 to {}): '.format(size - 1))
initial_col = game.get_valid_input('Enter initial column (0 to {}): '.format(size - 1))
game.initialize_board(initial_row, initial_col)
game.play()
