import pygame
import 

class Structure:
    def __init__(self, x, y, img):
        self.x = x 
        self.y =y 
        self.img = img
        self.health = 3
        self.mask = pygame.mask.from_surface(self.img)
        self.health = 20

    def draw(self):
        """draws the cover"""
        WIN.blit(self.img, (self.x, self.y))
        
    def hit(self, round):
        """checks to see in a structure was hit"""
        return fired_round(self,round)
