#### BFS and DFS with GUI and PNG
import sys
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue
def close():
    sys.exit() #a function to be called in the gui to terminate the code when button exit is pushed

class Node(): # a class to define the node which have the state and parent and actions
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier(): #the state space of DFS which uses STACK (LIFO)
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node) #the nodes are put inside the frontier

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier") # the state which the stack is underflow
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    def remove(self): #this function overrides the stack frontier due to its nature when dealing with nodes
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():
    def __init__(self):
        pass
    def close(self):
        sys.exit()

    def openfile(self): # a function to be called in gui used to open file from any path on the device
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Mohamed\\PycharmProjects\\Main",
                                              title="please select a file ",
                                              filetypes=(("text files", "*.txt"),
                                                         ("all files", ".")))
        with open(filepath) as f:
            contents = f.read()

            # Validate start and goal
            if contents.count("A") != 1:
                raise Exception("maze must have exactly one start point")
            #exception will be raised if the maze has no goal
            if contents.count("B") != 1:
                raise Exception("maze must have exactly one goal")
            #exception will be raised if the maze has no goal

            # Determine height and width of maze
            contents = contents.splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            # Keep track of walls
            self.walls = []
            for i in range(self.height): # for loop to read the coordinates of the maze
                row = []
                for j in range(self.width):
                    try:
                        if contents[i][j] == "A":
                            self.start = (i, j)
                            row.append(False)
                        elif contents[i][j] == "B":
                            self.goal = (i, j)
                            row.append(False)
                        elif contents[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        row.append(False)
                self.walls.append(row)

            self.solution = None

    def dijkstra(self,m, *h, start=None):
        if start is None:
            start = (m.rows, m.cols)

        hurdles = [(i.position, i.cost) for i in h]

        unvisited = {n: float('inf') for n in m.grid}# x.grid uses for loop to list all cells of the maze
        unvisited[start] = 0
        visited = {}
        revPath = {} # a reverse path
        while unvisited:
            currCell = min(unvisited, key=unvisited.get) #while the dict is not empty the program will get the most minimum value of the cells according to cost
            visited[currCell] = unvisited[currCell]
            if currCell == m._goal: #the code will exit when the goal is found which is 1,1 always
                break
            for d in 'EWNS':
                if m.maze_map[currCell][d] == True: # to keep track of walls using a dict which stores the cell coordinates and the open direction of path
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    if childCell in visited: # the code will skip the child cell if it is visited before
                        continue
                    tempDist = unvisited[currCell] + 1 # the cost to move to the child cell which is one move away from the agent
                    for hurdle in hurdles:
                        if hurdle[0] == currCell: # checks if the hurdle is my current cell which will add the cost of it to the total cost
                            tempDist += hurdle[1]

                    if tempDist < unvisited[childCell]: # if the calculated cost is better than the old cost the child cell cost will be updated
                        unvisited[childCell] = tempDist
                        revPath[childCell] = currCell
            unvisited.pop(currCell) #the visited cell will be removed from the unvisited dict

        fwdPath = {}
        cell = m._goal
        while cell != start:
            fwdPath[revPath[cell]] = cell
            cell = revPath[cell]

        return fwdPath, visited[m._goal]

    def DK(self):
        window.destroy() # to end the window
        myMaze = maze(15, 15)#dimensions of the maze
        myMaze.CreateMaze(1, 4, loopPercent=10) # used to create the maze the loop percent means how many possible paths to goal


        h1 = agent(myMaze, 9, 4, color=COLOR.red)
        h2 = agent(myMaze, 2, 10, color=COLOR.red)
        h3 = agent(myMaze, 4, 7, color=COLOR.red) #hurdels that will narrow the possible paths of the maze by avoiding it
        h4 = agent(myMaze, 6, 2, color=COLOR.red)
        h5 = agent(myMaze, 1, 6, color=COLOR.red)

        h1.cost = 100
        h2.cost = 100
        h3.cost = 100
        h4.cost = 100
        h5.cost = 100


        path, c = self.dijkstra(myMaze, h1, h2, h3, h4, h5, start=(15, 15))

        textLabel(myMaze, 'Total Cost', c)# a label to present the cost of the maze


        a = agent(myMaze, 15, 15, color=COLOR.blue, filled=False, footprints=True) #the agent which takes the start position and color and its footprint values

        myMaze.tracePath({a: path})

        myMaze.run()


    def h(self,cell1,cell2):
        x1,y1=cell1
        x2,y2=cell2

        return abs(x1-x2) + abs(y1-y2) #returns the manhattan dist.
    def aStar(self,x):
        start=(x.rows,x.cols)
        g_score={cell:float('inf') for cell in x.grid}#every cell has g cost infinity except start point until it becomes a candidate or explored
        g_score[start]=0
        f_score={cell:float('inf') for cell in x.grid} #grid is a list that contains the coordinates of the cells of the maze
        f_score[start]=self.h(start,(1,1))
        #the priority queue is a special kind of datastructure that uses fifo but in our case the stored elements will come out based on their priority
        #in our case the priority will be for the nodes or tiles with the lowest cost
        open=PriorityQueue()
        open.put((self.h(start,(1,1)),self.h(start,(1,1)),start))
        #first value is F cost  which is  g+h but first cell has g=0
        # the previous line makes a tuple that takes the heuristics and the start cell itself and f cost of start cell
        aPath={}
        while not open.empty():
            """empty Return True if the queue is empty, False otherwise"""
            currCell=open.get()[2]# the 2 represents the index of the coordinates of the start cell
            if currCell==(1,1):
                break
                #if the cell is found to be the goal the loop will break and the code will end
            for d in 'ESNW':
                #for loop to explore any neighbours EAST SOUTH WEST NORTH
                #maze map is a dictionary that contains the cells and the possible cells after it based on directions
                if x.maze_map[currCell][d]==True:
                    if d=='E':
                        #if direction is east it means that the next cell or child cell will be on the right
                        childCell=(currCell[0],currCell[1]+1)
                    if d=='W':
                        childCell=(currCell[0],currCell[1]-1)
                    if d=='N':
                        childCell=(currCell[0]-1,currCell[1])
                    if d=='S':
                        childCell=(currCell[0]+1,currCell[1])

                    temp_g_score=g_score[currCell]+1#the new g score
                    temp_f_score=temp_g_score+self.h(childCell,(1,1))#f score of child cell

                    if temp_f_score < f_score[childCell]: #the condition where it compares the previous f score with current f score if it is true
                        #it means the agent is getting closer and the f score will be updated
                        g_score[childCell]= temp_g_score
                        f_score[childCell]= temp_f_score
                        #put used to put an element into the queue
                        open.put((temp_f_score,self.h(childCell,(1,1)),childCell))
                        aPath[childCell]=currCell #reversed path
        fwdPath={}
        cell=(1,1)
        while cell!=start:
            fwdPath[aPath[cell]]=cell
            cell=aPath[cell]
        return fwdPath

    def ASTAR(self):
        window.destroy()
        x = maze(15, 15)
        x.CreateMaze(loopPercent=60)
        path = self.aStar(x)

        a = agent(x, footprints=True)
        x.tracePath({a: path})
        l = textLabel(x, 'A Star Path Length', len(path) + 1)

        x.run()

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    #if condition used to replace the # with white blocks that makes the maze more visually accepted
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                    # if A is found then it will be printed as the start point
                elif (i, j) == self.goal:
                    print("B", end="")
                    # if B is found then it will be printed as the start point
                elif solution is not None and (i, j) in solution:
                    #if the solution exists and has coordinates it will be resembled as *
                    print("*", end="")
                else:
                    print(" ", end="")
                    #otherwise an empty path will be printed as white space
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier() #default BFS
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            #every node stores its parent and the action done to get to the cell
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()# to get the correct actions done from start to goal
                cells.reverse()# to get the correct cells done from start to goal
                self.solution = (actions, cells)
                return

            # Mark node as explored
            #if the node is not the goal it will be added as explored node
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    # if the neighbors are not explored before we will add it as a child cell
    def comb(self):
        # a fuction used to combine all functions of the program
        self.openfile()
        print("Maze:")
        self.print()
        print("Solving...")
        self.solve()
        print("States Explored:", self.num_explored)
        print("Solution:")
        self.print()
        self.output_image("maze.png", show_explored=True)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

m = Maze()
s = maze
window = Tk()


window.title("WELCOME !!! \n please select the maze to solve With BFS AND DFS")
window.geometry("700x700")
window.config(bg='#24f3f0')
button1 = Button(window, text="EXIT", command=close, background="#FF0000", width=15, height=5,font="gameplay 15")
button1.pack(pady=10)
button = Button(window, text="Open", command=m.comb, background="#3792CB", width=15, height=5,font="gameplay 15")
button.place(relx=0.9, rely=0.9, anchor=CENTER)
button2 = Button(window, text= "Dijkstra", command=m.DK, background="#3792CB", width=15, height=5,font="gameplay 15")
button2.place(relx=0.5, rely=0.57, anchor=CENTER)
button3 = Button (window, text = "ASTAR", command=m.ASTAR, background="#3792CB", width=15, height=5,font="gameplay 15")
button3.place(relx=0.5, rely=0.8, anchor=CENTER)
button.pack()
window.mainloop()