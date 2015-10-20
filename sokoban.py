'''NAMES OF THE AUTHOR(S):
Scott IVINZA MBE
Jos ZIGABE '''
# coding: utf-8

import time
from utils import *
from search import *
from state import *
from copy import deepcopy


# Sokoban class
class Sokoban(Problem):

    
    nodes_visited = 0
    def __init__(self,init_state, goal_state):
        # Read goal grid 
        file_goal = open(goal_state, 'r')
        i = 0
        j = 0
        self.goal_state = []
        for line in file_goal:
            self.goal_state.append([])
            for string in line:
                for char in string:
                    if char != '\n' and char != '\r':
                        self.goal_state[i].append(char)
            i+=1
        file_goal.close()
        self.height = len(self.goal_state)
        self.width = len(self.goal_state[0])
        
        self.goals_coord = []
        for i in range(0, len(self.goal_state)):
            for j in range(0, len(self.goal_state[0])):
                if self.goal_state[i][j] == '.':
                    self.goals_coord.append([j, i])
                    
        self.grid_max_size = self.height*self.width
        # Get dead state pos
        self.get_dead_positions()
        
        # Read init grid and put it as initial State
        file_init = open(init_state, 'r')
        i = 0
        j = 0
        grid = []
        for line in file_init:
            grid.append([])
            for string in line:
                for char in string:
                    if char != '\n' and char != '\r':
                        grid[i].append(char)
            i+=1
        self.initial = State(grid, self.dead_pos)
        file_init.close()
        

    # return no-go zone (deadlock)
    def get_dead_positions(self):
        deadgrid = deepcopy(self.goal_state)
        self.mark_corners(deadgrid)
        self.mark_adjacent_h(deadgrid)
        self.mark_adjacent_v(deadgrid)
        self.dead_pos = deadgrid


    # Check for positions that are in a corner
    # Otherwise the avatar can not move the boxe
    def mark_corners(self, grid):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if grid[y][x] != '#' and grid[y][x] != '.':
                    # Mark corners as deadlock position
                    if x == 0 or y == 0 or x == self.width -1 or y == self.height - 1:
                        grid[y][x] = '*'
                    # Mark empty cells that are between 3 walls (horizontally)
                    elif ((x > 0 and grid[y][x-1]=='#') or (x - 1 < self.width and grid[y][x+1] == '#')) and \
                    ((y > 0 and grid[y-1][x] == '#') or (y-1 < self.height and grid[y+1][x] == '#')):
                        grid[y][x] = '*'
                    # Mark empty cells that are between 3 walls (vertically)
                    elif ((y> 0 and grid[y-1][x] == '#') or (y - 1 < self.height and grid[y+1][x] == '#')) and \
                    ((x>0 and grid[y][x-1] == '#') or (x-1 < self.width and grid[y][x+1] == '#')):
                        grid[y][x] = '*'


    # Check if the cell is in a corridor horinzally
    def mark_adjacent_h(self, grid):
        for y in range(1, self.height-1 ):
            line_up = True
            line_down = True
            for x in range(0, self.width):
                if (grid[y-1][x] != '#' or grid[y-1][x]=='.' or grid[y][x] == '.'):
                    line_up = False
                if (grid[y+1][x] != '#' or grid[y+1][x]=='.' or grid[y][x] == '.'):
                    line_down = False
            if line_up or line_down:
                for x in range(0, self.width):
                    if grid[y][x] != '#':
                        grid[y][x] = '*'


    # Check if the cell is a corridor vertcal manner
    def mark_adjacent_v(self, grid):
        for x in range(1, self.width-1 ):
            line_right = True
            line_left = True
            for y in range(0, self.height):
                if (grid[y][x-1] != '#' or grid[y][x-1]=='.' or grid[y][x] == '.'):
                    line_right = False
                if (grid[y][x+1] != '#' or grid[y][x+1]=='.' or grid[y][x] == '.'):
                    line_left = False
            if line_left or line_right:
                for y in range(0, self.height):
                    if grid[y][x] != '#':
                        grid[y][x] = '*'


    # Test if the goal_state is reached.
    def goal_test(self, state):
        for i in range(0, len(self.goal_state
                              )):
            for j in range(0, len(self.goal_state[0])):
                if self.goal_state[i][j] == '.' and state.at(i,j) != '$':
                    return False
            j = 0
        return True

    """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
    def successor(self, state):
        # Find @ on grid
        y,x = state.find_man()
        new_states = []
        # Check if he can go down.
        if y + 1 < self.height and state.at(y+1, x) != '#':
            new_states.append(state.successor(x,y,"down"))

        # Check if he can go up.
        if y > 0 and state.at(y-1, x) != '#':
            new_states.append(state.successor(x,y,"up"))

        # Check if ha can go right.
        if x +1 < self.width and state.at(y, x+1) != '#':
            new_states.append(state.successor(x,y,"right"))

        # Check if he can go left.
        if x > 0 and state.at(y, x-1) != '#':
            new_states.append(state.successor(x,y,"left"))
            
        for new_state in new_states:
            if new_state != None:
                new_state.calculate_cost(self.goals_coord)
                self.nodes_visited += 1
                yield("down", new_state)
                
    

    # Execute a* search on a graph
    def astar_graph_search(self):
        def h(n):
            return n.state.h
        return astar_graph_search(self, h)


# Launch the search
problem=Sokoban(sys.argv[1], sys.argv[2])
node=problem.astar_graph_search()
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

