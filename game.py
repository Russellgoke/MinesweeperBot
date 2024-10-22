from concurrent.futures import process
import random

class Game:
    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.is_mine = False
            self.is_revealed = False
            self.is_flagged = False
            self.adjacent_mines = 0
    
    def __init__(self, settings, dispatcher):
        self.dispatcher = dispatcher
        self.width = settings.width
        self.height = settings.height
        self.num_mines = settings.num_mines
        self.total_cells = self.width * self.height
        self.cells_revealed = 0
        self.game_over = False
        self.cells = self.create_board()
        self.place_mines()
        self.calculate_adjacent_mines()

    def create_board(self):
        return [[self.Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    def place_mines(self):
        all_cells = [cell for row in self.cells for cell in row]
        mine_cells = random.sample(all_cells, self.num_mines)
        for cell in mine_cells:
            cell.is_mine = True

    def calculate_adjacent_mines(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine:
                    cell.adjacent_mines = self.count_adjacent_mines(cell)

    def count_adjacent_mines(self, cell):
        neighbors = self.get_neighbors(cell)
        return sum(1 for neighbor in neighbors if neighbor.is_mine)
    
    def count_adjacent_flags(self, cell):
        neighbors = self.get_neighbors(cell)
        return sum(1 for neighbor in neighbors if neighbor.is_flagged)

    def get_neighbors(self, cell):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        neighbors = []
        for dx, dy in directions:
            x2, y2 = cell.x + dx, cell.y + dy
            if 0 <= x2 < self.width and 0 <= y2 < self.height:
                neighbors.append(self.cells[y2][x2])
        return neighbors

    """
    Receives call from gui and processes click
    """
    def handle_click(self, x, y):
        cell = self.cells[y][x]
        self.process_click(cell)

    def process_click(self, cell):
        """
        Handles a click on the cell at position (x, y).

        Args:
            x (int): The x-coordinate of the clicked cell.
            y (int): The y-coordinate of the clicked cell.
        """
        if self.game_over:
            return

        if cell.is_revealed or cell.is_flagged:
            return
        
        if cell.is_mine:
            # The player has clicked on a mine - game over
            self.game_over = True
            self.dispatcher.dispatch('game_lost', (cell.x, cell.y))
            return
        
        cell.is_revealed = True
        self.cells_revealed += 1
        adjacent_flags = self.count_adjacent_flags(cell)
        if cell.adjacent_mines == adjacent_flags:
            # If the number ofadjacent cells equals number of flags, reveal adjacent cells
            self.reveal_adjacent_cells(cell)

        # check if the player has won
        if self.cells_revealed == (self.total_cells - self.num_mines):
            self.game_over = True
            self.dispatcher.dispatch('game_won', None)
        #TODO update percent alive
        self.dispatcher.dispatch('game_updated', cell)

    def reveal_adjacent_cells(self, cell):
        """
        Reveals adjacent cells.

        Args:
            cell (Cell): The cell to start revealing from.
        """
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if not neighbor.is_revealed and not neighbor.is_flagged:
                self.process_click(neighbor)