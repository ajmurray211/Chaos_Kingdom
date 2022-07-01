from typing import Type
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# events to handle hits
YELLOW_HIT = pygame.USEREVENT +1
BLUE_HIT = pygame.USEREVENT +2

# import font
main_font = pygame.font.SysFont('comicsans', 30)
ammo_count_font = pygame.font.SysFont('comicsans', 60)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size
PLAYER_W, PLAYER_H = 70, 70
BULLET_W, BULLET_H = 10, 10

## Import pictures and set colors ##
NEUTRAL_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_flag.png')), (50, 40))
# player 1 - red
BLUE_PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player.png')), (PLAYER_W, PLAYER_H))
UNIT1_IMG = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'unit1.png')), (PLAYER_W*2, PLAYER_H*2)), True,False )
UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_flag.png')), (50, 40))
# player 2 - green
YELLOW_PLAYER_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yellow_player.png')), (PLAYER_W, PLAYER_H))
UNIT2_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'unit2.png')), (PLAYER_W *2, PLAYER_H*2))
UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_flag.png')), (50, 40))

# Bullet
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bullet.png')), (BULLET_W, BULLET_H))
BARB_WIRE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'barb_wire.png')), (40, HEIGHT))
BARB_WIRE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'barb_wire.png')), (40, HEIGHT))
SAND_BAGS = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sand_bags.png')), (90, 70))
# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu_bg.jpeg')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg1.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
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
        'blue':{
            'ammo': 15,
            'structures': 3,
            'health': 100
        },
        'yellow':{
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
        'city_num': 1
    },
    "Gishire": {
        'owner': 'green',
        'x_cord': 95,
        'y_cord': 300,
        'city_num': 2
    },
    "Tetgas": {
        'owner': 'None',
        'x_cord': 320,
        'y_cord': 212,
        'city_num': 3
    },
    "Oreledo": {
        'owner': 'None',
        'x_cord': 395,
        'y_cord': 300,
        'city_num': 4
    },
    "Plecdiff": {
        'owner': 'None',
        'x_cord': 460,
        'y_cord': 185,
        'city_num': 5
    },
    "Strinta": {
        'owner': 'None',
        'x_cord': 518,
        'y_cord': 242,
        'city_num': 6
    },
    "Yido": {
        'owner': 'None',
        'x_cord': 830,
        'y_cord': 100,
        'city_num': 7
    },
    "Ipria": {
        'owner': 'None',
        'x_cord': 627,
        'y_cord': 343,
        'city_num': 8
    },
    "Zhento": {
        'owner': 'None',
        'x_cord': 765,
        'y_cord': 450,
        'city_num': 9
    },
    "city_name": {
        'owner': 'None',
        'x_cord': 374,
        'y_cord': 478,
        'city_num': 10
    },
    "Inphis": {
        'owner': 'None',
        'x_cord': 334,
        'y_cord': 347,
        'city_num': 11
    },
    "Glavine": {
        'owner': 'None',
        'x_cord': 295,
        'y_cord': 317,
        'city_num': 12
    },
    "Sheaford": {
        'owner': 'None',
        'x_cord': 205,
        'y_cord': 400,
        'city_num': 13
    }
}

## Battlemap gameplay ##

