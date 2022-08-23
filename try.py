# from locale import currency
# import math
# import pygame
# from queue import PriorityQueue
# from collections import deque
# import time
# import copy
# import time





# open_set = PriorityQueue()



# open_set.put((4, "spot2"))
# open_set.put((5, "spot3"))
# open_set.put((6, "spot5"))
# open_set.put((7, "spot7"))
# open_set.put((2, "spot8"))
# open_set.put((10, "spot8"))

# print("THis is the open set")
# print(open_set.queue)

# print("This remove item")
# currency = open_set.get()[1]
# print("This get",currency)
# print("New open set")
# print(open_set.queue)
import heapq

xd = []
heapq.heapify(xd)
heapq.heappush(xd, (11,"Spot1"))
heapq.heappush(xd, (1,"Spot1"))
heapq.heappush(xd, (1,"Spot12"))
heapq.heappush(xd, (10,"Spot1"))
heapq.heappush(xd, (8,"Spot1"))


print(xd)

print("This index", heapq.heappop(xd)[1] )

print(xd[0])
print(xd[0][1])
