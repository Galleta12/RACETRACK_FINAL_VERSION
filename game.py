import pygame

import matrix
import alg
import versus

class Game():
    ROWS = 50
    def __init__(self, width):
        self.color_game = (0, 255, 0)
        self.grid = []
        self.width = width
        self.lines = []
        self.map_names = None
        self.end = None
        self.start = None
        self.car = None
        self.gap= 0
        self.win = None
        self.type_alg = None
        self.car2= None

    
    def save_map(self,win, map):
        self.win = win
        if map == "map1" and self.grid == []:
            self.map_names = "Basic_Curve"
        if map == "map2" and self.grid == []:
            self.map_names = "map_2_2"
        if map == "map3" and self.grid == []:
            self.map_names = "map_3"
            
           
    
    
    
    
    
    def draw_game(self,win, type_alg):
        self.win = win
        if type_alg == "a_(P)" and self.grid == []:
            self.type_alg = "a_(P)"
            self.load_map()
        if type_alg == "a_(M)" and self.grid == []:
            self.type_alg = "a_(M)"
            self.load_map()
        if type_alg == "a_bsf" and self.grid == []:
            self.type_alg = "a_bsf"
            self.load_map()
        
        
        self.run_game(win,self.grid,self.width)
    
    def run_game(self,win,grid, width):
        if self.car != None:
            matrix.draw(win,grid,self.ROWS, width,self.car,self.car2)
       
        
        else:
            matrix.draw(win,grid,self.ROWS, width)
        
    
    def game_event(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
				
            
            if pygame.mouse.get_pressed()[0]:# LEFT
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
                    self.car = matrix.Car(row,col,self.gap,self.ROWS,5,"car",self.grid,(0, 255, 0),(255, 165, 0))
                    self.car.moves()
                    self.car.prev_moves()
                    spot = self.grid[row][col]
                    self.start = spot
                    self.start.make_car()
                    print(self.start.row,"col",self.start.col)
                    print("Scroll up if you want to place the car for the ai")
                    print("if you dont want to play against the ai don't press anything")
                    
                elif self.car != None and self.car.validate(row,col):
                    self.car.update(row,col)
                    #car.set_velocity_spot(prex,prey,row,col)
                    self.car.update_x_y_pos()
                    self.car.moves()
                    #car.moves_for_spot(new_spot)
                    self.car.prev_moves()
           # ------------------------------------------------------------------------------------------
           #for the second car
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # center
                pos = pygame.mouse.get_pos()
                row, col = self.get_clicked_pos(pos, self.ROWS, self.width)
                if not self.car2:
                    self.car2 = matrix.Car(row,col,self.gap,self.ROWS,10,"car2",self.grid,(255, 0, 0),(255, 255, 255))
                    self.car2.moves()
                    self.car2.prev_moves()
                    spot = self.grid[row][col]
                    self.start = spot
                    
                    print(self.start.row,"col",self.start.col)
                    print("Press v to run the algorithm and start playing")
                    print("if you dont want to play against the ai don't press anything")
                    
         
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if self.type_alg == "a_(P)":
                        alg.algorithm_p(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car),self.grid, self.start, self.end,self.car)
                    if self.type_alg == "a_(M)":
                        alg.algorithm_m(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car),self.grid, self.start, self.end,self.car)
                    if self.type_alg == "a_bsf":
                        alg.breadth_first_search(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car),self.grid, self.start, self.end,self.car)
                #Move car
                if event.key == pygame.K_r: 
                    self.car.automate_move(self.win,self.end)
                #Move ai car
                if event.key == pygame.K_h:
                    self.car2.automate_move_play(self.win,self.end)

                #play against the ai
                if event.key == pygame.K_v:
                    if self.type_alg == "a_(P)":
                        versus.algorithm_p(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car,self.car2),self.grid, self.start, self.end,self.car2)
                    if self.type_alg == "a_(M)":
                        versus.algorithm_m(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car,self.car2),self.grid, self.start, self.end,self.car2)
                    if self.type_alg == "a_bsf":
                        versus.breadth_first_search(lambda: matrix.draw(self.win, self.grid, self.ROWS,self.gap,self.car,self.car2),self.grid, self.start, self.end,self.car2)
                
                    





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
                   
        


		
