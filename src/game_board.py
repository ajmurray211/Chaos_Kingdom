import pygame, sys
from game_constants import *

def renderTextCenteredAt(text, font, color, x, y, screen, allowed_width):
    """Renders text wrapping at a specified width, and centered"""
    words = text.split()
    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break
        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, color)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

def draw_gameboard():
    """"starts the gamboard commands"""
    # variables
    run=True
    clock = pygame.time.Clock()
    red_active_token = []
    green_active_token = []
    red_owned_cities = []
    green_owned_cities = []
    neutral_cities = []
    turn_index = 1

    # capitals
    red_owned_cities.append('Utrila')
    green_owned_cities.append('Gishire')

    def change_owner(city, attacker):
        """changes the owner of a city based on an attack"""
        print(attacker)
        if city in neutral_cities:
            if attacker == 'red' and city not in red_owned_cities:
                red_owned_cities.append(city)
            if attacker =='green' and city not in green_owned_cities:
                green_owned_cities.append(city)
        elif city in red_owned_cities and attacker == 'green':
            red_owned_cities.remove(city)
            green_owned_cities.append(city)
        elif city in green_owned_cities and attacker == 'red':
                green_owned_cities.remove(city)
                red_owned_cities.append(city)
        
    def active_token_change(who, city, index):
        """Changes the active token for the each player"""
        if who == 'red':
            red_active_token.pop(0)
            red_active_token.append(city_dict[city]['linked_cities'][index])
            change_owner(city_dict[city]['linked_cities'][index], who)
            pygame.display.update()
        elif who == 'green':
            green_active_token.pop(0)
            green_active_token.append(city_dict[city]['linked_cities'][index])
            change_owner(city_dict[city]['linked_cities'][index], who)
            pygame.display.update()

    def check_owner(who,city):
        """checks the current owner of the city, and launches battle map if necessary"""
        if who == 'red' and city in green_owned_cities:
            draw_battlemap(city_dict[city]['bg'])
        if who == 'green' and city in red_owned_cities:
            draw_battlemap(city_dict[city]['bg'])

    def winner(who):
        """declares the game winner and brings you to main menu"""
        winner_msg = winner_font.render(f"{who} you have won!!",1, color_dict['black'])
        WIN.blit(winner_msg, (30, HEIGHT /2 - winner_font.get_height() /2 ))
        pygame.display.update()
        pygame.time.delay(5000)
        draw_main_menu()

    def move(who, city):
        """checks to see where you can move and allows movement, returns boolean if movement is allowed""" 
        linked_cities = city_dict[city]['linked_cities']
        if len(linked_cities) == 2:
            renderTextCenteredAt(f'{who}: Press UP to move to {linked_cities[0]}, or DOWN to move to {linked_cities[1]}', city_font, color_dict['black'], WIDTH/2, HEIGHT -80, WIN, 500)
            if keys[pygame.K_UP]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[0]))
                print(check_owner(who, city_dict[city]['linked_cities'][0]))
                active_token_change(who,city,0)
                return True
            if keys[pygame.K_DOWN]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[1]))
                active_token_change(who, city , 1)
                return True
        elif len(linked_cities) == 3: 
            renderTextCenteredAt(f'{who}: Press UP to move to {linked_cities[0]}, DOWN to move to {linked_cities[1]}, or RIGHT to move to {linked_cities[2]}', city_font, color_dict['black'], WIDTH/2, HEIGHT -80, WIN, 500) 
            if keys[pygame.K_UP]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[0]))
                active_token_change(who,city, 0)
                return True
            if keys[pygame.K_DOWN]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[1]))
                active_token_change(who,city, 1)
                return True
            if keys[pygame.K_RIGHT]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[2]))
                active_token_change(who,city, 2) 
                return True
        elif len(linked_cities) == 4:             
            renderTextCenteredAt(f'{who}: Press UP to move to {linked_cities[0]}, DOWN to move to {linked_cities[1]}, RIGHT to move to {linked_cities[2]}, or Left to {linked_cities[3]} ', city_font, color_dict['black'], WIDTH/2, HEIGHT -80, WIN, 500)
            if keys[pygame.K_UP]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[0]))
                active_token_change(who,city, 0)
                return True
            if keys[pygame.K_DOWN]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[1]))
                active_token_change(who,city, 1)
                return True
            if keys[pygame.K_RIGHT]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[2]))
                active_token_change(who,city, 2)
                return True
            if keys[pygame.K_LEFT]:
                change_owner(linked_cities[0], check_owner(who, linked_cities[3]))
                active_token_change(who,city, 3)
                return True
   
    while run:
        keys = pygame.key.get_pressed()
        event = pygame.event.wait()
        clock.tick(FPS)
        WIN.blit(GAME_BOARD_BG, (0,0))

        # assigns initial active token
        if len(red_active_token) == 0:
            red_active_token.append(red_owned_cities[0])
        if len(green_active_token) == 0:
            green_active_token.append(green_owned_cities[0])

        # assigns name and flags to cities
        for name in city_dict:
            if name not in red_owned_cities or name not in green_owned_cities:
                neutral_cities.append(name)

            # assigns flags to the correct color and location
            city_name = city_font.render(name,1,color_dict['white'])
            if name in red_owned_cities :
                if name in red_active_token:
                    WIN.blit(ACTIVE_UNIT1_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                else:
                    WIN.blit(UNIT1_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'],city_dict[name]['y_cord'] - (UNIT2_FLAG.get_height() - 20)))
            elif name in green_owned_cities:
                if name in green_active_token:
                    WIN.blit(ACTIVE_UNIT2_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                else:
                    WIN.blit(UNIT2_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'],city_dict[name]['y_cord'] - (UNIT2_FLAG.get_height() - 20)))
            else:
                WIN.blit(NEUTRAL_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'], city_dict[name]['y_cord'] - city_name.get_height() + 10))

        # declares winner
        if len(red_owned_cities) == 13 or 'Gishire' in red_owned_cities:
            winner('Red')
        if len(green_owned_cities) == 13 or 'Utrila' in green_owned_cities:
            winner('Green')

        # executes the turn based portion of the game 
        if turn_index  == 1:
           if move('green', green_active_token[0]):
               turn_index += 1
        elif turn_index == 2:
            if move('red', red_active_token[0]):
                turn_index -= 1
            
        # dev controls to progress or quit to be deleted later 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                run = False

        # renders the city count and updates the screen
        green_cities = ammo_count_font.render(str(len(green_owned_cities)),1, color_dict['black'])
        WIN.blit(green_cities, (100, HEIGHT - ammo_count_font.get_height() - 10))
        red_cities = ammo_count_font.render(str(len(red_owned_cities)),1, color_dict['black'])
        WIN.blit(red_cities, (860, HEIGHT - ammo_count_font.get_height() - 10))
        pygame.display.update()
