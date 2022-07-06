import pygame, os, random, time, sys
pygame.font.init()

###################### Game settings and imports section ###############################
# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# import font 
main_font = pygame.font.Font('assets/IMMORTAL.ttf', 30)
city_font = pygame.font.Font('assets/IMMORTAL.ttf', 20)
ammo_count_font = pygame.font.Font('assets/IMMORTAL.ttf', 60)
winner_font = pygame.font.Font('assets/IMMORTAL.ttf', 100)

# set FPS and Vel for arrows and player movement
FPS = 60

# set W adn H for player size
PLAYER_W, PLAYER_H = 70, 70
ARROW_W, ARROW_H = 40, 10

## Import pictures and set colors ##
NEUTRAL_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_flag.png')), (50, 40))

# player 1 - red
RED_PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_player.png')), (PLAYER_W, PLAYER_H))
UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_flag.png')), (50, 40))
ACTIVE_UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_red.png')), (50, 40))

# player 2 - green
GREEN_PLAYER_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_player.png')), (PLAYER_W, PLAYER_H))
UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_flag.png')), (50, 40))
ACTIVE_UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_green.png')), (50, 40))

# arrows and barriers
ARROW1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'arrow1.png')), (ARROW_W, ARROW_H))
RIVER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'river.png')), (120, HEIGHT))
BOLDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bolder.png')), (90, 70))

# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'title_bg5.png')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg1.jpeg')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG}#, '3':BATTLEMAP_BG

# color
color_dict = {'white':(255,255,255), 'yellow':(255,255,0), 'blue':(0,0,255), 'black':(0,0,0), 'green': (0,255,0), 'red':(255,0,0)}
text_dict = { 
    '1': {
        "title": "Chaos Kingdom",
        "prompt1": "Press the spacebar to start",
        "prompt2": "Press h to view game description",
        "prompt3": "Press a to view about game maker",
        "prompt4": "Press c to view controls",
    },
    '2':{
        'title': 'How to play',
        'prompt': 'This is a turn based conquest game. The goal of the game is to take over every city. You will be prompted to move your active token to a city if that city is neutral (blue) you will automatically get it but if that city is the opposing players color you will automatically be launched into a battlemap. The winner of that match will determine who gets the city. Once you select a direction to move press the spacebar to end your turn.'
    },
    '3':{   
        'title': "Battle map",
        'red':{
            'ammo': 15,
            'structures': 3,
            'health': 100
        },
        'green':{
            'ammo': 15,
            'structures': 3,
            'health': 100
        }
    },
    '4':{
        'title': 'About maker',
        'prompt': 'This game was inspired from starwars battlefront 2 a game that my brother and I used to play growing up. The structure is based off of battlefront but the theme of the game stems from my love of Skyrim and fantasy RPGs. This is the first game that I have ever built and I had a blast, hopefully you enjoy playing!'
    },
    '5':{
        'title': 'Battle map controls',
        'prompt1': '--- Player 1 --- UP-w, DOWN-s, LEFT-a, RIGHT-d, SHOOT-c, BUILD-v. ',
        'prompt2': '--- Player 2 --- UP-arrow up, DOWN - arrow down, LEFT - left arrow, RIGHT - right arrow, SHOOT - n, BUILD - m'
    }
}
city_dict = {
    "Utrila": {        
        'x_cord': 836,
        'y_cord': 220,
        'city_num': 1,
        'bg': 'lava_bg',
        'linked_cities': ['Yido', 'Ipria']
        },
    "Gishire": {
        'x_cord': 95,
        'y_cord': 300,
        'city_num': 2,
        'bg': 'mountain_bg',
        'linked_cities': ['Tetgas', 'Sheaford']
        },
    "Tetgas": {        
        'x_cord': 320,
        'y_cord': 212,
        'city_num': 3,
        'bg': 'waterfall_bg',
        'linked_cities': ['Gishire', 'Oreledo', 'Plecdiff']
        },
    "Oreledo": {
        'x_cord': 395,
        'y_cord': 300,
        'city_num': 4,
        'bg': 'mountain_bg',
        'linked_cities': ['Tetgas', 'Inphis', 'Strinta']
        },
    "Plecdiff": {
        'x_cord': 460,
        'y_cord': 185,
        'city_num': 5,
        'bg': 'mountain_bg',
        'linked_cities': ['Tetgas', 'Strinta']
        },
    "Strinta": {
        'x_cord': 518,
        'y_cord': 242,
        'city_num': 6,
        'bg': 'mountain_bg',
        'linked_cities': ['Plecdiff', 'Ipria', 'Yido', 'Oreledo']    
        },
    "Yido": {
        'x_cord': 830,
        'y_cord': 100,
        'city_num': 7,
        'bg': 'winter_bg',
        'linked_cities': ['Strinta', 'Utrila']    
        },
    "Ipria": {
        'x_cord': 627,
        'y_cord': 343,
        'city_num': 8,
        'bg': 'desert_bg1',
        'linked_cities': ['Utrila', 'Strinta', 'Zhento']    
        },
    "Zhento": {
        'x_cord': 765,
        'y_cord': 450,
        'city_num': 9,
        'bg': 'desert_bg1',
        'linked_cities': ['Ipria', 'Uleron']
        },
    "Uleron": {
        'x_cord': 374,
        'y_cord': 478,
        'city_num': 10,
        'bg': 'winter_bg',
        'linked_cities': ['Inphis', 'Zhento']
    },
    "Inphis": {
        'x_cord': 334,
        'y_cord': 347,
        'city_num': 11,
        'bg': 'mountain_bg',
        'linked_cities': ['Oreledo', 'Uleron', 'Glavine']
    },
    "Glavine": {
        'x_cord': 295,
        'y_cord': 317,
        'city_num': 12,
        'bg': 'mountain_bg',
        'linked_cities': ['Inphis','Sheaford']
    },
    "Sheaford": {
        'x_cord': 205,
        'y_cord': 400,
        'city_num': 13,
        'bg': 'mountain_bg',
        'linked_cities': ['Gishire','Glavine']
    }
}
###################### end of Game settings and imports section ##############
 
