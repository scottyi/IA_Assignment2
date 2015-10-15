from copy import deepcopy
import math
from utils import *

class State:
    def __init__(self, grid, dead_pos):
        self.grid = grid
        self.dead_pos = dead_pos
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.h = 0 # Estimated cost from Heuristic

###########################################       
    def __hash__(self):
        s = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                s+=self.grid[y][x]
        return hash(s)
            

###########################################       
    def __eq__(self, state):
        return hash(self) == hash(state)

###########################################       
    def __str__(self):
        s = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                s+=self.grid[y][x]
            s+='\n'
        return s
            
        
###########################################       
    def successor(self, x, y, action):
        new_state = State(deepcopy(self.grid), self.dead_pos)
        if action == "up":
            return self.move_up(x,y, new_state)
        elif action == "down":
            return self.move_down(x,y, new_state)
        elif action == "right":
            return self.move_right(x,y, new_state)
        elif action == "left":
            return self.move_left(x,y, new_state)
    
###########################################  
        
    def move_up(self, x, y, new_state):
        if new_state.grid[y-1][x] == '$':
            if y - 1 > 0 and new_state.grid[y-2][x] == ' ' and self.dead_pos[y-2][x] != '*':
                new_state.grid[y-2][x] = '$'
                new_state.grid[y-1][x] = '@'
                new_state.grid[y][x] = ' '
            else:
                return None
        elif new_state.grid[y-1][x] == ' ':
            new_state.grid[y-1][x] = '@'
            new_state.grid[y][x] = ' '
        else:
            return None
        return new_state

###########################################    
        
    def move_down(self, x,y, new_state):
        if new_state.grid[y+1][x] == '$':
            if y + 1 <  self.height and new_state.grid[y+2][x] == ' ' and self.dead_pos[y+2][x] != '*':
                new_state.grid[y+2][x] = '$'
                new_state.grid[y+1][x] = '@'
                new_state.grid[y][x] = ' '
            else:
                return None
        elif new_state.grid[y+1][x] == ' ':
            new_state.grid[y+1][x] = '@'
            new_state.grid[y][x] = ' '
        else:
            return None
        return new_state

###########################################  
        
    def move_left(self, x,y, new_state):
        if new_state.grid[y][x-1] == '$':
            if x - 1 > 0 and new_state.grid[y][x-2] == ' ' and self.dead_pos[y][x-2] != '*':
                new_state.grid[y][x-2] = '$'
                new_state.grid[y][x-1] = '@'
                new_state.grid[y][x] = ' '
            else:
                return None
        elif new_state.grid[y][x-1] == ' ':
            new_state.grid[y][x-1] = '@'
            new_state.grid[y][x] = ' '
        else:
            return None
        return new_state

###########################################     

    def move_right(self, x, y, new_state):
        if new_state.grid[y][x+1] == '$':
            if x + 1 <  self.width and new_state.grid[y][x+2] == ' ' and self.dead_pos[y][x+2] != '*':
                new_state.grid[y][x+2] = '$'
                new_state.grid[y][x+1] = '@'
                new_state.grid[y][x] = ' '
            else:
                return None
        elif new_state.grid[y][x+1] == ' ':
            new_state.grid[y][x+1] = '@'
            new_state.grid[y][x] = ' '
        else:
            return None
        return new_state

###########################################
    
    # Returns the cells containing a block
    def get_blocks(self):
        blocks = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                if self.grid[y][x] == "$":
                    blocks.append([x, y])
        return blocks
    
    # Calculate the sum of the costs from blocks to goals, and save it in state.h for further use
    def calculate_cost(self, goals):
        blocks = self.get_blocks()
        total_cost = 0
        
        for b in range(0, len(blocks)):
            total_cost += self.cost(blocks[b][0], blocks[b][1], goals[b][0], goals[b][1])
            
        self.h = total_cost
    
    # Euclidien cost between two different cells
    def cost(self, start_x, start_y, goal_x, goal_y):
        return math.ceil(math.sqrt((start_x - goal_x)**2 + (start_y - goal_y)**2))

        
###########################################     
    def find_man(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if self.at(i,j) == '@':
                    return (i,j)


    def at(self, y, x):
        return self.grid[y][x]

