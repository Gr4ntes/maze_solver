from tkinter import Tk, Canvas, BOTH
import time
import random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root= Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)
    
    def wait_for_close(self):
        self.running = True
        while(self.running):
            self.redraw()
    
    def close(self):
        self.running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, top_left, bottom_right, win = None, has_top = True, has_right = True, has_bottom = True, has_left = True):
        self.x1 = top_left.x
        self.y1 = top_left.y
        self.x2 = bottom_right.x
        self.y2 = bottom_right.y
        self.has_top = has_top
        self.has_right = has_right
        self.has_bottom = has_bottom
        self.has_left = has_left
        self.win = win
        self.visited = False
    
    def draw(self):
        if self.has_top:
            self.win.draw_line(Line(Point(self.x1, self.y1), Point(self.x2, self.y1)))
        else:
            self.win.draw_line(Line(Point(self.x1, self.y1), Point(self.x2, self.y1)), "white")
        if self.has_right:
            self.win.draw_line(Line(Point(self.x2, self.y1), Point(self.x2, self.y2)))
        else:
            self.win.draw_line(Line(Point(self.x2, self.y1), Point(self.x2, self.y2)), "white")
        if self.has_bottom:
            self.win.draw_line(Line(Point(self.x1, self.y2), Point(self.x2, self.y2)))
        else:
            self.win.draw_line(Line(Point(self.x1, self.y2), Point(self.x2, self.y2)), "white")
        if self.has_left:
            self.win.draw_line(Line(Point(self.x1, self.y1), Point(self.x1, self.y2)))
        else:
            self.win.draw_line(Line(Point(self.x1, self.y1), Point(self.x1, self.y2)), "white")
    
    def draw_move(self, to_cell, undo=False):
        if undo:
            fill_color = "grey"
        else:
            fill_color = "red"

        self.win.draw_line(Line(Point(self.x1 + (self.x2 - self.x1) // 2, self.y1 + (self.y2 - self.y1) // 2), 
                           Point(to_cell.x1 + (to_cell.x2 - to_cell.x1) // 2, to_cell.y1 + (to_cell.y2 - to_cell.y1) // 2)), fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y  
        self.win = win
        self.cells = []
        self.create_cells()
    
    def create_cells(self):
        for i in range(self.num_cols):
            self.cells.append([])
            for j in range(self.num_rows):
                top_left = Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y)
                bottom_right = Point(self.x1 + (i + 1) * self.cell_size_x, self.y1 + (j + 1) * self.cell_size_y)
                self.cells[i].append(Cell(top_left, bottom_right, self.win))
    
    def draw(self):
        for col in self.cells:
            for cell in col:
                cell.draw()
    
    def break_entrance_and_exit(self): 
        self.cells[0][0].has_top = False
        if self.win:
            self.cells[0][0].draw()
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom = False
        if self.win:
            self.cells[self.num_cols - 1][self.num_rows - 1].draw()
    
    def break_walls(self, i, j):
        self.cells[i][j].visited = True
        while True:
            directions = []
            # can go left?
            if i > 0 and not self.cells[i-1][j].visited:
                directions.append([i-1, j])
            # can go up?
            if j > 0 and not self.cells[i][j-1].visited:
                directions.append([i, j-1])
            # can go right?
            if i < self.num_cols - 1 and not self.cells[i+1][j].visited:
                directions.append([i+1, j])
            # can go down?
            if j < self.num_rows - 1 and not self.cells[i][j+1].visited:
                directions.append([i, j+1])

            if len(directions) == 0:
                if self.win != None:
                    self.cells[i][j].draw()
                return
            
            num = random.randrange(len(directions))
            new_i = directions[num][0]
            new_j = directions[num][1]
            if new_i == i-1 and new_j == j:
                self.cells[i][j].has_left = False
                self.cells[new_i][new_j].has_right = False
            elif new_i == i and new_j == j-1:
                self.cells[i][j].has_top = False
                self.cells[new_i][new_j].has_bottom = False
            elif new_i == i+1 and new_j == j:
                self.cells[i][j].has_right = False
                self.cells[new_i][new_j].has_left = False
            elif new_i == i and new_j == j+1:
                self.cells[i][j].has_bottom = False
                self.cells[new_i][new_j].has_top = False
            
            if self.win != None:
                self.animate()
            self.break_walls(new_i, new_j)
            
    def reset_cell_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False
    
    def solve(self, i=0, j=0):
        self.animate()
        self.cells[i][j].visited = True
        if i == self.num_cols-1 and j == self.num_rows-1:
            return True

        if i > 0 and not self.cells[i-1][j].visited and not self.cells[i][j].has_left:
            self.cells[i][j].draw_move(self.cells[i-1][j])
            result = self.solve(i-1, j)
            if result == True:
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i-1][j], undo=True)
        if j > 0 and not self.cells[i][j-1].visited and not self.cells[i][j].has_top:
            self.cells[i][j].draw_move(self.cells[i][j-1])
            result = self.solve(i, j-1)
            if result == True:
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j-1], undo=True)
        if i < self.num_cols - 1 and not self.cells[i+1][j].visited and not self.cells[i][j].has_right:
            self.cells[i][j].draw_move(self.cells[i+1][j])
            result = self.solve(i+1, j)
            if result == True:
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i+1][j], undo=True)
        if j < self.num_rows - 1 and not self.cells[i][j+1].visited and not self.cells[i][j].has_bottom:
            self.cells[i][j].draw_move(self.cells[i][j+1])
            result = self.solve(i, j+1)
            if result == True:
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j+1], undo=True)   

        return False


    def animate(self):
        self.win.redraw()
        self.draw()
        time.sleep(0.05)


win = Window(800, 600)
maze = Maze(50, 50, 10, 14, 50, 50, win)
maze.break_entrance_and_exit()
maze.break_walls(0, 0)
maze.reset_cell_visited()
maze.draw()
maze.solve()
win.wait_for_close()