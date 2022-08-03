import math
import pygame
from queue import PriorityQueue
from collections import deque
import time
import copy


#heuristic function
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#return abs(x1 - x2) + abs(y1 - y2)
	return math.sqrt((x1 - x2)**2 + abs(y1 - y2)**2)
# I am not using this
def pythagorea(x,y):
	return math.sqrt(x**2 + y**2)



# reconstruct the path
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		#time.sleep(0.2)
        
		draw()

# posibles 
# cerrados nodes
# my a start algorithm
def algorithm(draw, grid, start, end,car):
	#count = 0
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos()) 
	vel_check = {spot: [float("inf"),float("inf")] for row in grid for spot in row}
	vel_check[start][0] = 0
	vel_check[start][1] = 0
    
	open_set_hash = {start : [start.vx_spot,start.vy_spot]}
	

	while not open_set.empty() :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
        
		current = open_set.get()[1]
		if current in open_set_hash:
			open_set_hash.pop(current)
		#open_set_hash.remove(current)
		#car.update(current.row,current.col)
		#car.update_x_y_pos()
		
        
		if current == end:
		
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True
		# get the new moves
		car.moves_for_spot(current)
		#car.moves()
		#car.update_x_y_pos()
	    
        #check all the moves
		for neighbor in car.moves_spot:
			# for outs in current.neighbors:
			# 	if neighbor == outs:
				
			temp_g_score = g_score[current] + 1
			
			
			if temp_g_score < g_score[neighbor]:
				
				# check the g score and update it	
				came_from[neighbor] = current
				
				
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
				#here is the problem
				if neighbor in open_set_hash:
					if open_set_hash[neighbor] != [neighbor.vx_spot,neighbor.vy_spot] or open_set_hash[neighbor] == [neighbor.vx_spot,neighbor.vy_spot] :
						
						open_set.put((f_score[neighbor], neighbor))
						#open_set_hash.add(neighbor)
						open_set_hash[neighbor] = [neighbor.vx_spot,neighbor.vy_spot]
					
						
						if  not neighbor.is_car() and not neighbor.is_end():
							neighbor.make_open()

				else:
					
					neighbor.set_velocity_spot(current.row,current.col,neighbor.row,neighbor.col)
					if neighbor not in open_set_hash:
						neighbor.set_velocity_spot(current.row,current.col,neighbor.row,neighbor.col)
						#car.update(current.row,current.col)
						#count += 1
						
						open_set.put((f_score[neighbor], neighbor))
						#open_set_hash.add(neighbor)
						open_set_hash[neighbor] = [neighbor.vx_spot,neighbor.vy_spot]
						vel_check[neighbor][0] = [car.velx]
						vel_check[neighbor][1] = [car.vely]
						
						if  not neighbor.is_car() and not neighbor.is_end():
							neighbor.make_open()
				
					
					

		draw()

		if current != start:
			current.make_closed()
			#pass
			

	return False

def breadth_first_search(draw, grid, start, end, car):
	frontier = deque()
	frontier.append(start)
	came_from = {}
	open_set_hash = {start}
	
	while len(frontier) > 0:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = frontier.popleft()
		car.update(current.row,current.col)
		
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True
		car.moves()
		for next in car.moves_spot:
			
			if next not in open_set_hash:
				car.update(current.row,current.col)
				came_from[next] = current				
				frontier.append(next)
				open_set_hash.add(next)
				next.make_open()

		draw()

		if current != start:
			current.make_closed()
			
			
	return False




	




