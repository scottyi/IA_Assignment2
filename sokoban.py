'''NAMES OF THE AUTHOR(S):
Scott IVINZA MBE
Jos ZIGABE '''
# coding: utf-8

import time
from utils import *
from search import *
from state import *
from copy import deepcopy


######################  Implement the search #######################
class Sokoban(Problem):
    """Contains the initial State"""
    
    nodes_explored = 0
    def __init__(self,init, goal):
        # Read goal grid 
        fg = open(goal, 'r')
        i = 0
        j = 0
        self.goal = []
        for line in fg:
            self.goal.append([])
            for word in line:
                for char in word:
                    if char != '\n' and char != '\r':
                        self.goal[i].append(char)
            i+=1
        fg.close()
        self.height = len(self.goal)
        self.width = len(self.goal[0])
        
        self.goals_coord = []
        for i in range(0, len(self.goal)):
            for j in range(0, len(self.goal[0])):
                if self.goal[i][j] == '.':
                    self.goals_coord.append([j, i])
                    
        self.grid_max_size = self.height*self.width
        # Get dead state pos
        self.get_dead_positions()
        
        # Read init grid and put it as initial State
        fi = open(init, 'r')
        i = 0
        j = 0
        grid = []
        for line in fi:
            grid.append([])
            for word in line:
                for char in word:
                    if char != '\n' and char != '\r':
                        grid[i].append(char)
            i+=1
        self.initial = State(grid, self.dead_pos)
        fi.close()
        


    def get_dead_positions(self):
        deadgrid = deepcopy(self.goal)
        self.mark_corners(deadgrid)
        self.mark_adjacent_h(deadgrid)
        self.mark_adjacent_v(deadgrid)
        self.dead_pos = deadgrid

###################################################
    def mark_corners(self, grid):
        # Check for positions that are in a corner 
        for x in range(0, self.width):
            for y in range(0, self.height):
                if grid[y][x] != '#' and grid[y][x] != '.':
                    # Mark corners as deadlock pos
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

####################################################
    def mark_adjacent_h(self, grid):
        for y in range(1, self.height-1 ):
            lineup = True
            linedown = True
            for x in range(0, self.width):
                if (grid[y-1][x] != '#' or grid[y-1][x]=='.' or grid[y][x] == '.'):
                    lineup = False
                if (grid[y+1][x] != '#' or grid[y+1][x]=='.' or grid[y][x] == '.'):
                    linedown = False
            if lineup or linedown:
                for x in range(0, self.width):
                    if grid[y][x] != '#':
                        grid[y][x] = '*'

#####################################################
    def mark_adjacent_v(self, grid):
        for x in range(1, self.width-1 ):
            liner = True
            linel = True
            for y in range(0, self.height):
                if (grid[y][x-1] != '#' or grid[y][x-1]=='.' or grid[y][x] == '.'):
                    liner = False
                if (grid[y][x+1] != '#' or grid[y][x+1]=='.' or grid[y][x] == '.'):
                    linel = False
            if linel or liner:
                for y in range(0, self.height):
                    if grid[y][x] != '#':
                        grid[y][x] = '*'

###################################################   
    def goal_test(self, state):
        for i in range(0, len(self.goal)):
            for j in range(0, len(self.goal[0])):
                if self.goal[i][j] == '.' and state.at(i,j) != '$':
                    return False
            j = 0
        return True

###################################################   
    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        # Find @ on grid
        y,x = state.find_man()
        new_states = []
        # Can go down ?
        if y + 1 < self.height and state.at(y+1, x) != '#':
            new_states.append(state.successor(x,y,"down"))

        # Can go up ?
        if y > 0 and state.at(y-1, x) != '#':
            new_states.append(state.successor(x,y,"up"))

        # Can go right ?
        if x +1 < self.width and state.at(y, x+1) != '#':
            new_states.append(state.successor(x,y,"right"))

        # Can go left ?
        if x > 0 and state.at(y, x-1) != '#':
            new_states.append(state.successor(x,y,"left"))
            
        for new_state in new_states:
            if new_state != None:
                new_state.calculate_cost(self.goals_coord)
                self.nodes_explored += 1
                yield("down", new_state)
                
    
###################################################
    def astar_graph_search(self):
        def h(n):
            return n.state.h
        return astar_graph_search(self, h)


###################### Launch the search #########################
problem=Sokoban(sys.argv[1], sys.argv[2])
node=problem.astar_graph_search()
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

