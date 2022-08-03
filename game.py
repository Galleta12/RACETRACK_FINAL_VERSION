import pygame

import matrix

class Game():
    ROWS = 50
    def __init__(self, width):
        self.color_game = (0, 255, 0)
        self.grid = []
        self.width = width
        self.lines = []
        self.map_names = None
        self.end = None
        self.car = None
        self.gap= 0

    def draw_game(self,win, map):
        if map == "map1" and self.grid == []:
            self.map_names = "Basic_curve"
            self.load_map()
           
        
        
        self.run_game(win,self.grid,self.width)
    def run_game(self,win,grid, width):
        if self.car != None:
            matrix.draw(win,grid,self.ROWS, width,self.car)
        else:
            matrix.draw(win,grid,self.ROWS, width)
    
    def game_event(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
				
            
            if pygame.mouse.get_pressed()[0] :# LEFT
                pos = pygame.mouse.get_pos()
                row, col = self.get_clicked_pos(pos, self.ROWS, self.width)
                spot = self.grid[row][col]
                self.end = spot
                print(self.end.row,"col",self.end.col)
                self.end.make_end()
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = self.get_clicked_pos(pos, self.ROWS, self.width)
                if not self.car:
                    self.car = matrix.Car(row,col,self.gap,self.ROWS,5,"car",self.grid)
                    self.car.moves()
                    self.car.prev_moves()
                    spot = self.grid[row][col]
                    start = spot
                    start.make_car()
                elif self.car != None and self.car.validate(row,col):
                    self.car.update(row,col)
                    #car.set_velocity_spot(prex,prey,row,col)
                    self.car.update_x_y_pos()
                    self.car.moves()
                    #car.moves_for_spot(new_spot)
                    self.car.prev_moves()




    def get_clicked_pos(self,pos, rows, width):
        self.gap = width // rows
        y, x = pos

        row = y // self.gap
        col = x // self.gap

        return row, col
        
    def load_map(self):
        with open(f"{self.map_names}.txt","r") as file: # Reading from file named given argument
            lines = ["".join(i.split()) for i in file.readlines()]
        self.lines = lines
        self.grid = matrix.make_grid(self.ROWS, self.width, lines)
        print("Grid done")
                   
        


		
