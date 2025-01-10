import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[11]),
            num_rows,
        )
        self.assertEqual(
            m1.cell_size_x,
            10,
        )

    def test_maze_visited_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        all_false = False
        for cells in m1._cells:
            for cell in cells:
                if cell.visited:
                    all_false = True
        self.assertEqual(
            all_false,
            False
        )

if __name__ == "__main__":
    unittest.main()