import pygame
import random
from Tokens.inventory import Inventory

class Token:

    def __init__(self, x, y, w, h):
        self.dead = False
        self.hitbox = pygame.Rect(x, y, w, h)
        self.velocity = pygame.Vector2(0, 0)
        self.is_on_ground = False
        self.collisions = []
        self.transparent = False
        self.facing_left = False

    def is_dead(self):
        return self.dead

    def update(self, tokens):
        pass

    def render(self, g):
        pass

    def collides(self, token):
        return self.hitbox.colliderect(token.hitbox)

    def moveX(self, dt):
        self.hitbox.x += self.velocity.x #* dt

    def moveY(self, dt):
        self.hitbox.y += self.velocity.y #* dt

    def add_collisions(self, collisions):
        self.collisions += collisions

    def reset_collisions(self):
        self.collisions = []

    def set_transparent(self, val):
        self.transparent = val

    def __repr__(self):
        return self.__class__.__name__ + " " + str(self.transparent)

class Player(Token):

    def __init__(self, tokens):
        super().__init__(100, 100, 40, 100)
        self.speed = 10
        self.inventory = Inventory()
        self.item_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
        starting_item = ElectroShock(self.hitbox.x, self.hitbox.y+self.hitbox.height/2, tokens, True, self)
        starting_item.state = 1
        self.inventory.add(starting_item)
        self.inventory_render_type = True
        self.space_pressed_prev_frame = False 

    def update(self, tokens):
        
        self.velocity.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed 
            self.facing_left = True 
        if keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.facing_left = False
        if keys[pygame.K_w] and self.is_on_ground:
            self.velocity.y = -25
        if not keys[pygame.K_SPACE] and self.space_pressed_prev_frame:
            self.inventory_render_type = not self.inventory_render_type
        self.space_pressed_prev_frame = keys[pygame.K_SPACE]

        for index, key in enumerate(self.item_keys):
            if keys[key]:
                item = self.inventory.use(index)
                if item is not None:
                    item.use(self, tokens)

        if self.is_on_ground and self.velocity.y >= 1:
            self.velocity.y = 0
        else:
            self.velocity.y += 1
            if self.velocity.y > 3:
                self.velocity.y += 0.5

            if self.velocity.y > 7:
                self.velocity.y = 7

        self.is_on_ground = False

    def render(self, g):
        pygame.draw.rect(g, (255, 0, 0), self.hitbox)
        if self.inventory_render_type:
            self.inventory.render_bar(g)
        else:
            self.inventory.render_full(g)

class Platform(Token):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def render(self, g):
        pygame.draw.rect(g, (255, 255, 0), self.hitbox)

class Enemy(Token):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def AI(self, tokens):
        pass

    def get_drop(self, tokens):
        drops = self.get_drops(tokens)
        return random.choice(drops)
    
    def get_drops(self):
        pass

    def render(self, g):
        pygame.draw.rect(g, (100, 100, 0), self.hitbox)

    def update(self, tokens):
        self.AI(tokens)

        if self.is_on_ground and self.velocity.y >= 1:
            self.velocity.y = 0
        else:
            self.velocity.y += 1
            if self.velocity.y > 3:
                self.velocity.y += 0.5

            if self.velocity.y > 7:
                self.velocity.y = 7

        self.is_on_ground = False

    def get_player(self, tokens):
        return tokens[0]

class Zombie(Enemy):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.cooldown()

    def AI(self, tokens):
        
        player = self.get_player(tokens)
        if (player.hitbox.x > self.hitbox.x):
            self.velocity.x = 1
        else:
            self.velocity.x = -1

        self.ticks -= 1
        if(self.ticks < 0):
            self.cooldown()
            projectile = FireBall(self.hitbox.x, self.hitbox.y+self.hitbox.width/2, self.velocity.x == -1, tokens, False)
            projectile.state = 2
            #tokens.append(projectile)

    def cooldown(self):
        self.ticks = random.randint(1, 3) * 60 
    
    def get_drops(self, tokens):
        return [FireBall(self.hitbox.x, self.hitbox.y, False, tokens, True)]

class Item(Token):

    def __init__(self, x, y, w, h, left, tokens, friendly):
        super().__init__(x, y, w ,h)
        self.state = 0
        self.set_transparent(True)
        self.left = left
        self.tokens = tokens
        self.friendly = friendly

    def start_drop(self):
        self.velocity.y = -10

    def update(self, tokens):
        
        if self.state == 0:
            self.dropped(tokens)
        elif self.state == 1:
            self.picked(tokens)
        else:
            self.active(tokens)

    def active(self, tokens):
        pass

    def dropped(self, tokens):

        if tokens[0] in self.collisions:
            if(tokens[0].inventory.add(self)):
                self.state = 1
                self.velocity.y = 0
            else:
                self.state = 0

        if self.is_on_ground and self.velocity.y >= 1:
            self.velocity.y = 0
        else:
            self.velocity.y += 1
            if self.velocity.y > 3:
                self.velocity.y += 0.5

            if self.velocity.y > 7:
                self.velocity.y = 7

        self.is_on_ground = False

    def picked(self, tokens):
       pass 

    def use(self, token, tokens):
        tokens.append(self)
        self.state = 2
        self.friendly = isinstance(token, Player)
        self.left = token.facing_left
        self.hitbox.x = token.hitbox.x
        self.hitbox.y = token.hitbox.y

    def kill(self):

        if self.friendly:

            for coll in self.collisions:
                if isinstance(coll, Enemy):
                    coll.dead = True
                    self.dead = True
        else:
            for coll in self.collisions:
                if isinstance(coll, Player):
                    coll.dead = True
                    self.dead = True

    def dropped_render(self, g):
        pygame.draw.rect(g, (0,0,0), self.hitbox)

    def active_render(self, g):
        pass

    def render(self, g):

        if self.state == 0:
            self.dropped_render(g)
        elif self.state == 2:
            self.active_render(g)

class FireBall(Item):


    def __init__(self, x, y, left, tokens, friendly):
        super().__init__(x, y, 30, 30, left, tokens, friendly)
        self.speed = random.randint(3, 6)

    def active(self, tokens):
        
        if self.left:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = self.speed

        if self.hitbox.x < 0 or self.hitbox.x > 1080:
            self.dead = True
        self.kill()


    def active_render(self, g):
        pygame.draw.rect(g, (255, 255, 255), self.hitbox)

    def use(self, token, tokens):
        super().use(token, tokens)
        self.velocity.x = 0
        self.velocity.y = 0
        self.hitbox.y = token.hitbox.y + (token.hitbox.height / 2 - self.hitbox.height / 2)

class ElectroShock(Item):
    
    def __init__(self, x, y, tokens, friendly, user):
        super().__init__(x, y, user.hitbox.width, user.hitbox.height, False, tokens, friendly)
        self.user = user
        self.ticks = 60

    def active(self, tokens):
        
        if self.friendly:
            self.user = tokens[0]
        
        if self.user.velocity.x < 0:
            self.hitbox.x = self.user.hitbox.x - self.hitbox.width
        elif self.user.velocity.x > 0:
            self.hitbox.x = self.user.hitbox.x + self.user.hitbox.width

        self.hitbox.y = self.user.hitbox.y
        self.kill()

        self.ticks -= 1
        if self.ticks  < 0:
            self.dead = True

    def active_render(self, g):
        pygame.draw.rect(g, (0,0,0), self.hitbox)


