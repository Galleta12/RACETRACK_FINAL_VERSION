import pygame
import math
from queue import PriorityQueue
import csv
import pandas as pd
import os
#this is the one that will draw the barriers
from trail_track import draw_tracks
#from trail_track_2 import draw_tracks
#this will draw the spots that are outside the track
#you can comment this ans use the version 2 to change to another barrier
from bound import limit_bound
#from bound_2 import limit_bound
from alg import algorithm, breadth_first_search
import random

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Racetrack")

#the class of each square
class Spot:
    def __init__(self, row, col, width, total_rows, value):
        self.value = value
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = GREEN
        self.neighbors = []
        self.neighbors_pos = []
        self.width = width
        self.total_rows = total_rows
        self.out_bound = []
        self.vx_spot= 0
        self.vy_spot=0
        

    def get_value(self):
        return self.value
    def get_velocity_spot(self):
        return [self.vx_spot,self.vy_spot]
    def set_velocity_spot(self, pos_x, pos_y,new_x, new_y):
        self.vx_spot = new_x-pos_x
        self.vy_spot = new_y - pos_y

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_car(self):
        return self.color == BLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_make_possible(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == GOLD

    def reset(self):
        self.value = 0
        self.color = WHITE

    def make_possible(self):
        if self.value != 1:
            self.color = ORANGE
        else:
            self.color = BLUE
    def is_out_bound(self):
        return self.color == WHITE
    def make_out_bound(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_car(self):
        self.color = BLUE

    def make_open(self):
        self.color = MAGENTA

    def is_open(self):
        return self.color == MAGENTA

    def make_barrier(self):
        self.value = 1
        self.color = BLACK

    def make_end(self):
        self.color = GOLD

    def make_path(self):
        self.color = PURPLE

    def draw_track(self, grid):
        draw_tracks(grid)
    
        
        for spot in limit_bound(grid):
            spot.make_out_bound()
 

    def draw(self, win):

        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))
    
    
    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        
   
    def update_possible_path(self, grid):
        for x in range(len(grid)):
            for j in range(len(grid)):
                if grid[x][j].is_make_possible():
                    grid[x][j].reset()

    def update_car_line(self, grid):
        for x in range(len(grid)):
            for j in range(len(grid)):
                if grid[x][j].get_value() == 5:
                    grid[x][j].reset()

    def __lt__(self, other):
        return False

#this will create my 2d array for the grid and also create all the objects
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows, 0)
            grid[i].append(spot)
    spot.draw_track(grid)
    return grid

#this will draw the lines of the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#this will draw the car and the spots
def draw(win, grid, rows, width,car = None):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    myfonts = pygame.font.SysFont('Comic Sans MS', 30)
    myfontss = pygame.font.SysFont('Comic Sans MS', 18)
    
    
    #win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    #just to check if the car exits and to print messages, however that is not important now
    if car != None:
        car.draw_car(win)
        x,y=car.get_velocity_spot()
        textsurface = myfont.render("VelX: %s, VelY: %s"%(car.velx,car.vely), False, (0, 0, 0))
        textsurfaces = myfonts.render("PosX: %s, PosY: %s"%(car.row,car.col), False, (0, 0, 0))
        textsurfacess = myfontss.render("Moves%s"%(car.moves_car), True, (0, 0, 0))
        win.blit(textsurface,(0,0))
        win.blit(textsurfaces,(0,30))
        win.blit(textsurfacess,(0,60))
 
    draw_grid(win, rows, width)
    pygame.display.update()

#get the position of the grid when u click on it
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


