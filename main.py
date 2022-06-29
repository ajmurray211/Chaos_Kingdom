
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# set border 
# import font
main_font = pygame.font.SysFont('comicsans', 30)
ammo_count_font = pygame.font.SysFont('comicsans', 60)
# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size
PLAYER_W, PLAYER_H = 70, 70
BULLET_W, BULLET_H = 10, 10

## Import pictures and set colors ##
# player 1
BLUE_PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player.png')), (PLAYER_W, PLAYER_H))
# player 2
YELLOW_PLAYER_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yellow_player.png')), (PLAYER_W, PLAYER_H))
# Bullet
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bullet.png')), (BULLET_W, BULLET_H))
BARB_WIRE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'barb_wire.png')), (40, HEIGHT))
BARB_WIRE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'barb_wire.png')), (40, HEIGHT))
SAND_BAGS = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sand_bags.png')), (90, 70))
# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu_bg.jpeg')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG, '3':BATTLEMAP_BG}

# color
color_dict = {'white':(255,255,255), 'yellow':(255,255,0), 'blue':(0,0,255), 'black':(0,0,0), 'green': (0,255,0), 'red':(255,0,0)}
text_dict = { 
    '1': {
        "title": "Chaos Kingdom",
        "prompt": "Press any key to start",
        'size': 50
    },
    '2':{
        'title': 'Game Board',
        'size': 100
    },
    '3':{   
        'title': "Battle map",
        'blue':{
            'ammo': 5,
            'structures': 3,
            'health': 100
        },
        'yellow':{
            'ammo': 5,
            'structures': 3,
            'health': 100
        }
    }
}

