from cell import Cell
from graphics import Window
import time
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self.seed = seed

        if self.seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self._break_entrance_and_exit()

    
    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        # Top-left corner
        x1 = self._x1 + (j * self.cell_size_x)
        y1 = self._y1 + (i * self.cell_size_y)
        
        # Bottom-right corner
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        # Draw the cell
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _break_entrance_and_exit(self):
            self._cells[0][0].has_top_wall = False
            self._draw_cell(0, 0)
            self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
            self._draw_cell(self.num_cols-1, self.num_rows-1)

 

    def _reset_cells_visited(self):
        for cells in self._cells:
            for cell in cells:
                cell.visited = False



    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        # i is cols, and j is rows

        while True:

            to_visit = []
            # Check North
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            # South
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            # East
            if j < self.num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            # West
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            random_index_num = random.randrange(len(to_visit))
            chosen_direction = to_visit[random_index_num]

            # its moving North
            if chosen_direction == (i-1,j):
                self._cells[i][j].has_top_wall = False
                self._cells[i-1][j].has_bottom_wall = False

            # its moving South  
            if chosen_direction == (i+1,j):
                self._cells[i][j].has_bottom_wall = False
                self._cells[i+1][j].has_top_wall = False

            # its moving East  
            if chosen_direction == (i,j+1):
                self._cells[i][j].has_right_wall = False
                self._cells[i][j+1].has_left_wall = False
            # its moving West     
            if chosen_direction == (i,j-1):
                self._cells[i][j].has_left_wall = False
                self._cells[i][j-1].has_right_wall = False

            self._break_walls_r(chosen_direction[0], chosen_direction[1])

    
    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j].visited = True
        
        end_cell = self._cells[self.num_cols-1][self.num_rows-1]

        if self._cells[i][j] == end_cell:
            return True
        
        
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        for direction in directions:
            new_i = i + direction[0]
            new_j = j + direction[1]

            if 0 <= new_i < self.num_cols and 0 <= new_j < self.num_rows: #make sure not out of bounds
                can_move = False
                if direction == [0, 1]:  # East (increase row)
                    can_move = not self._cells[i][j].has_right_wall
                elif direction == [1, 0]:  # South (increase col)
                    can_move = not self._cells[i][j].has_bottom_wall
                elif direction == [0, -1]:  # West (decrease row)
                    can_move = not self._cells[i][j].has_left_wall
                elif direction == [-1, 0]:  # North (decrease col)
                    can_move = not self._cells[i][j].has_top_wall

                if can_move and not self._cells[new_i][new_j].visited:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    self._cells[i][j].draw_move(self._cells[new_i][new_j],True)
        return False

    
    def _animate(self):         
        if self._win is None:
            return
        time.sleep(0.005)
        self._win.redraw()

