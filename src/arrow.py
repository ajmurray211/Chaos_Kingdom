from game_constants import *

class Arrow:
    def __init__(self, x, y, img, color):
        self.x = x
        self.y = y
        self.img = img
        self.color = color
        self.mask = pygame.mask.from_surface(self.img) 
        
    def draw(self, window ):
        """draws the arrows"""
        window.blit(self.img, (self.x, self.y))
        self.move_b(vel = 3)
        
    def move_b(self, vel):
        """moves the arrow based on player color"""
        if self.color == 'green':
            self.x += vel
        elif self.color == 'red':
            self.x -= vel

    def off_screen(self):
        """checks to see if a arrow leavs the screen"""
        return not(self.x < WIDTH and self.x >0)
