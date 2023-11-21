from queue import *
import pygame
import heapq
import random
class Algorithm:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        
    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


    def reconstruct_path(self, came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
    
    def dfs(self, draw):
        open_set = [self.start]
        came_from = {}
        close = set()
        while open_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            current = open_set.pop()
            #close.add(current)
            if current == self.end:
                self.reconstruct_path(came_from, self.end, draw)
                self.end.make_end()
                return True
            
            if current not in close:
                close.add(current)
                
                #random.shuffle(current.neighbors)
                for neighbor in current.neighbors:
                    if neighbor not in close:
                        open_set.append(neighbor)
                        came_from[neighbor] = current
                        neighbor.make_open()
                    
            draw()
            
            if current != self.start:
                current.make_closed()
                
        return False
                    
            
        

    def bfs(self, draw):
        open_set = Queue()
        open_set.put(self.start)
        came_from = {}
        close = set()
        while open_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            current = open_set.get()
            #close.add(current)
            if current == self.end:
                self.reconstruct_path(came_from, self.end, draw)
                self.end.make_end()
                return True
            
            if current not in close:
                close.add(current)
                
                random.shuffle(current.neighbors)
                for neighbor in current.neighbors:
                    if neighbor not in close:
                        open_set.put(neighbor)
                        came_from[neighbor] = current
                        neighbor.make_open()
                    
            draw()
            
            if current != self.start:
                current.make_closed()

    def a_star(self, draw):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[self.start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[self.start] = self.h(self.start.get_pos(), self.end.get_pos())

        open_set_hash = {self.start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end:
                self.reconstruct_path(came_from, self.end, draw)
                self.end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), self.end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != self.start:
                current.make_closed()

        return False

    def ucs(self):
        pass

    def greedy(self, draw):
        open_set = PriorityQueue()
        open_set.put((self.h(self.start.get_pos(), self.end.get_pos()), self.start))
        closed_set = set()
        came_from = {}
        
        while open_set:
            current = open_set.get()[1]
            if current == self.end:
                self.reconstruct_path(came_from, self.end, draw)
                self.end.make_end()
                return True
            
            closed_set.add(current)
            
            for neighbor in current.neighbors:
                if neighbor not in closed_set:
                    heuristic = self.h(neighbor.get_pos(), self.end.get_pos())
                    open_set.put(( heuristic, neighbor))
                    came_from[neighbor] = current
                    neighbor.make_open()
                    
            draw()
            if current != self.start:
                current.make_closed()
                
        return False
        

    def dijkstra(self):
        pass

    def floyd_warshall(self):
        pass

    def bellman_ford(self):
        pass

    def hill_climbing(self):
        pass
    
    def solve(self, algo):
        
        pass