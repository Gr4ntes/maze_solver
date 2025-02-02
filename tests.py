import unittest

from maze_solver_main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )
    def test_maze_entrance(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[0][0].has_top)
    def test_maze_exit(self):  
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[num_cols - 1][num_rows - 1].has_bottom)
    def test_visited_reset(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.break_walls(0, 0)
        m1.reset_cell_visited()
        for i in range(m1.num_cols):
            for j in range(m1.num_rows):
                self.assertFalse(m1.cells[i][j].visited)

if __name__ == "__main__":
    unittest.main()

