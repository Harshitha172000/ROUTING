#!/usr/bin/env python
# coding: utf-8

#   #      MAZE ROUTING - HADLOCK'S ALGORITM 
# 

# In[37]:


get_ipython().system('pip install pygame')


# In[38]:


import pygame
from pygame.locals import *
from queue import PriorityQueue
#pygame.init()


#     Class node which corresponds to single rectangle in a grid, holds the node(pixel) information like its dimensions,color         and its neighbors. 

# In[39]:


class node:
    
    def __init__(self, x, y, gap):
        
        self.row = x                           
        self.col = y
        self.width= gap
        self.color=(255, 255, 255)
        self.neighbors=[]
    
        
    def get_pos(self):
        return self.row//self.width, self.col//self.width
    
    def make_block(self):
        self.color=pygame.Color('cyan')
      
    def is_barrier(self):
        return (self.color == pygame.Color('cyan') or self.color ==pygame.Color("yellow"))
    
    def is_open(self):
        return self.color == pygame.Color('white')
    
    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.row, self.col, self.width, self.width))
        
    def addtext(self, text_):
        pygame.font.init()
        font = pygame.font.Font('freesansbold.ttf', 10)
        text = font.render(text_, True, (0,0,0), self.color)
        
        WIN.blit(text, (self.row, self.col, self.width+self.row, self.col+self.width))
        pygame.display.update()



#    Class grid_: It forms connection between grid lines and nodes which helps in accessing all nodes

# In[40]:


class grid_:
    
    def __init__(self,  rows, width):
        self.gap = width//rows
        self.rows= rows
        self.width = width
        self.gap = self.width // self.rows
        
    def form(self):
        grid= []
       
        for i in range(0,self.rows):
            grid.append([])
            for j in range(0, self.rows):
            
                grid[i].append(node(i*self.gap,j*self.gap, self.gap))
        return grid
                


#    Some parameters that can be varied to change pygame screen settings

# In[41]:


WIDTH= 600                       ## WIDTH of pygame GUI screen
rows_=40                          ## Number of rows in grid
axis=3                          ##Setting axis so that output appears at the centre of pygame screen


#   Module create_block : Given coordinates and dimensions of block, colors rectangles inside that block so that they can be identified as obstacles or barrier.

# In[42]:



def create_block(x, y, w, h, gap, grid):
    
    
    for i in list(range(x+axis, (x+w+axis))):
 for j in list(range(y+axis, y+h+axis)):
    
    grid[i][j].make_block()
    
    


# Module draw_grid : Draws grid lines on pygame screen

# In[43]:


def draw_grid(win, rows, width):
    gap = width // rows
    
    for i in range(rows):
        pygame.draw.line(win, pygame.Color('GREY'), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, pygame.Color('GREY'), (j * gap, 0), (j * gap, width))


# draw : Very important module, it displays all blocks, pins and path.

# In[44]:


def draw(win, grid, rows, width):
    

    for row in range(0, rows):
        for spot in range(0,rows):
        
            grid[row][spot].draw()

    draw_grid(win, rows, width)
    pygame.display.update()


# create_pins : Adds identification color to pins (i.e, nodes that acts as pins ) 

# In[45]:



def create_pins(x1,y1,x2,y2,grid,i):

start=grid[x1+axis][y1+axis]
grid[x1+axis][y1+axis].color = pygame.Color('green')

end = grid[x2+axis][ y2+axis]
grid[x2+axis][y2+axis].color = pygame.Color('green')

return start, end


# update_neighbors : Updates each neighbor, giving information whether its neighbors are blocks or a node which is part of already existing path. 

# In[46]:



def update_neighbors(row,col, grid):
        neighbors = []
        
        if (0 < row < len(grid[0])) and not grid[row + 1][col].is_barrier():  # DOWN
            neighbors.append(grid[row + 1][col])

        if row > 0 and not grid[row - 1][col].is_barrier(): #UP
            neighbors.append(grid[row - 1][col])

        if 0<col < len(grid[0]) and not grid[row][col + 1].is_barrier(): #RIGHT
            neighbors.append(grid[row][col + 1])

        if col > 0 and not grid[row][col - 1].is_barrier(): #LEFT
            neighbors.append(grid[row][col - 1])
       
        return neighbors


