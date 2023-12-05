import pygame

class Player:
    def __init__(self,x, y, player_img, color, player_vel=3, is_ai = False, health =100):
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
        self.is_ai = is_ai
        self.player_vel = player_vel
        self.angle = 0  # Initialize the angle of rotation
        self.rotated_image = self.player_img 
        self.random_roam_timer = 0
        self.rotation_angle = 0 

    def ai_logic(self, target):
            """AI logic for NPC player"""

            def random_roam(self):
                """make the ai roam in a random direction every few seconds"""
                directions = ['up', 'down', 'left', 'right']
                random_direction = random.choice(directions)
                
                if random_direction == 'up':
                    self.move('up')
                elif random_direction == 'down':
                    self.move('down')
                elif random_direction == 'left':
                    self.move('left')
                elif random_direction == 'right':
                    self.move('right')

            if self.is_ai:
                current_time = pygame.time.get_ticks()
                if current_time - self.random_roam_timer >= 100:  # Check if 3 seconds have passed
                    random_roam(self)
                    self.random_roam_timer = current_time  # Update the timer
                for arrow in target.arrows:
                    if self.hit(arrow):
                        self.move('up')
                
                    if abs(self.y - target.y) <= 100:
                        self.shoot()


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

    def move(self, direction):
        """Controls a player's movement and updates rotation"""
        if direction == 'right':
            self.x += self.player_vel
            self.rotation_angle = 90
        elif direction == 'left':
            self.x -= self.player_vel
            self.rotation_angle = 270
        elif direction == 'up':
            self.y -= self.player_vel
            self.rotation_angle = 0
        elif direction == 'down':
            self.y += self.player_vel
            self.rotation_angle = 180

        # Rotate the image based on the updated angle
        self.rotated_image = pygame.transform.rotate(self.player_img, self.rotation_angle)

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