###################### Gameboard gameplay ####################################
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
############################ end of gameboard gameplay #######################

########################### Battlemap gameplay ################################
class Player:
    MAX_FIRE_RATE = 35
    def __init__(self,x, y, player_img, color, health =100):
        self.x =x
        self.y =y
        self.color =color
        self.player_img = player_img
        self.mask = pygame.mask.from_surface(self.player_img)
        self.arrows = []
        self.cover_built = []
        self.health = health
        self.max_health = 100
        self.fire_rate = 0
        self.build_rate = 0
        self.mag = text_dict['3'][self.color]['ammo']
        self.cover_count =text_dict['3'][self.color]['structures']

    def draw(self, window):
        """draws the player, and calls arrows, structures and health draw methods"""
        window.blit(self.player_img, (self.x,self.y))
        self.healthbar(window)
        self.move_arrows()
        for arrow in self.arrows:
            arrow.draw(window)
        for cover in self.cover_built:
            cover.draw()

    def shoot(self, inverse = False):
        """shoots a arrow"""
        if self.mag >= 0 and self.fire_rate == 0:
            if inverse:
                arrow = Arrow(self.x, self.y + GREEN_PLAYER_IMG.get_height()/2, pygame.transform.rotate(ARROW1, 180), self.color)
            else:
                arrow = Arrow(self.x + GREEN_PLAYER_IMG.get_width(), self.y + RED_PLAYER_IMG.get_height()/2, ARROW1, self.color)
            self.arrows.append(arrow)
            self.mag -= 1
            self.fire_rate = 1
        elif self.mag == 1:
            self.reload_gun()

    def reload_gun(self):
        """relaods the gun after a set amount of time"""
        self.mag = 15

    def cool_down(self):
        """sets a cooldown for shooting"""
        if self.fire_rate >= self.MAX_FIRE_RATE:
            self.fire_rate = 0
        elif self.fire_rate > 0:
            self.fire_rate += 1

    def move_arrows(self, vel = 3):
        """moves a players arrows, until it is off screen then it deletes"""
        self.cool_down()
        for arrow in self.arrows:
            arrow.move_b(vel)
            if arrow.off_screen():
                self.arrows.remove(arrow)

    def move(self, direction, player_vel):
        """controls a players movement"""
        if direction == 'right':
            self.x += player_vel
        if direction == 'left':
            self.x -= player_vel
        if direction == 'up':
            self.y -= player_vel
        if direction == 'down':
            self.y += player_vel

    def hit(self, round):
        """checks to see if a hit has happened"""
        return fired_round(self,round)

    def build(self, inverse = False):
        """Places a pice of cover down"""
        if self.fire_rate == 0:
            if len(self.cover_built) < 3 :
                if inverse:
                    cover = Structure(self.x - RED_PLAYER_IMG.get_width() - 10, self.y + 10,BOLDER)
                else:
                    cover = Structure(self.x + GREEN_PLAYER_IMG.get_width(), self.y, BOLDER)
                self.cover_built.append(cover)
                for cover in self.cover_built:
                    cover.draw()
            self.fire_rate = 1

    def healthbar(self, window):
        """braws a healthbar for the player"""
        pygame.draw.rect(window, color_dict['red'], (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(window, color_dict['green'], (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width() * (self.health / self.max_health), 10))

def fired_round(obj, round):
    """checks to see if two masks overlap"""
    overlap_x = obj.x - round.x
    overlap_y = obj.y -round.y
    return round.mask.overlap(obj.mask, (overlap_x,overlap_y)) != None

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

def draw_battlemap(map):
    """starts the battlemap commands"""
    green_player = Player(50, HEIGHT - (GREEN_PLAYER_IMG.get_height() + 50) ,GREEN_PLAYER_IMG , 'green')
    red_player = Player(WIDTH - (RED_PLAYER_IMG.get_width()+50),100,RED_PLAYER_IMG, 'red')
    player_vel = 6
    winner_text = ''
    run = True
    BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', f'{map}.png')), (WIDTH,HEIGHT))
    pygame.display.update()

    while winner_text == '' and run:
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
            green_player.move('right', player_vel)
        if keys[pygame.K_w] and green_player.y > 20:
            green_player.move('up', player_vel)
        if keys[pygame.K_s] and green_player.y + player_vel + PLAYER_H < HEIGHT :
            green_player.move('down', player_vel)
        if keys[pygame.K_LEFT] and red_player.x + player_vel + PLAYER_W > WIDTH / 2 + 100 + PLAYER_W:
            red_player.move('left', player_vel)
        if keys[pygame.K_RIGHT] and red_player.x + player_vel < WIDTH - PLAYER_W:
            red_player.move('right', player_vel)
        if keys[pygame.K_UP] and red_player.y > 20:
            red_player.move('up', player_vel)
        if keys[pygame.K_DOWN]and red_player.y + player_vel + PLAYER_H < HEIGHT:
            red_player.move('down', player_vel)
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