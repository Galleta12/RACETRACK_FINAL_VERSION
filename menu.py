
import pygame

import button
import game


pygame.init()


WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Racetrack Game")


#game state
game_paused = False
menu_state = "main"



font = font = pygame.font.SysFont("arialblack", 40)

color_text = (255, 255, 255)

play_img = pygame.image.load("images/PLAY.png").convert_alpha()

quit_img = pygame.image.load("images/QUIT.png").convert_alpha()
map1_img = pygame.image.load('images/MAP1.png').convert_alpha()
map2_img = pygame.image.load('images/MAP2.png').convert_alpha()
map3_img = pygame.image.load('images/MAP3.png').convert_alpha()
a_P_img = pygame.image.load('images/A(P).png').convert_alpha()
a_M_img = pygame.image.load('images/A(M).png').convert_alpha()
bsf_img = pygame.image.load('images/BSF.png').convert_alpha()


#button objects instances
play_button = button.Button(304, 125, play_img, 1)

quit_button = button.Button(336, 375, quit_img, 1)
map1_button = button.Button(226, 75, map1_img, 1)
map2_button = button.Button(225, 200, map2_img, 1)
map3_button = button.Button(246, 325, map3_img, 1)
a_P_button = button.Button(332, 450, a_P_img, 1)
a_M_button = button.Button(297, 250, a_M_img, 1)
bsf_button = button.Button(285, 363, bsf_img, 1)


#game instance
play_game = game.Game(WIDTH)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if play_button.draw(screen):
        menu_state = "play"
  
      if quit_button.draw(screen):
        run = False
    #check if the options menu is open
    if menu_state == "play":
      #draw the different options buttons
      if map1_button.draw(screen):
        menu_state = "map1"
        play_game.save_map(screen,menu_state)
        
      if map2_button.draw(screen):
        menu_state = "map2"
  
        play_game.save_map(screen,menu_state)
      if map3_button.draw(screen):
        menu_state = "map3"
      
        play_game.save_map(screen,menu_state)
      
      
  
    if menu_state[0:3] == "map": 
        
     
      if a_M_button.draw(screen):
        menu_state ="a_(M)"
      if bsf_button.draw(screen):
        menu_state ="a_bsf"
      if a_P_button.draw(screen):
        menu_state ="a_(P)"
    

    if menu_state[0] == "a":
        play_game.draw_game(screen,menu_state)
        play_game.game_event()
       
    
      
        
        
    
        


  else:
    draw_text("Press SPACE to play", font, color_text, 160, 250)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()



