import pygame, os, random, time
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
UNIT1_IMG = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'unit1.png')), (PLAYER_W*2, PLAYER_H*2)), True,False )
UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_flag.png')), (50, 40))
ACTIVE_UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_red.png')), (50, 40))

# player 2 - green
GREEN_PLAYER_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_player.png')), (PLAYER_W, PLAYER_H))
UNIT2_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'unit2.png')), (PLAYER_W *2, PLAYER_H*2))
UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_flag.png')), (50, 40))
ACTIVE_UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_green.png')), (50, 40))

# arrows and barriers
ARROW1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'arrow1.png')), (ARROW_W, ARROW_H))
RIVER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'river.png')), (120, HEIGHT))
BOLDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bolder.png')), (90, 70))

# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'title_bg5.png')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg1.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battle_map_bg.png')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG, '3':BATTLEMAP_BG}

# color
color_dict = {'white':(255,255,255), 'yellow':(255,255,0), 'blue':(0,0,255), 'black':(0,0,0), 'green': (0,255,0), 'red':(255,0,0)}
text_dict = { 
    '1': {
        "title": "Chaos Kingdom",
        "prompt": "Press the spacebar to start",
        'size': 50
    },
    '2':{
        'title': 'How to play',
        'prompt': 'This is where the dicription of the game and how everything works will go.'
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
        },
        'winner':''
    }
}
city_dict = {
    "Utrila": {
        'owner': 'red',
        'x_cord': 836,
        'y_cord': 220,
        'city_num': 1,
        'active': True ,
        'linked_cities': ['Yido', 'Ipria']   
        },
    "Gishire": {
        'owner': 'green',
        'x_cord': 95,
        'y_cord': 300,
        'city_num': 2,
        'active': True ,
        'linked_cities': ['Tetgas','Sheaford']   
        },
    "Tetgas": {
        'owner': 'None',
        'x_cord': 320,
        'y_cord': 212,
        'city_num': 3,
        'active': False,
        'linked_cities': ['Gishire','Plecdiff','Oreledo']    
        },
    "Oreledo": {
        'owner': 'None',
        'x_cord': 395,
        'y_cord': 300,
        'city_num': 4,
        'active': False,
        'linked_cities': ['Tetgas','Strinta', 'Inphis']    
        },
    "Plecdiff": {
        'owner': 'None',
        'x_cord': 460,
        'y_cord': 185,
        'city_num': 5,
        'active': False,
        'linked_cities': ['Tetgas','Strinta']    
        },
    "Strinta": {
        'owner': 'None',
        'x_cord': 518,
        'y_cord': 242,
        'city_num': 6,
        'active': False,
        'linked_cities': ['Plecdiff', 'Oreledo', 'Yido','Ipria']    
        },
    "Yido": {
        'owner': 'None',
        'x_cord': 830,
        'y_cord': 100,
        'city_num': 7,
        'active': False,
        'linked_cities': ['Strinta','Utrila']    
        },
    "Ipria": {
        'owner': 'None',
        'x_cord': 627,
        'y_cord': 343,
        'city_num': 8,
        'active': False,
        'linked_cities': ['Strinta','Zhento', 'Zhento']    
        },
    "Zhento": {
        'owner': 'None',
        'x_cord': 765,
        'y_cord': 450,
        'city_num': 9,
        'active': False,
        'linked_cities': ['Ipria', 'Uleron']    
        },
    "Uleron": {
        'owner': 'None',
        'x_cord': 374,
        'y_cord': 478,
        'city_num': 10,
        'active': False,
        'linked_cities': ['Zhento','Inphis']
    },
    "Inphis": {
        'owner': 'None',
        'x_cord': 334,
        'y_cord': 347,
        'city_num': 11,
        'active': False,
        'linked_cities': ['Oreledo','Uleron', 'Glavine']
    },
    "Glavine": {
        'owner': 'None',
        'x_cord': 295,
        'y_cord': 317,
        'city_num': 12,
        'active': False,
        'linked_cities': ['Inphis','Sheaford']
    },
    "Sheaford": {
        'owner': 'None',
        'x_cord': 205,
        'y_cord': 400,
        'city_num': 13,
        'active': False,
        'linked_cities': ['Gishire','Galvine']
    }
}
###################### end of Game settings and imports section ##############

