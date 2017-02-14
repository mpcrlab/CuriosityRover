import pygame
import rover as Rover
import cv2
import numpy as np

from LCADictionary import *

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.quit = False
        self.treads = [0,0]

		# List of emotions: Searching, Intereted, Bored 
		self.emotion = None
		self.short_term_dict = LCADictionary()
		self.long_term_dict = LCADictionary()

		#Establish connection and image stream
		while type(self.image) == type(None):
			pass

        self.run()

	# Move for one time step, move around in random directions
	# Foward left right, backwards if stuck
	# TODO: Don't make movement too choppy (i.e. make each movement like 1s)
	def random_action(self):
		pass

	# Move randomly until a new item is found that is 
	# not represented in long term
	def findSomethingNew(self, dict, image):
		pass

	def run(self):
		while not self.quit:
			if self.short_term_dict.isImageRepresented(self.image):
				# Clear short term memory, and move randomly
				# until a new item is found that is not represented
				# in long term
				self.short_term_dict.clear()
				self.findSomethingNew(self.long_term_dict, self.image)
			else:
				# Continue to collect data and update both short and
				# long term dictionary with frames
				self.short_term_dict.update(self.image)
				self.long_term_dict.update(self.image)

			# Manual quit by user
			for event in pygame.event.get():
	            if event.type == pygame.KEYDOWN:
	                if chr(event.key) in ['q','Q']:
	                	self.quit = True

	        # Manages loop to be limited by FPS       	
            self.clock.tick(self.FPS)
