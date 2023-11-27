import random
import pygame
from clock import Clock
from dropdown import Dropdown
from settings import *
from spot import Spot
from algorithms import Algorithm
from button import Button
import sys
pygame.init()
pygame.font.init()


class Main():
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("arialblack", 30)
		self.message_color = WHITE
		self.running = True
		self.game_over = False
		self.FPS = pygame.time.Clock()
		self.clock_running = False
		self.set_position_mode = False
		self.current_state = None

	def instructions(self):
		pass

	def make_grid(self, rows, width):
		grid = []
		gap = width // rows
		for i in range(rows):
			grid.append([])
			for j in range(rows):
				spot = Spot(i, j, gap, rows)
				grid[i].append(spot)

		return grid


	def draw_grid(self, win, rows, width):
		gap = width // rows
		for i in range(rows + 1):
			pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
			for j in range(rows + 1):
				pygame.draw.line(win, GREY, (j* gap, 0), (j* gap, width))


	def draw(self, win, grid, rows, width):
		for row in grid:
			for spot in row:
				spot.draw(win)
		self.draw_grid(win, rows, width)
		pygame.display.update()

	def get_clicked_pos(self, pos, rows, width):
		gap = width // rows
		y, x = pos

		row = y // gap
		col = x // gap

		return row, col

	def is_click_in_maze(self, pos, rows, width):
		x, y = pos
		# Check if the click is within the maze boundaries
		return 0 <= x < width - 30 and 0 <= y < width - 30

	def generate_maze(self, grid, rows_maze):
		start = grid[0][0]
		start.make_start()
		end = grid[rows_maze - 1][rows_maze - 1]
		end.make_end()
		for row in grid:
			for spot in row:
				# spot.make_barrier()
				if spot != start and spot != end and random.random() < 0.3:
					spot.make_barrier()
		nonvisited = []
		nonvisited.append(start)

		while len(nonvisited) > 0:
			current = nonvisited.pop()
			if current == end:
				break
			
			if current in nonvisited:
				continue
			neighbors = current.neighbors
   
			for neighbor in neighbors:
				if not neighbor.is_visited():
					neighbor.reset()
					nonvisited.append(neighbor)
					current.remove_wall(neighbor)
					neighbor.visited = True
		start.reset()
		end.reset()

	def draw_text(self, screen, text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))

	def reset_maze(self, win, grid, rows, width, start, end):
		for row in grid:
			for spot in row:
				if spot.is_closed() or spot.is_open() or not spot.is_barrier():
					spot.reset()
				if spot == start:
					spot.make_start()
				if spot == end:
					spot.make_end()
		self.draw_grid(win, rows, width)
		pygame.display.update()

	def moving(self, direction, start, end, row_start, col_start, grid, rows_maze):
		if direction == "LEFT" and row_start > 0:
			new_row, new_col = row_start - 1, col_start
		elif direction == "RIGHT" and row_start < rows_maze - 1:
			new_row, new_col = row_start + 1, col_start
		elif direction == "UP" and col_start > 0:
			new_row, new_col = row_start, col_start - 1
		elif direction == "DOWN" and col_start < rows_maze - 1:
			new_row, new_col = row_start, col_start + 1
		else:
			return
		new_spot = grid[new_row][new_col]
		if not new_spot.is_barrier():
			return new_row, new_col
		return row_start, col_start

	def run_algo(self, algos, algo, grid, width, clock, rows_maze):
		match algo:
			case 'bfs':				algos.bfs(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
			case 'dfs':				algos.dfs(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
			case 'greedy':			algos.greedy(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
			case 'astar':			algos.a_star(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
			case 'dijkstra':		algos.dijkstra(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
			case _:					algos.a_star(lambda: self.draw(self.screen, grid, rows_maze, width), clock)
    
	# main game loop
	def main(self, width):
		clock = Clock(screen)
		##### important
		rows_maze = ROWS_EASY
		##### important
		grid = self.make_grid(rows_maze, width)
		start = None
		end = None

		select_algo = False
		choose_algo = False
		select_mode = False
		algo = ''
		mode = ''
  
		start_button = Button(775, 100, pygame.image.load('img/button_start.png').convert_alpha(), 0.7)
		generate_maze_button = Button(775, 170, pygame.image.load('img/button_generate.png').convert_alpha(), 0.7)
		mode_button = Button(775, 240, pygame.image.load('img/button_mode.png').convert_alpha(), 0.7)
		algorithm_button = Button(775, 310, pygame.image.load('img/button_algorithm.png').convert_alpha(), 0.7)
		reset_button = Button(775, 380, pygame.image.load('img/button_reset.png').convert_alpha(), 0.7)
		clear_button = Button(775, 450, pygame.image.load('img/button_clear.png').convert_alpha(), 0.7)
  
		easy_mode_button = Button(775, 30, pygame.image.load('img/button_easy.png').convert_alpha(), 0.7)
		medium_mode_button = Button(775, 100, pygame.image.load('img/button_medium.png').convert_alpha(), 0.7)
		hard_mode_button = Button(775, 170, pygame.image.load('img/button_hard.png').convert_alpha(), 0.7)
		render_button = Button(775, 240, pygame.image.load('img/button_render.png').convert_alpha(), 0.7)
		return_mode_button = Button(775, 310, pygame.image.load('img/button_return.png').convert_alpha(), 0.7)
  
		bfs_button = Button(775, 30, pygame.image.load('img/button_bfs.png').convert_alpha(), 0.7)
		dfs_button = Button(775, 100, pygame.image.load('img/button_dfs.png').convert_alpha(), 0.7)
		astar_button = Button(775, 170, pygame.image.load('img/button_a.png').convert_alpha(), 0.7)
		greedy_button = Button(775, 240, pygame.image.load('img/button_greedy.png').convert_alpha(), 0.7)
		dijkstra_button = Button(775, 310, pygame.image.load('img/button_dijkstra.png').convert_alpha(), 0.7)
		return_button = Button(775, 380, pygame.image.load('img/button_return.png').convert_alpha(), 0.7)
  
		row_start, col_start = None, None
		row_end, col_end = None, None
		while self.running:
			self.screen.fill(LIGHTBLUE)
			clock.draw( 775, 30)
   
			if not select_algo and not select_mode:
				start_button.draw(self.screen)
				mode_button.draw(self.screen)
				algorithm_button.draw(self.screen)
				reset_button.draw(self.screen)
				clear_button.draw(self.screen)
				generate_maze_button.draw(self.screen)
    
			elif select_mode:
				easy_mode_button.draw(self.screen)
				medium_mode_button.draw(self.screen)
				hard_mode_button.draw(self.screen)
				render_button.draw(self.screen)
				return_mode_button.draw(self.screen)
    
			else:
				bfs_button.draw(self.screen)
				dfs_button.draw(self.screen)
				astar_button.draw(self.screen)
				greedy_button.draw(self.screen)
				dijkstra_button.draw(self.screen)
				return_button.draw(self.screen)
    
			self.draw(self.screen, grid, rows_maze, width)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = event.pos
					if self.is_click_in_maze(pos, rows_maze, window_size[0]):
						row, col = self.get_clicked_pos(pos, rows_maze, width)
						spot = grid[row][col]
						if not start and spot != end:
							row_start, col_start = row, col
							start = spot
							start.make_start()

						elif not end and spot != start:
							row_end, col_end = row, col
							end = spot
							end.make_end()

						elif spot != end and spot != start:
							spot.make_barrier()

				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = event.pos
     
					if self.is_click_in_maze(pos, rows_maze, window_size[0]):
						row, col = self.get_clicked_pos(pos, rows_maze, width)
						spot = grid[row][col]
						spot.reset()
						if spot == start:
							start = None
						elif spot == end:
							end = None
      
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = event.pos
     
					if not select_algo:
						if start_button.rect.collidepoint(mouse_pos) and start and end:
							for row in grid:
								for spot in row:
									spot.update_neighbors(grid)
							algos = Algorithm( grid, start, end)
							clock.start_timer()
       
							if self.run_algo(algos, algo, grid, width, clock, rows_maze):
								clock.stop_timer()
							choose_algo = False
							continue
							
					if mode_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						select_mode = True
						continue
      
					if algorithm_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						algorithm_button.clicked = True
						select_algo = True
						continue
					
					if reset_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						start = None
						end = None
						grid = self.make_grid(rows_maze, width)
						clock.reset_timer()
      
					if clear_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						self.reset_maze(screen, grid, rows_maze, width, start, end)
						clock.reset_timer()
      
					if return_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						select_algo = False

					if return_mode_button.rect.collidepoint(mouse_pos) and select_mode and not select_algo:
						select_mode = False

					if generate_maze_button.rect.collidepoint(mouse_pos) and not select_algo and not select_mode:
						start = None
						end = None
						grid = self.make_grid(rows_maze, width)
						self.generate_maze(grid, rows_maze)
      
					if render_button.rect.collidepoint(mouse_pos) and select_mode and not select_algo:
						select_mode = False
						self.reset_maze(screen, grid, rows_maze, width, start, end)

						if mode == 'easy':
							rows_maze = ROWS_EASY
						elif mode == 'medium':
							rows_maze= ROWS_MEDIUM
						elif mode == 'hard':
							rows_maze = ROWS_HARD
						else:
							rows_maze = ROWS_EASY
       
						grid = self.make_grid(rows_maze, width)
						continue

					if select_algo and not choose_algo:
						if bfs_button.rect.collidepoint(mouse_pos):					algo = 'bfs'
						elif dfs_button.rect.collidepoint(mouse_pos):				algo = 'dfs'
						elif astar_button.rect.collidepoint(mouse_pos):				algo = 'astar'
						elif greedy_button.rect.collidepoint(mouse_pos):			algo = 'greedy'
						elif dijkstra_button.rect.collidepoint(mouse_pos):			algo = 'dijkstra'
      
						select_algo = False
						algorithm_button.clicked = False
						continue
					
					if select_mode and not select_algo:
						if easy_mode_button.rect.collidepoint(mouse_pos):		mode = 'easy'
						elif medium_mode_button.rect.collidepoint(mouse_pos):	mode = 'medium'
						elif hard_mode_button.rect.collidepoint(mouse_pos):		mode = 'hard'
						continue
     
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_v:
						start = None
						end = None
						grid = self.make_grid(rows_maze, width)
						self.generate_maze(grid, rows_maze)
								
					if event.key == pygame.K_c:
						start = None
						end = None
						grid = self.make_grid(rows_maze, width)
					
					if start and end:
						if event.key == pygame.K_UP:
							point = grid[row_start][col_start]
							point.reset()
							newrow, newcol = self.moving("UP", start, end, row_start, col_start, grid, rows_maze)
							if newrow == row_end and newcol == col_end:
								end = grid[newrow][newcol]
								end.reset()
								end = None
							row_start, col_start = newrow, newcol
							start = grid[newrow][newcol]
							start.make_start()
						elif event.key == pygame.K_DOWN:
							point = grid[row_start][col_start]
							point.reset()
							newrow, newcol = self.moving("DOWN", start, end, row_start, col_start, grid, rows_maze)
							if newrow == row_end and newcol == col_end:
								end = grid[newrow][newcol]
								end.reset()
								end = None
							row_start, col_start = newrow, newcol
							start = grid[newrow][newcol]
							start.make_start()
						elif event.key == pygame.K_RIGHT:
							point = grid[row_start][col_start]
							point.reset()
							newrow, newcol = self.moving("RIGHT", start, end, row_start, col_start, grid, rows_maze)
							if newrow == row_end and newcol == col_end:
								end = grid[newrow][newcol]
								end.reset()
								end = None
							row_start, col_start = newrow, newcol
							start = grid[newrow][newcol]
							start.make_start()
						elif event.key == pygame.K_LEFT:
							point = grid[row_start][col_start]
							point.reset()
							newrow, newcol = self.moving("LEFT", start, end, row_start, col_start, grid, rows_maze)
							if newrow == row_end and newcol == col_end:
								end = grid[newrow][newcol]
								end.reset()
								end = None
							row_start, col_start = newrow, newcol
							start = grid[newrow][newcol]
							start.make_start()

			pygame.display.update()
			self.FPS.tick(60)


if __name__ == "__main__":
	window_size = WINDOW_SIZE
	screen = (window_size[0] + 150, window_size[1])
	screen = pygame.display.set_mode(screen)
	pygame.display.set_caption("Maze Game")

	game = Main(screen)
	game.main(window_size[0] - 30)