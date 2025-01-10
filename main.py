from graphics import Window, Line, Point
from cell import Cell
from maze import Maze


def main():
    win = Window(800, 600)


    num_cols = 12
    num_rows = 16
    m1 = Maze(10, 10, num_rows, num_cols, 40, 40, win)
    m1.solve()

    win.wait_for_close()


main()