class Player:
    MAX_FIRE_RATE = 25
    def __init__(self,x, y, player_img, color, health =100):
        self.x =x
        self.y =y
        self.color =color
        self.player_img = player_img
        self.mask = pygame.mask.from_surface(self.player_img)
        self.bullets = []
        self.cover_built = []
        self.health = health
        self.max_health = 100
        self.fire_rate = 0
        self.build_rate = 0
        self.mag = text_dict['3'][self.color]['ammo']
        self.cover_count =text_dict['3'][self.color]['structures']

    def draw(self, window):
        """draws the player, and calls bullets, structures and health draw methods"""
        window.blit(self.player_img, (self.x,self.y))
        self.healthbar(window)
        self.move_bullets()
        for bullet in self.bullets:
            bullet.draw(window)
        for cover in self.cover_built:
            cover.draw()

    def shoot(self, inverse = False):
        """shoots a bullet"""
        if self.mag >= 0 and self.fire_rate == 0:
            if inverse:
                bullet = Bullet(self.x + YELLOW_PLAYER_IMG.get_width(), self.y + YELLOW_PLAYER_IMG.get_height()/2, pygame.transform.rotate(BULLET, 180), self.color)
            else:
                bullet = Bullet(self.x, self.y + BLUE_PLAYER_IMG.get_height()/2, BULLET, self.color)
            self.bullets.append(bullet)
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

    def move_bullets(self, vel = 7):
        """moves a players bullets, until it is off screen then it deletes"""
        self.cool_down()
        for bullet in self.bullets:
            bullet.move_b(vel)
            if bullet.off_screen():
                self.bullets.remove(bullet)

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
                    cover = Structure(self.x - BLUE_PLAYER_IMG.get_width(), self.y + 10,pygame.transform.rotate(SAND_BAGS, 180))
                else:
                    cover = Structure(self.x + YELLOW_PLAYER_IMG.get_width(), self.y, SAND_BAGS)
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

# class for bullet
class Bullet:
    def __init__(self, x, y, img, color):
        self.x = x
        self.y = y
        self.img = img
        self.color = color
        self.mask = pygame.mask.from_surface(self.img) 
        
    def draw(self, window ):
        """draws the bullets"""
        window.blit(self.img, (self.x, self.y))
        self.move_b(vel = 7)
        
    def move_b(self, vel):
        """moves the bullet based on player color"""
        if self.color == 'yellow':
            self.x += vel
        elif self.color == 'blue':
            self.x -= vel

    def off_screen(self):
        """checks to see if a bullet leavs the screen"""
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

def draw_main_menu(input = 1):
    """draws the main menu and runs the commands"""
    WIN.blit(MAIN_MENU_BG, (0,0))
    title = main_font.render(text_dict[str(input)]['title'], 1, color_dict['white'])
    prompt = main_font.render(text_dict[str(input)]['prompt'], 1, color_dict['white'])
    WIN.blit(title, (WIDTH/2 - title.get_width()/2,10))
    WIN.blit(prompt, (WIDTH/2 - prompt.get_width()/2 ,HEIGHT/2))
    WIN.blit(UNIT1_IMG, (WIDTH- (WIDTH/4),HEIGHT-200))
    WIN.blit(UNIT2_IMG, (WIDTH/6,HEIGHT-200))

def draw_gameboard():
    """"starts the gamboard commands"""
    run=True
    while run:
        WIN.blit(GAME_BOARD_BG, (0,0))
        # assigns flags to citys by color
        for city in city_dict:
            if city_dict[city]['owner'] == 'red':
                WIN.blit(UNIT1_FLAG, (city_dict[city]['x_cord'],city_dict[city]['y_cord']))
            elif city_dict[city]['owner'] == 'green':
                WIN.blit(UNIT2_FLAG, (city_dict[city]['x_cord'],city_dict[city]['y_cord']))
            else:
                WIN.blit(NEUTRAL_FLAG, (city_dict[city]['x_cord'],city_dict[city]['y_cord']))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_6]:
                draw_battlemap(text_dict['3'])
            pygame.display.update()

