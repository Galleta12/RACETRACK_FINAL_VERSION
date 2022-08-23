import pygame
import time
from collections import deque

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

class Spot:
    def __init__(self, row, col, width, total_rows, value, type_spot):
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
        self.load_type(type_spot)
        
        

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
    
    def is_path(self):
        return self.color == PURPLE
    
    def load_type(self, type_spot):
        if type_spot == "#":
            self.make_barrier()
        elif type_spot == ".":
            self.make_out_bound()
    
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
def make_grid(rows, width, lines):
    grid = []
    gap = width // rows
    for i, line in enumerate(lines):
        grid.append([])
        for j, block in enumerate(line):
            spot = Spot(i, j, gap, rows, 0, block)
            grid[-1].append(spot)
   
    return grid

#this will draw the lines of the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width,car = None, car2 = None):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    myfonts = pygame.font.SysFont('Comic Sans MS', 30)
    myfontss = pygame.font.SysFont('Comic Sans MS', 18)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
    if car != None:
        car.draw_car(win)
        if car2 !=None:
            car2.draw_car(win)
        # x,y=car.get_velocity_spot()
        # textsurface = myfont.render("VelX: %s, VelY: %s"%(car.velx,car.vely), False, (0, 0, 0))
        # textsurfaces = myfonts.render("PosX: %s, PosY: %s"%(car.row,car.col), False, (0, 0, 0))
        # textsurfacess = myfontss.render("Moves%s"%(car.moves_car), True, (0, 0, 0))
        # win.blit(textsurface,(0,0))
        # win.blit(textsurfaces,(0,30))
        # win.blit(textsurfacess,(0,60))
    

    draw_grid(win, rows, width)
    pygame.display.update()


class Car(Spot):
    acceleration_options = [(dvx, dvy) for dvx in [-1, 0, 1] for dvy in [-1, 0, 1]]
    def __init__(self, row, col, width, total_rows, value,type_spot,grid,color_car,color_moves):
        super().__init__(row, col, width, total_rows, value,type_spot)
        self.row = row
        self.col = col
        self.velx = 0
        self.vely = 0
        self.color_car = color_car
        self.color_moves = color_moves
        self.moves_car = []
        self.moves_spot =[]
        self.state = ()
        self.list_state = []
        self.x = row * width
        self.y = col * width
        self.r = width // 2
        self.grid = grid
        self.pre_moves = []
        self.path_nodes = []
    def draw_car(self, win):
        # will draw the car and the possible moves
        pygame.draw.circle(win, self.color_car, (self.x +8 , self.y + 7), self.r)
        if self.moves_spot:
            for spot in self.moves_spot:
                if spot.get_pos() != self.get_pos():
                    pygame.draw.circle(win, self.color_moves, (spot.x +8 , spot.y + 7), self.r - 2)
     

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
    
    def automate_move(self,win,end):
        
        for spot in reversed(self.path_nodes):
            self.update(spot.row,spot.col)
            self.update_x_y_pos()
            self.draw_car(win)
            
               
            pygame.display.update()
            pygame.display.flip()
            time.sleep(0.5)
        
        self.update(end.row,end.col)
        self.update_x_y_pos()
        self.draw_car(win)
        pygame.display.update()
        pygame.display.flip()
    def automate_move_play(self,win,end):
        
        self.path_nodes = deque(self.path_nodes)
        current = self.path_nodes.pop()
        #print(current)
        self.update(current.row,current.col)
        self.update_x_y_pos()
        self.draw_car(win)
        
        pygame.display.update()
        pygame.display.flip()
        if not self.path_nodes:
            self.update(end.row,end.col)
            self.update_x_y_pos()
            self.draw_car(win)
            pygame.display.update()
            pygame.display.flip()

        
                   
    def save_path_nodes(self,path_nodes):
        self.path_nodes = path_nodes

                 
       
    
                        
                      
        
       
					
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
   