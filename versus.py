from distutils.command.check import check
import math
import pygame
from queue import PriorityQueue
from collections import deque
import time
import copy
import time


#heuristic function pythagoream
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#return abs(x1 - x2) + abs(y1 - y2)
	return math.sqrt((x1 - x2)**2 + abs(y1 - y2)**2)



#heuristic function manhattan
def h_2(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)
	


    
       





# reconstruct the path
def reconstruct_path(came_from, current, draw,car):
	count_path=0
	path_nodes = []
	
	while current in came_from:
		current = came_from[current]
		count_path+=1
		#current.make_path()
		path_nodes.append(current)   
		draw()
	print("This is the number of nodes on the path",count_path+1)
	car.save_path_nodes(path_nodes)
	

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))





def algorithm_m(draw, grid, start, end,car):
	
	start_time = time.time()
	nodes_visited =0
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h_2(start.get_pos(), end.get_pos()) 

	closed_nodes = {}
	
    
	open_set_hash = {start}
	

	
	while not open_set.empty() :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
        
		current = open_set.get()[1]
		
		
		nodes_visited +=1
		#print("Currnet, ", current, "Row",current.row, "Col",current.col, "Velocity",current.get_velocity_spot(), "Velocity car",car.velx,",", car.vely)
		if current in open_set_hash:
			open_set_hash.remove(current)
		

		closed_nodes[current] = [current.get_velocity_spot()[0],current.get_velocity_spot()[1]]
	
		
        
		if current == end:
		
			reconstruct_path(came_from, end, draw, car)
			end_time = time.time()
			time_lapsed = end_time - start_time
			time_convert(time_lapsed)
			end.make_end()
			print("THis is the nodes visited :", nodes_visited )
			
			return True
		car.moves_for_spot(current)
		

		for neighbor in car.moves_spot:
		
				
			temp_g_score = g_score[current] + 1
			
			
			if temp_g_score < g_score[neighbor]:
				
					
				came_from[neighbor] = current
				
				
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h_2(neighbor.get_pos(), end.get_pos()) 
				neighbor.set_velocity_spot(current.row,current.col,neighbor.row,neighbor.col)
				#car.update(neighbor.row,neighbor.col)
				if neighbor not in open_set_hash:
					#car.update(neighbor.row,neighbor.col)
				
					open_set.put((f_score[neighbor], neighbor))
					open_set_hash.add(neighbor)
					
					
					
					if  not neighbor.is_car() and not neighbor.is_end():
						pass
				elif neighbor in closed_nodes:
					if neighbor.get_velocity_spot() != closed_nodes[neighbor]:
						
						# print("Different velocity this is the current", neighbor.row, neighbor.col, "This velocity not in closed", neighbor.get_velocity_spot())
						# print("The ones dropped", neighbor.row, neighbor.col, "This velocity", closed_nodes[neighbor])
					
						open_set.put((f_score[neighbor], neighbor))
						open_set_hash.add(neighbor)
						
						
					   
						
						if  not neighbor.is_car() and not neighbor.is_end():
							pass
					
					

		draw()

		if current != start:
			pass
	print("THis is outside the loop may work if the path was not found")
	end_time = time.time()
	time_lapsed = end_time - start_time
	time_convert(time_lapsed)
	print("THis is the nodes visited :", nodes_visited )

			
			

	return False



def algorithm_p(draw, grid, start, end,car):
	
	start_time = time.time()
	nodes_visited =0
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos()) 

	closed_nodes = {}
	
    
	open_set_hash = {start}
	

	
	while not open_set.empty() :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
        
		current = open_set.get()[1]
		
		
		nodes_visited +=1
		#print("Currnet, ", current, "Row",current.row, "Col",current.col, "Velocity",current.get_velocity_spot(), "Velocity car",car.velx,",", car.vely)
		if current in open_set_hash:
			open_set_hash.remove(current)
		

		closed_nodes[current] = [current.get_velocity_spot()[0],current.get_velocity_spot()[1]]
	
		
        
		if current == end:
		
			reconstruct_path(came_from, end, draw, car)
			end_time = time.time()
			time_lapsed = end_time - start_time
			time_convert(time_lapsed)
			end.make_end()
			print("THis is the nodes visited :", nodes_visited )
			
			return True
		car.moves_for_spot(current)
		

		for neighbor in car.moves_spot:
		
				
			temp_g_score = g_score[current] + 1
			
			
			if temp_g_score < g_score[neighbor]:
				
					
				came_from[neighbor] = current
				
				
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
				neighbor.set_velocity_spot(current.row,current.col,neighbor.row,neighbor.col)
				#car.update(neighbor.row,neighbor.col)
				if neighbor not in open_set_hash:
					#car.update(neighbor.row,neighbor.col)
				
					open_set.put((f_score[neighbor], neighbor))
					open_set_hash.add(neighbor)
					
					
					
					if  not neighbor.is_car() and not neighbor.is_end():
						pass
				elif neighbor in closed_nodes:
					if neighbor.get_velocity_spot() != closed_nodes[neighbor]:
						
						# print("Different velocity this is the current", neighbor.row, neighbor.col, "This velocity not in closed", neighbor.get_velocity_spot())
						# print("The ones dropped", neighbor.row, neighbor.col, "This velocity", closed_nodes[neighbor])
					
						open_set.put((f_score[neighbor], neighbor))
						open_set_hash.add(neighbor)
						
						
					   
						
						if  not neighbor.is_car() and not neighbor.is_end():
							pass
					
					

		draw()

		if current != start:
			pass
	print("THis is outside the loop may work if the path was not found")
	end_time = time.time()
	time_lapsed = end_time - start_time
	time_convert(time_lapsed)
	print("THis is the nodes visited :", nodes_visited )

			
			

	return False

def breadth_first_search(draw, grid, start, end, car):
	start_time = time.time()
	frontier = deque()
	frontier.append(start)
	came_from = {}
	open_set_hash = {start}
	nodes_visited = 0
	while len(frontier) > 0:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = frontier.popleft()
		nodes_visited +=1
		
		
		if current == end:
			reconstruct_path(came_from, end, draw, car)
			end_time = time.time()
			time_lapsed = end_time - start_time
			time_convert(time_lapsed)
			end.make_end()
			print("THis is the nodes visited :", nodes_visited )
			return True
		car.moves_for_spot(current)
		for next in car.moves_spot:
			
			if next not in open_set_hash:
				next.set_velocity_spot(current.row,current.col,next.row,next.col)
				came_from[next] = current				
				frontier.append(next)
				open_set_hash.add(next)
				pass

		draw()

		if current != start:
			pass
	print("THis is outside the loop may work if the path was not found")
	end_time = time.time()
	time_lapsed = end_time - start_time
	time_convert(time_lapsed)
	print("THis is the nodes visited :", nodes_visited )
			
			
	return False




	




