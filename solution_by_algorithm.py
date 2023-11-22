import random
import pygame
from clock import Clock
from dropdown import Dropdown
from settings import *
from spot import Spot
from algorithms import Algorithm
from button import Button

pygame.init()
pygame.font.init()


class Main():
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("arialblack", 30)
		#self.message_color = pygame.Color("cyan")
		self.message_color = WHITE
		self.running = True
		self.game_over = False
		self.FPS = pygame.time.Clock()
		self.clock_running = False
		self.set_position_mode = False
		self.dropdown = Dropdown(
			screen,
			[COLOR_INACTIVE, COLOR_ACTIVE],
			[COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
			785, 180, 150, 50,
			pygame.font.SysFont(None, 30), 
			'Algorithms',
			['DFS', 'BFS', 'A*', 'UCS', 'Greedy', 'Dijkstra', 'Floyd-warshall', 'Bellman-Ford', 'Hill climbing']
		)
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

	# draws all configs; maze, player, instructions, and time
	def _draw(self, game, clock, start_button):
		self.instructions()
		if self.game_over:
			clock.stop_timer()
			self.screen.blit(game.message(),(785,120))
			pygame.draw.rect(self.screen, (0, 255, 0), start_button)
			start_text = self.font.render("Start", True, (0, 0, 0))
			self.screen.blit(start_text, (start_button.x + 20, start_button.y + 15))
		else:
			clock.update_timer()
		self.screen.blit(clock.display_timer(), (785, 20)) if self.clock_running else None
		score = self.font.render('Your score: ', True,self.message_color)
		score = self.font.render(f"120 - clock.elapsed_time", True,self.message_color)
		pygame.display.flip()
		pygame.display.update()

	def remove_wall(self, grid, current, next_cell):
		x, y = current.get_pos()
		next_x, next_y = next_cell.get_pos()

		if x == next_x and y < next_y:  # Move down
			wall = grid[x][y + 1]
		elif x == next_x and y > next_y:  # Move up
			wall = grid[x][y - 1]
		elif x < next_x and y == next_y:  # Move right
			wall = grid[x + 1][y]
		elif x > next_x and y == next_y:  # Move left
			wall = grid[x - 1][y]
		wall.reset()


	def generate_maze(self, grid):
		for row in grid:
			for spot in row:
				spot.make_barrier()

		# Set the start and end spots
		start = grid[0][0]
		start.make_start()
		end = grid[ROWS - 1][ROWS - 1]
		end.make_end()
		
		nonvisited = []
		nonvisited.append(start)

		while len(nonvisited) > 0:
			current = nonvisited.pop()
			if current == end:
				break
			
			if current in nonvisited:
				continue

			#current.reset()
			neighbors = current.neighbors
   
			for neighbor in neighbors:
				if not neighbor.is_visited():
					neighbor.reset()
					nonvisited.append(neighbor)
					current.remove_wall(neighbor)
					neighbor.visited = True
					#pygame.display.update()
		start.reset()
		end.reset()

	def draw_text(self, screen, text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))

	def reset_maze(self, win, grid, rows, width, start, end):
		for row in grid:
			for spot in row:
				if spot.is_closed() or spot.is_open() or spot.is_end:
					spot.reset()
				if spot == start:
					spot.make_start()
				if spot == end:
					spot.make_end()
		self.draw_grid(win, rows, width)
		pygame.display.update()

	# main game loop
	def main(self, width):
		clock = Clock()
		
		#maze.generate_maze()
		clock.start_timer()
		
		grid = self.make_grid(ROWS, width)
		start = None
		end = None

		start_button = Button(775, 100, pygame.image.load('img/button_start.png').convert_alpha(), 0.7)
		select_button = Button(775, 200, pygame.image.load('img/button_select.png').convert_alpha(), 0.7)
		reset_button = Button(775, 300, pygame.image.load('img/button_select.png').convert_alpha(), 0.7)
		clear_button = Button(775, 400, pygame.image.load('img/button_select.png').convert_alpha(), 0.7)
		while self.running:
			self.screen.fill(LIGHTBLUE)	
			start_button.draw(self.screen)
			select_button.draw(self.screen)
			reset_button.draw(self.screen)
			clear_button.draw(self.screen)
			self.draw(self.screen, grid, ROWS, width)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = event.pos
					if self.is_click_in_maze(pos, ROWS, window_size[0]):
						row, col = self.get_clicked_pos(pos, ROWS, width)
						spot = grid[row][col]
						if not start and spot != end:
							start = spot
							start.make_start()

						elif not end and spot != start:
							end = spot
							end.make_end()

						elif spot != end and spot != start:
							spot.make_barrier()

				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = event.pos
					if self.is_click_in_maze(pos, ROWS, window_size[0]):
						row, col = self.get_clicked_pos(pos, ROWS, width)
						spot = grid[row][col]
						spot.reset()
						if spot == start:
							start = None
						elif spot == end:
							end = None
      
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = event.pos
					if start_button.rect.collidepoint(mouse_pos) and start and end:
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
						algos = Algorithm( grid, start, end)
						#algos.dfs(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.bfs(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.greedy(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.a_star(lambda: self.draw(self.screen, grid, ROWS, width))
						algos.ucs(lambda: self.draw(self.screen, grid, ROWS, width))
					if select_button.rect.collidepoint(mouse_pos):
						print("select btn clicked")

					if reset_button.rect.collidepoint(mouse_pos):
						start = None
						end = None
						grid = self.make_grid(ROWS, width)
					if clear_button.rect.collidepoint(mouse_pos):
						self.reset_maze(screen, grid, ROWS, width, start, end)
   
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and start and end:
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
						algos = Algorithm( grid, start, end)
						algos.dfs(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.bfs(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.greedy(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.a_star(lambda: self.draw(self.screen, grid, ROWS, width))
						#algos.ucs(lambda: self.draw(self.screen, grid, ROWS, width))
      

					if event.key == pygame.K_v:
						self.generate_maze(grid)
								
						
					if event.key == pygame.K_c:
						start = None
						end = None
						grid = self.make_grid(ROWS, width)

			

			#self.dropdown.draw()
			pygame.display.update()
			self.FPS.tick(60)


if __name__ == "__main__":
	window_size = WINDOW_SIZE
	screen = (window_size[0] + 150, window_size[1])
	tile_size = TILE_SIZE
	screen = pygame.display.set_mode(screen)
	pygame.display.set_caption("Maze")

	game = Main(screen)
	game.main(window_size[0] - 30)