#    ALGORITHM MODULE AND ITS HELPER MODULES

# In[47]:



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    color = pygame.Color("yellow")
    wirelength=0   
    while current in came_from:
        current = came_from[current]
        current.color = color
        wirelength+=1
        draw()
    return wirelength

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {};

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    wirelength=0
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()

        current = open_set.get()[2]
        x, y = current.get_pos()
        neighbors=[]
        current.neighbors = update_neighbors(x, y, grid)
        open_set_hash.remove(current)

        if current == end:
            end.color = pygame.Color("yellow")
            wirelen=reconstruct_path(came_from, end, draw)
            
            return wirelen, came_from

        for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                     came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
        draw()       
         
   # return 0, 0
        
      


# In[48]:



WIN = pygame.display.set_mode((WIDTH, WIDTH), pygame.RESIZABLE)
pygame.display.set_caption("Hadlock's Routing Algorithm")
WIN.fill(pygame.Color('WHITE'))

def main(win):
    rows=rows_;
    gri = grid_(rows, WIDTH)
    grid = gri.form()
    gap = WIDTH//rows
    draw(win, grid, rows, WIDTH)
    
    #############################################################################
    ##              Given test data inputs of blocks                           ##
    ##                 Can modify blocks or pins                               ##
    #############################################################################
    
    blocks = [[1, 0, 0, 7, 9],
              [2, 11,8, 6, 8],
              [3, 0, 23, 16, 6]]
              #[4, 20,20,7,8]]
    
    
      
    pins = [[1, 7, 0, 11, 12],
            [2, 14, 8, 1, 9],
            [3, 1, 23, 16, 24],
            [4, 14, 16, 8, 29],
            [5, 1, 29, 17, 12]]
            #[6, 21,20, 27,27]
    
    #############################################################################
    
    
    ######################### Creating Blocks on Pygame Screen ########################
    
    for i in range(len(blocks)):
        create_block(blocks[i][1], blocks[i][2], blocks[i][3], blocks[i][4], gap, grid)
    draw(win, grid, rows, WIDTH)
    
    ######################### Analysing Pin Information ###############################
    
    start =[None]*len(pins)
    end = [None]*len(pins)
    for i in range(len(pins)):
        start[i], end[i] = create_pins(pins[i][1],pins[i][2], pins[i][3], pins[i][4], grid, i)    
    draw(win, grid, rows, WIDTH)
    
        
    wirelen =[None]*len(pins)
    wirelength =[None]*len(pins)
    path={}
    k={}
    ######################## Calling algorithm to form path ###########################
    
    for i in range(len(pins)):
        
        wirelength[i], path[i]=algorithm(lambda: draw(win, grid, rows, WIDTH), grid, start[i], end[i])
        
    draw(win, grid, rows, WIDTH)
    
    #####################    NAMING BLOCK ID'S, PIN ID'S AND NET ID'S ##################################
    
    for i in range(len(blocks)):
        grid[blocks[i][1]+axis+(blocks[i][3]//2)][blocks[i][2]+axis+(blocks[i][4]//2)].addtext('B'+str(blocks[i][0])+' ('+str(blocks[i][3])+','+str( blocks[i][4])+')')
    
       
    for i in range(len(pins)):
        current=end[i]
        
        while current in path[i]:
            current=path[i][current]
            current.addtext('N'+str(pins[i][0]))
    
    for i in range(len(pins)):
        start[i].color = pygame.Color('green')
        end[i].color = pygame.Color('green')
        start[i].draw()
        end[i].draw()
        start[i].addtext('P'+str(pins[i][0]))
        end[i].addtext('P'+str(pins[i][0]))
     
 
    print ('Pin Ids : Netlength' )
    for i in range(len(pins)):
        print( str(pins[i][0])+'       : '+str(wirelength[i])+' units')
   
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    pygame.quit()  
main(WIN)


# In[ ]:





# 
# NOTE: Pygame display has (0,0) at top right corner. 
# 
# I have set axis=3 which shifts blocks to 3 units right and 3 units down. This is done to observe blocks at center of display.  
# 
# 

# In[ ]:





# In[ ]:




