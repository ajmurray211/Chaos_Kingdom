import pygame, os, random, time, sys
pygame.font.init()
import random
from src.game_constants import *

########################### Battlemap gameplay ################################
MAX_FIRE_RATE = 35

def fired_round(obj, round):
    """checks to see if two masks overlap"""
    overlap_x = obj.x - round.x
    overlap_y = obj.y -round.y
    return round.mask.overlap(obj.mask, (overlap_x,overlap_y)) != None

def draw_battlemap(map):
    """starts the battlemap commands"""
    player_vel = 6
    green_player = Player(50, HEIGHT - (GREEN_PLAYER_IMG.get_height() + 50) ,GREEN_PLAYER_IMG , 'green', is_ai=True)
    red_player = Player(WIDTH - (RED_PLAYER_IMG.get_width()+50),100,RED_PLAYER_IMG, 'red',player_vel,)

    winner_text = ''
    run = True
    BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', f'{map}.png')), (WIDTH,HEIGHT))
    pygame.display.update()

    while winner_text == '' and run:

        # Call AI logic for the NPC player
        green_player.ai_logic(red_player)

        WIN.blit(BATTLEMAP_BG,(0,0))
        def draw_winner(text):
            """handles player winning"""
            renderTextCenteredAt(f"{text} player wins!!", winner_font,color_dict['black'],WIDTH/2 ,HEIGHT /2 , WIN, 900)
            pygame.display.update()
            pygame.time.delay(5000)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False

        # handles the player movement and limits the players movement to their perspective boxes
        if keys[pygame.K_a] and green_player.x + player_vel > 0:
            green_player.move('left', player_vel)
        if keys[pygame.K_d] and green_player.x + player_vel + PLAYER_W < WIDTH / 2 - 100:
            green_player.move('right')
        if keys[pygame.K_w] and green_player.y > 20:
            green_player.move('up')
        if keys[pygame.K_s] and green_player.y + player_vel + PLAYER_H < HEIGHT :
            green_player.move('down')
        if keys[pygame.K_LEFT] and red_player.x + player_vel + PLAYER_W > WIDTH / 2 + 100 + PLAYER_W:
            red_player.move('left')
        if keys[pygame.K_RIGHT] and red_player.x + player_vel < WIDTH - PLAYER_W:
            red_player.move('right')
        if keys[pygame.K_UP] and red_player.y > 20:
            red_player.move('up')
        if keys[pygame.K_DOWN]and red_player.y + player_vel + PLAYER_H < HEIGHT:
            red_player.move('down')
        if keys[pygame.K_v]:
            green_player.build()
        if keys[pygame.K_n]:
            red_player.build(True)
        if keys[pygame.K_c]:
            green_player.shoot()
        if keys[pygame.K_m]:
            red_player.shoot(True)
        
        # checks to see if a arrow hits a player or structure
        for arrow in green_player.arrows:
            if red_player.hit(arrow):
                red_player.health -= 10 
                green_player.arrows.remove(arrow)
            for build in red_player.cover_built:
                if build.hit(arrow) and build.health > 0:
                    build.health -= 10 
                    green_player.arrows.remove(arrow)
                elif build.health <= 0:
                    red_player.cover_built.remove(build)
        for arrow in red_player.arrows:
            if green_player.hit(arrow):
                green_player.health -= 10 
                red_player.arrows.remove(arrow)
            for build in green_player.cover_built:
                if build.hit(arrow) and build.health > 0:
                    build.health -= 10 
                    red_player.arrows.remove(arrow)
                elif build.health <= 0:
                    green_player.cover_built.remove(build)

        # draws the barbed wire/ sandbags/ ammo_count
        # WIN.blit(RIVER, (WIDTH/2 - RIVER.get_width()/2, 10))
        for key in text_dict['3']:
            # draws greens info
            if key == 'green':
                green_ammo_count = ammo_count_font.render(str(green_player.mag),1, color_dict['green'])
                WIN.blit(green_ammo_count, (WIDTH - WIDTH/2 - green_ammo_count.get_width() - 150,10))
                for i in range(0, 3-len(green_player.cover_built)):
                    WIN.blit(BOLDER,(BOLDER.get_width() * i, 10))

            # draws reds info
            if key == 'red':
                red_ammo_count = ammo_count_font.render(str(red_player.mag),1,color_dict['red'])
                WIN.blit(red_ammo_count, (WIDTH/2 + red_ammo_count.get_width() + 100, 10))
                for i in range(0, 3-len(red_player.cover_built)):
                    WIN.blit(BOLDER,(WIDTH - (BOLDER.get_width() * (i+1)), 10))

        # draws the players on the screen
        green_player.draw(WIN)
        red_player.draw(WIN)
    
        # update winner
        if green_player.health == 0:
            winner_text = 'Red'
        if red_player.health == 0:
            winner_text = 'Green'
        if winner_text != '':
            draw_winner(winner_text)
        pygame.display.update()
    return(winner_text)
############################ End of battlemap section ########################

def draw_main_menu(what):
    """draws the main menu and runs the commands"""
    WIN.blit(MAIN_MENU_BG, (0,0))
    if what == 'title':
        prompt1 = main_font.render(text_dict['1']['prompt1'], 1, color_dict['black'])
        WIN.blit(prompt1, (WIDTH/2 - prompt1.get_width()/2 ,HEIGHT/2))
        renderTextCenteredAt(text_dict['1']['prompt2'], main_font,color_dict['black'], 200, HEIGHT - HEIGHT/4, WIN, 200)
        renderTextCenteredAt(text_dict['1']['prompt3'], main_font,color_dict['black'], 500, HEIGHT - HEIGHT/4, WIN, 200)
        renderTextCenteredAt(text_dict['1']['prompt4'], main_font,color_dict['black'], 800, HEIGHT - HEIGHT/4, WIN, 200)
    if what == 'how_to':
        renderTextCenteredAt(text_dict['2']['title'], main_font, color_dict['black'], WIDTH/2, 150, WIN, 600)
        renderTextCenteredAt(text_dict['2']['prompt'], main_font, color_dict['black'], WIDTH/2, 200, WIN, 650)
    if what == 'about':
        renderTextCenteredAt(text_dict['4']['title'], main_font, color_dict['black'], WIDTH/2, 150, WIN, 600)
        renderTextCenteredAt(text_dict['4']['prompt'], main_font, color_dict['black'], WIDTH/2, 200, WIN, 650)
    if what == 'controls':
        renderTextCenteredAt(text_dict['5']['title'], main_font, color_dict['black'], WIDTH/2, 150, WIN, 600)
        renderTextCenteredAt(text_dict['5']['prompt1'], main_font, color_dict['black'], WIDTH/2 - 200, 200, WIN, 245)
        renderTextCenteredAt(text_dict['5']['prompt2'], main_font, color_dict['black'], WIDTH/2 + 200, 200, WIN, 325)

def main():
    """This is the main menu handling initial game events"""
    clock = pygame.time.Clock()
    run = True
    draw_main_menu('title')

    while run:
        # draw main menu background
        title = winner_font.render(text_dict['1']['title'], 1, color_dict['black'])
        WIN.blit(title, (WIDTH/2 - title.get_width()/2,10))
        
        clock.tick(FPS)
        # default quit function in loop
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_BACKSPACE]:
                draw_main_menu('title')
            if keys[pygame.K_h]:
                draw_main_menu('how_to')
            if keys[pygame.K_a]:
                draw_main_menu('about')
            if keys[pygame.K_c]:
                draw_main_menu('controls')
            if keys[pygame.K_SPACE]:
                draw_gameboard()

        pygame.display.update()

# only runs the game if the file name is "main"
if __name__ == '__main__':
    main()