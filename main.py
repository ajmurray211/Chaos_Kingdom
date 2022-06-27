from email.header import Header
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# set border 
# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size

# Import pictures and set colors
# player 1
# player 2
# Bullet
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
# color dict

## Battlemap gameplay ##

# player class
    # def to shoot
    # def to move bullets
    # def for being hit 
    # def to draw
    # def for healthbar

# class for bullet
    # def for moving
    # def for draw
    # def for collision
    # def for offscreen

# def to draw the winner text

# def to draw the window
def draw_window():
    """This method updates the window"""
    WIN.blit(BG, (0,0))
    pygame.display.update()

## This is the process for filtering multiple screens ###
def main():
    run =True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    # def for main menu
    #     filter clicks to launch different screens
    #         closing the app
    #         directions
    #         controls
    #         running the gameboard

    # def for gameboard
    #     filter clicks to launch different screens
    #         closing to the main menu 
    #         opening the battle map

    # def for battlemap
    # define instance of player for player 1 
    # define instance of player for player 2
    #     filter for the end of game or quit that returns to game board 
    #         game ends or close launches gameboard

            
# call main menu to run the app 
main()