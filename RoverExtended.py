import pygame
from rover import Rover
import cv2
import numpy as np
import random
import time

from LCADictionary import *

class RoverExtended(Rover):
    def __init__(self):
        Rover.__init__(self)
        pygame.init()
        pygame.display.set_caption('Dashboard')
        self.dashboard = pygame.display.set_mode([700,480])
        self.dashboard.fill((255,255,255))



        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.quit = False
        self.move_speed = 1000 #in ms
        self.treads = [0,0]

        # List of emotions: Searching, Intereted, Bored
        self.emotion = None
        self.short_term_dict = LCADictionary()
        self.long_term_dict = LCADictionary()

        #Establish connection and image stream
    	while type(self.image) == type(None):
            pass

        self.run()

    def process_video_from_rover(self, jpegbytes, timestamp_10msec):
        window_name = 'Machine Perception and Cognitive Robotics'
        array_of_bytes = np.fromstring(jpegbytes, np.uint8)
        self.image = cv2.imdecode(array_of_bytes, flags=3)
        k = cv2.waitKey(5) & 0xFF
        return self.image

    # Move for one time step, move around in random directions
    # Foward left right, backwards if stuck
    # TODO: Don't make movement too choppy (i.e. make each movement duration length)
    # Duration - length in ms that action will be taken
    def random_action(self, duration):
        pass


    # Uses OpenCV to determine whether it is stuck
    # i.e. looking at a wall, pixel values not changing much
    # returns boolean
    def isStuck(self):
        pass

    # Gets rover out of stuck position
    def getUnstuck(self):
        pass


    def rotateLeft(self, duration):
        pass

    def rotateRight(self, duration):
        pass

    def reverse(self, duration):
        pass

    # Move randomly until a new item is found that is
    # not represented in long term
    def findSomethingNew(self, image):
        # While the rover is looking around and "understands" everything
        # Loop ends when it does NOT "understand" what it's looking at
        while self.long_term_dict.isImageRepresented(image):
            self.random_action(self.move_speed)
            if self.isStuck():
                self.getUnstuck()

    def end(self):
        self.quit = True
        self.treads = [0,0]
        self.set_wheel_treads(0,0)
        cv2.destroyAllWindows()
        self.close()  

    def run(self):
    	while not self.quit:
            # Manual quit by user
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if chr(event.key) in ['q','Q','z','Z']:
                        self.quit = True

	        if self.short_term_dict.isImageRepresented(self.image):
	            # Clear short term memory, and move randomly
	            # until a new item is found that is not represented
	            # in long term
	            self.short_term_dict.clear()
	            self.findSomethingNew(self.image)
	        else:
	            # Continue to collect data and update both short and
	            # long term dictionary with frames
	            self.short_term_dict.update(self.image)
	            self.long_term_dict.update(self.image)

	        if self.long_term_dict.isImageRepresented(self.image):
	            self.findSomethingNew(self.image)
	       
            cv2.imshow("RoverCam", self.image)
           
            # Manages loop to be limited by FPS
            self.clock.tick(self.FPS)

            pygame.display.flip()
            self.dashboard.fill((255,255,255))
        self.end()