## Battlemap gameplay ##
# player class
class Player:
    MAX_FIRE_RATE = 30
    def __init__(self,x, y, player_img, color, health =100):
        self.x =x
        self.y =y
        self.color =color
        self.player_img = player_img
        self.mask = pygame.mask.from_surface(self.player_img)
        self.bullets = []
        self.health = health
        self.max_health = 100
        self.fire_rate = 0
        self.mag = text_dict['3'][self.color]['ammo']

    # def to draw a player on the screen
    def draw(self, window):
        window.blit(self.player_img, (self.x,self.y))
        self.healthbar(window)
        # self.reload_gun()
        for bullet in self.bullets:
            bullet.draw(window)
            if bullet.x>WIDTH or bullet.x<0:
                self.bullets.remove(bullet)
                print(self.bullets)

    def reload_gun(self):
        if self.mag == 1:
            self.mag == 5
        else:
            self.mag -=1

    # def to shoot
    def shoot(self, inverse = False):
        if len(self.bullets ) < self.mag:
            if inverse:
                bullet = Bullet(self.x + YELLOW_PLAYER_IMG.get_width(), self.y + YELLOW_PLAYER_IMG.get_height()/2, pygame.transform.rotate(BULLET, 180), self.color)
            else:
                bullet = Bullet(self.x, self.y + BLUE_PLAYER_IMG.get_height()/2, BULLET, self.color)
            self.bullets.append(bullet)
            self.move_bullets()
            self.reload_gun()
            self.fire_rate = 1

    # def to slow shooting down
    def cool_down(self):
        if self.fire_rate >= self.MAX_FIRE_RATE:
            self.fire_rate = 0
        elif self.fire_rate > 0:
            print(self.fire_rate)
            self.fire_rate += 1

    # def to move bullets
    def move_bullets(self, vel = 7):
        self.cool_down()
        for bullet in self.bullets:
            bullet.move_b(vel)

    # def to move the player
    def move(self, direction, player_vel):
        if direction == 'right':
            self.x += player_vel
        if direction == 'left':
            self.x -= player_vel
        if direction == 'up':
            self.y -= player_vel
        if direction == 'down':
            self.y += player_vel

    # def for being hit 

    # def for healthbar
    def healthbar(self, window):
        pygame.draw.rect(window, color_dict['red'], (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(window, color_dict['green'], (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width() * (self.health / self.max_health), 10))

# class for bullet
class Bullet:
    def __init__(self, x, y, img, color):
        self.x = x
        self.y = y
        self.img = img
        self.color = color
        self.mask = pygame.mask.from_surface(self.img) 
        
    # def for drawing bullets in self.list
    def draw(self, window ):
        window.blit(self.img, (self.x, self.y))
        self.move_b(vel = 7)
        
    # def for moving bullets
    def move_b(self, vel):
        if self.color == 'yellow':
            self.x += vel
        elif self.color == 'blue':
            self.x -= vel

    # def for collision
    # def for offscreen
    def off_screen(self):
        return (self.x > WIDTH or self.x <0)

# def to draw the winner text

# def to draw main_menu
def draw_main_menu(input):
    title = main_font.render(input['title'], 1, color_dict['white'])
    prompt = main_font.render(input['prompt'], 1, color_dict['white'])
    WIN.blit(title, (WIDTH/2 - title.get_width()/2,10))
    WIN.blit(prompt, (WIDTH/2 - prompt.get_width()/2 ,HEIGHT/2))

# def to draw gameboard
def draw_gameboard(input):
    main_text = main_font.render(input['title'], 1, (255,255,255))
    WIN.blit(main_text, (10,10))

# def to draw battle map
def draw_battlemap(input, yellow_player, blue_player, player_vel):
    """handles the battle map game"""
    keys = pygame.key.get_pressed()

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
    if keys[pygame.K_c]:
        yellow_player.shoot(True)
    if keys[pygame.K_m]:
        blue_player.shoot()

    # draws the barbed wire/ sandbags/ ammo_count
    WIN.blit(BARB_WIRE, (WIDTH/2 - BARB_WIRE.get_width()/2, 10))
    for key in input:
        # draws yellows info
        if key == 'yellow':
           yellow_ammo_count = ammo_count_font.render(str(yellow_player.mag),1, color_dict['yellow'])
           WIN.blit(yellow_ammo_count, (WIDTH - WIDTH/2 - yellow_ammo_count.get_width() - 50,10))
           for i in range(0, text_dict['3'][key]['structures']):
               WIN.blit(SAND_BAGS,(SAND_BAGS.get_width() * i, 10))
        # draws blues info
        if key == 'blue':
            blue_ammo_count = ammo_count_font.render(str(blue_player.mag),1,color_dict['blue'])
            WIN.blit(blue_ammo_count, (WIDTH/2 + blue_ammo_count.get_width(), 10))
            for i in range(0, text_dict['3'][key]['structures']):
                WIN.blit(SAND_BAGS,(WIDTH - (SAND_BAGS.get_width() * (i+1)), 10))

    # draws the players on the screen
    yellow_player.draw(WIN)
    blue_player.draw(WIN)
    pygame.display.update()

# def to draw the window
def draw_window(background, curr_index, yellow, blue, player_vel):
    """This method updates the window"""
    WIN.blit(background, (0,0))

    # filter what to display 
    if curr_index == 1:
        draw_main_menu(text_dict['1'])
    if curr_index == 2:
        draw_gameboard(text_dict['2'])
    if curr_index == 3:
        draw_battlemap(text_dict['3'], yellow, blue, player_vel)

    pygame.display.update()

### This is the process for filtering multiple screens ###
def main():
    """This will handle the main events of the game"""
    yellow_player = Player(50, 600 ,YELLOW_PLAYER_IMG , 'yellow')
    blue_player = Player(900,100,BLUE_PLAYER_IMG, 'blue')
    current_bg_index = 1
    player_vel = 4
    run = True

    while run:
        # draw main menu background
        draw_window(BG_DICT[str(current_bg_index)], current_bg_index, yellow_player, blue_player, player_vel)
        # default quit function in loop
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_SPACE]:
                current_bg_index = 2
            if keys[pygame.K_RETURN]:
                current_bg_index = 3
                # draw_battlemap(BG_DICT['3'], yellow_player, blue_player, player_vel)
            if keys[pygame.K_y]:
                current_bg_index = 1

if __name__ == '__main__':
    main()