class Car(Spot):
    acceleration_options = [(dvx, dvy) for dvx in [-1, 0, 1] for dvy in [-1, 0, 1]]
    def __init__(self, row, col, width, total_rows, value,grid):
        super().__init__(row, col, width, total_rows, value)
        self.row = row
        self.col = col
        self.velx = 0
        self.vely = 0
        self.moves_car = []
        self.moves_spot =[]
        self.state = ()
        self.list_state = []
        self.x = row * width
        self.y = col * width
        self.r = width // 2
        self.grid = grid
        self.pre_moves = []
    def draw_car(self, win):
        # will draw the car and the possible moves
        pygame.draw.circle(win, GREEN, (self.x +8 , self.y + 7), self.r)
        if self.moves_spot:
            for spot in self.moves_spot:
                if spot.get_pos() != self.get_pos():
                    pygame.draw.circle(win, ORANGE, (spot.x +8 , spot.y + 7), self.r - 2)
     

    #update the position of the car           
    def update_x_y_pos(self):
        self.x = self.row * self.width
        self.y = self.col * self.width       
        
    # get the new moves
    def moves(self):
        self.list_state = []
        self.moves_car = []
        self.moves_spot = []
        self.state = (self.row,self.col,self.velx,self.vely)
        state = {self.state}
        for x,y,vx,vy in  state:
            for dvx, dvy in self.acceleration_options:
                new_vx, new_vy = vx+dvx, vy+dvy
                new_x, new_y = x+new_vx, y+new_vy
                if new_x < self.total_rows   and new_y < self.total_rows :
                    if  not self.grid[new_x][new_y].is_barrier() and  self.grid[new_x][new_y].color!= GREEN or self.grid[new_x][new_y].is_end():
                        self.list_state.append([new_x, new_y, new_vx, new_vy])
                        self.moves_car.append([new_x,new_y])
                        self.moves_spot.append(self.grid[new_x][new_y])
    # this will get the new moves, depending on the spot object
    def moves_for_spot(self,new_spot):
        self.list_state = []
        self.moves_car = []
        self.moves_spot = []
        vxx, vyy = new_spot.get_velocity_spot()
        self.state = (new_spot.row,new_spot.col,vxx, vyy)
        state = {self.state}
        for x,y,vx,vy in  state:
            for dvx, dvy in self.acceleration_options:
                new_vx, new_vy = vx+dvx, vy+dvy
                new_x, new_y = x+new_vx, y+new_vy
                if new_x < self.total_rows   and new_y < self.total_rows :
                    if  not self.grid[new_x][new_y].is_barrier() and  self.grid[new_x][new_y].color!= GREEN or self.grid[new_x][new_y].is_end():
                        self.list_state.append([new_x, new_y, new_vx, new_vy])
                        self.moves_car.append([new_x,new_y])
                        self.moves_spot.append(self.grid[new_x][new_y])
    
                        
                      
        
       
					
    def get_moves(self):
        return self.moves_car
    def update(self,row,col):
        self.row = row
        self.col = col
        for x,y, vx, vy in self.list_state:
            if [self.row, self.col] == [x,y]:
                self.velx = vx
                self.vely = vy
        self.state = (self.row, self.col, self.velx, self.vely)
    def update_pos(self,row,col):
        self.row = row
        self.col = col
       
    def velocity(self):
        pass
    def radar(self):
        pass
    def radar_moves(self):
        pass
    def prev_moves(self):
        self.pre_moves.append([self.row,self.col,self.velx,self.vely])
        self.grid[self.row][self.col].make_path()
    def validate(self,row,col):
        if [row, col] in self.moves_car:
            return True
        return False
   
            
				
		
		
		
        
	
		
    

    


   


def main():
   
    clock = pygame.time.Clock()
    ROWS = 48
    grid = make_grid(ROWS, WIDTH)
    
    gap = WIDTH // ROWS
    start = None
    end = None
    car = None
    prex= 0
    prey=0
    run = True
    while run:
        clock.tick(100)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                #spot.make_out_bound()
                end = spot
                end.make_end()
                #print("barrier_list.append(grid[%s][%s])" % (row, col))
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                new_spot= grid[row][col]
                if not car:
                    prex=row
                    prey=col
                    car = Car(row, col, gap, ROWS, 5,grid)
                    car.moves()
                    car.prev_moves()
                    spot = grid[row][col]
                    start = spot
                    start.make_car()
                    
                    
                elif car != None and car.validate(row,col):
                    
                    car.update(row,col)
                    #car.set_velocity_spot(prex,prey,row,col)
                    car.update_x_y_pos()
                    car.moves()
                    #car.moves_for_spot(new_spot)
                    car.prev_moves()
                    prex=row
                    prey=col
                    print(car.pre_moves)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    #algorithm(lambda: draw(WIN, grid, ROWS,WIDTH),grid, start, end,car)
                    breadth_first_search(lambda: draw(WIN, grid, ROWS,WIDTH),grid, start, end,car)
						    
					
       
        if car != None:
            draw(WIN, grid, ROWS, WIDTH,car)
        else:
            draw(WIN, grid, ROWS,WIDTH)
       
        pygame.display.update()

                            		
    pygame.quit()



main()