def draw_battlemap(input):
    """starts the battlemap commands"""
    yellow_player = Player(50, HEIGHT - (YELLOW_PLAYER_IMG.get_height() + 50) ,YELLOW_PLAYER_IMG , 'yellow')
    blue_player = Player(WIDTH - (BLUE_PLAYER_IMG.get_width()+50),100,BLUE_PLAYER_IMG, 'blue')
    player_vel = 6
    winner_text = ''
    run = True

    while winner_text == '' and run:
        WIN.blit(BATTLEMAP_BG,(0,0))
        def draw_winner(text):
            """handles player winning"""
            draw_text = WINNER_FONT.render(text, 1, color_dict['white'])
            WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT /2 - draw_text.get_height() /2 ))
            pygame.display.update()
            pygame.time.delay(5000)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
        # handles the player movement and limits the players movement to their perspective boxes
        if keys[pygame.K_a] and yellow_player.x + player_vel > 0:
            yellow_player.move('left', player_vel)
        if keys[pygame.K_d] and yellow_player.x + player_vel + PLAYER_W < WIDTH / 2 - BARB_WIRE.get_width() / 2:
            yellow_player.move('right', player_vel)
        if keys[pygame.K_w] and yellow_player.y > 20:
            yellow_player.move('up', player_vel)
        if keys[pygame.K_s] and yellow_player.y + player_vel + PLAYER_H < HEIGHT :
            yellow_player.move('down', player_vel)
        if keys[pygame.K_LEFT] and blue_player.x + player_vel + PLAYER_W > WIDTH / 2 + BARB_WIRE.get_width() + PLAYER_W:
            blue_player.move('left', player_vel)
        if keys[pygame.K_RIGHT] and blue_player.x + player_vel < WIDTH - PLAYER_W:
            blue_player.move('right', player_vel)
        if keys[pygame.K_UP] and blue_player.y > 20:
            blue_player.move('up', player_vel)
        if keys[pygame.K_DOWN]and blue_player.y + player_vel + PLAYER_H < HEIGHT:
            blue_player.move('down', player_vel)
        if keys[pygame.K_v]:
            yellow_player.build()
        if keys[pygame.K_n]:
            blue_player.build(True)
        if keys[pygame.K_c]:
            yellow_player.shoot(True)
        if keys[pygame.K_m]:
            blue_player.shoot()
        
        # checks to see if a bullet hits a player or structure
        for bullet in yellow_player.bullets:
            if blue_player.hit(bullet):
                blue_player.health -= 10 
                yellow_player.bullets.remove(bullet)
            for build in blue_player.cover_built:
                if build.hit(bullet) and build.health > 0:
                    build.health -= 10 
                    yellow_player.bullets.remove(bullet)
                elif build.health <= 0:
                    blue_player.cover_built.remove(build)
        for bullet in blue_player.bullets:
            if yellow_player.hit(bullet):
                yellow_player.health -= 10 
                blue_player.bullets.remove(bullet)
            for build in yellow_player.cover_built:
                if build.hit(bullet) and build.health > 0:
                    build.health -= 10 
                    blue_player.bullets.remove(bullet)
                elif build.health <= 0:
                    yellow_player.cover_built.remove(build)

        # draws the barbed wire/ sandbags/ ammo_count
        WIN.blit(BARB_WIRE, (WIDTH/2 - BARB_WIRE.get_width()/2, 10))
        for key in input:
            # draws yellows info
            if key == 'yellow':
                yellow_ammo_count = ammo_count_font.render(str(yellow_player.mag),1, color_dict['yellow'])
                WIN.blit(yellow_ammo_count, (WIDTH - WIDTH/2 - yellow_ammo_count.get_width() - 50,10))
                for i in range(0, 3-len(yellow_player.cover_built)):
                    WIN.blit(SAND_BAGS,(SAND_BAGS.get_width() * i, 10))

            # draws blues info
            if key == 'blue':
                blue_ammo_count = ammo_count_font.render(str(blue_player.mag),1,color_dict['blue'])
                WIN.blit(blue_ammo_count, (WIDTH/2 + blue_ammo_count.get_width(), 10))
                for i in range(0, 3-len(blue_player.cover_built)):
                    WIN.blit(SAND_BAGS,(WIDTH - (SAND_BAGS.get_width() * (i+1)), 10))

        # draws the players on the screen
        yellow_player.draw(WIN)
        blue_player.draw(WIN)

        # update winner
        if yellow_player.health == 0:
            winner_text = 'Blue player wins!!'
        if blue_player.health == 0:
            winner_text = 'Yellow player wins!!'
        if winner_text != '':
            draw_winner(winner_text)

        pygame.display.update()

### This is the process for filtering multiple screens ###
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

        pygame.display.update()

# only runs the game if the file name is "main"
if __name__ == '__main__':
    main()