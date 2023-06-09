import pygame
import sys
from pygame.locals import *

from level import Level
from settings import *

class Game():
	def __init__(self):
		super().__init__() 
		pygame.init()
		self.display_surf = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Platform Jump')
		self.clock = pygame.time.Clock()
		self.level = Level()

	def run(self):

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				# TODO How can I avoid running inputs here?
				# Prefer to have it within Player.update()
				self.level.P1.input(event)	
			
			# TODO something wrong with dt perhaps
			dt = self.clock.tick(FPS) / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()