###################### Gameboard gameplay ####################################

# class for active marker?
    # color
    # city location
    # linked cities 

    # move the active token
        # is the city is located in linked cities of the current city location 


# class for Cities 
    # name
    # owner
    # active
    # city connections
    # coordinates

    # handle when a player attacks (self, who is attacking)
        # if the city has an owner not equal to teh current owner
            # launch a battlemap
                # set current owner to winner 
                    # change owner method
                # if they won do nothing 
        # if the city doesnt have an owner
            # change the owner function
            # change active status

    # change owner (self, who is attacking )
        # if the city owner is none
            # set self.owner to attacker color 
        # if the owner color is red
            # change the owner color to green
        # if the owner color is equal to green
            # change the owner color to red

    # change active status (self)
        # set self.status to opposite
        # if self.active equals True
            # set active to false
        # if status equals false
            # set status to true  

def draw_gameboard():
    """"starts the gamboard commands"""
    run=True
    clock = pygame.time.Clock()
   
    while run:
        red_owned = []
        green_owned = []
        clock.tick(FPS)
        WIN.blit(GAME_BOARD_BG, (0,0))
        # assigns name and flags to cities
        for name in city_dict:
            if city_dict[name]['owner'] == 'red' and name not in red_owned:
                red_owned.append(name)
            elif city_dict[name]['owner'] == 'green' and name not in green_owned:
                green_owned.append(name)

            city_name = city_font.render(name,1,color_dict['white'])
            if city_dict[name]['owner'] == 'red':
                if city_dict[name]['active'] == True:
                    WIN.blit(ACTIVE_UNIT1_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                elif city_dict[name]['active'] == False:
                    WIN.blit(UNIT1_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'],city_dict[name]['y_cord'] - (UNIT2_FLAG.get_height() - 20)))
            elif city_dict[name]['owner'] == 'green':
                if city_dict[name]['active'] == True:
                    WIN.blit(ACTIVE_UNIT2_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                elif city_dict[name]['active'] == False:
                    WIN.blit(UNIT1_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'],city_dict[name]['y_cord'] - (UNIT2_FLAG.get_height() - 20)))
            else:
                WIN.blit(NEUTRAL_FLAG, (city_dict[name]['x_cord'],city_dict[name]['y_cord']))
                WIN.blit(city_name, (city_dict[name]['x_cord'], city_dict[name]['y_cord'] - city_name.get_height() + 10))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_6]:
                draw_battlemap(text_dict['3'])

            green_cities = ammo_count_font.render(str(len(green_owned)),1, color_dict['black'])
            WIN.blit(green_cities, (860, HEIGHT - ammo_count_font.get_height() - 10))
            red_cities = ammo_count_font.render(str(len(red_owned)),1, color_dict['black'])
            WIN.blit(red_cities, (100, HEIGHT - ammo_count_font.get_height() - 10))
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
                arrow = Arrow(self.x + GREEN_PLAYER_IMG.get_width(), self.y + GREEN_PLAYER_IMG.get_height()/2, pygame.transform.rotate(ARROW1, 180), self.color)
            else:
                arrow = Arrow(self.x, self.y + RED_PLAYER_IMG.get_height()/2, ARROW1, self.color)
            self.arrows.append(arrow)
            print(self.mag)
            self.mag -= 1
            self.fire_rate = 1
        elif self.mag == 1:
            self.reload_gun()

    def reload_gun(self):
        """relaods the gun after a set amount of time"""
        self.mag = 15
        print('hit reload')

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

def draw_battlemap(input):
    """starts the battlemap commands"""
    green_player = Player(50, HEIGHT - (GREEN_PLAYER_IMG.get_height() + 50) ,GREEN_PLAYER_IMG , 'green')
    red_player = Player(WIDTH - (RED_PLAYER_IMG.get_width()+50),100,RED_PLAYER_IMG, 'red')
    player_vel = 6
    winner_text = ''
    run = True
    pygame.display.update()

    while winner_text == '' and run:
        WIN.blit(BATTLEMAP_BG,(0,0))
        def draw_winner(text):
            """handles player winning"""
            draw_text = winner_font.render(text, 1, color_dict['white'])
            WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT /2 - draw_text.get_height() /2 ))
            pygame.display.update()
            pygame.time.delay(5000)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False

        # handles the player movement and limits the players movement to their perspective boxes
        if keys[pygame.K_a] and green_player.x + player_vel > 0:
            green_player.move('left', player_vel)
        if keys[pygame.K_d] and green_player.x + player_vel + PLAYER_W < WIDTH / 2 - RIVER.get_width() / 2:
            green_player.move('right', player_vel)
        if keys[pygame.K_w] and green_player.y > 20:
            green_player.move('up', player_vel)
        if keys[pygame.K_s] and green_player.y + player_vel + PLAYER_H < HEIGHT :
            green_player.move('down', player_vel)
        if keys[pygame.K_LEFT] and red_player.x + player_vel + PLAYER_W > WIDTH / 2 + RIVER.get_width() + PLAYER_W:
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
        WIN.blit(RIVER, (WIDTH/2 - RIVER.get_width()/2, 10))
        for key in input:
            # draws greens info
            if key == 'green':
                green_ammo_count = ammo_count_font.render(str(green_player.mag),1, color_dict['green'])
                WIN.blit(green_ammo_count, (WIDTH - WIDTH/2 - green_ammo_count.get_width() - 50,10))
                for i in range(0, 3-len(green_player.cover_built)):
                    WIN.blit(BOLDER,(BOLDER.get_width() * i, 10))

            # draws reds info
            if key == 'red':
                red_ammo_count = ammo_count_font.render(str(red_player.mag),1,color_dict['red'])
                WIN.blit(red_ammo_count, (WIDTH/2 + red_ammo_count.get_width(), 10))
                for i in range(0, 3-len(red_player.cover_built)):
                    WIN.blit(BOLDER,(WIDTH - (BOLDER.get_width() * (i+1)), 10))

        # draws the players on the screen
        green_player.draw(WIN)
        red_player.draw(WIN)

        # update winner
        if green_player.health == 0:
            winner_text = 'red player wins!!'
        if red_player.health == 0:
            winner_text = 'Green player wins!!'
        if winner_text != '':
            draw_winner(winner_text)

        pygame.display.update()
############################ End of battlemap section ########################

def draw_main_menu(input = 1):
    """draws the main menu and runs the commands"""
    WIN.blit(MAIN_MENU_BG, (0,0))
    title = main_font.render(text_dict[str(input)]['title'], 1, color_dict['white'])
    prompt = main_font.render(text_dict[str(input)]['prompt'], 1, color_dict['white'])
    WIN.blit(title, (WIDTH/2 - title.get_width()/2,10))
    WIN.blit(prompt, (WIDTH/2 - prompt.get_width()/2 ,HEIGHT/2))

def main():
    """This is the main menu handling initial game events"""
    clock = pygame.time.Clock()
    run = True
    draw_main_menu()

    while run:
        # draw main menu background
        clock.tick(FPS)
        # default quit function in loop
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_RSHIFT]:
                draw_main_menu(2)
            if keys[pygame.K_SPACE]:
                draw_gameboard()
        draw_main_menu()

        pygame.display.update()

# only runs the game if the file name is "main"
if __name__ == '__main__':
    main()