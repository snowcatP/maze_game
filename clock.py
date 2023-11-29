import pygame, time
import settings
pygame.font.init()

class Clock:
	def __init__(self, screen):
		self.start_time = None
		self.elapsed_time = 0
		self.font = pygame.font.SysFont("calibri", 30)
		self.message_color = pygame.Color(settings.BLACK)
		self.running = False
		self.screen = screen
	# Start the timer
	def start_timer(self):
		self.start_time = pygame.time.get_ticks()
		self.running = True

	# Update the timer
	def update_timer(self):
		if self.running:
			self.elapsed_time = (pygame.time.get_ticks() - self.start_time)
		#self.display_timer()
		
	# Display the timer
	def display_timer(self):
		millisecs = int(self.elapsed_time % 1000)
		secs = int((self.elapsed_time // 1000) % 60)
		mins = int((self.elapsed_time // (1000 * 60)) % 60)
		my_time = self.font.render(f"{mins:02}:{secs:02}.{millisecs:03}", True, self.message_color) 
		self.screen.blit(my_time, (840, 10))
		pygame.display.flip()
	def draw(self, x, y):
		millisecs = int(self.elapsed_time % 1000)
		secs = int((self.elapsed_time // 1000) % 60)
		mins = int((self.elapsed_time // (1000 * 60)) % 60)
  
		formatted_timer = f"{mins:02}:{secs:02}.{millisecs:03}"
		text_surface = self.font.render(formatted_timer, True, (0, 0, 0))
		self.screen.blit(text_surface, (x, y))
		
	def reset_timer(self):
		self.elapsed_time = 0

	# Stop the timer
	def stop_timer(self):
		self.start_time = None