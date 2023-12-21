import pygame
import random

class Token:

    def __init__(self, x, y, w, h):
        self.dead = False
        self.hitbox = pygame.Rect(x, y, w, h)
        self.velocity = pygame.Vector2(0, 0)
        self.is_on_ground = False
        self.collisions = []
        self.transparent = False

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

    def __init__(self):
        super().__init__(100, 100, 40, 100)
        self.speed = 10
    
    def update(self, tokens):

        self.velocity.x = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -self.speed 
        if keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_w] and self.is_on_ground:
            self.velocity.y = -25

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

class Gamer(Enemy):

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
            tokens.append(FireBall(self.hitbox.x, self.hitbox.y+self.hitbox.width/2, self.velocity.x == -1, tokens, False))

    def cooldown(self):
        self.ticks = random.randint(1, 3) * 60 
    
    def get_drops(self):
        pass

class Item(Token):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w ,h)
        self.state = "PickedUp"
        self.set_transparent(True)

    def update(self, tokens):
        pass

    def render(self, g):
        pass

class FireBall(Item):


    def __init__(self, x, y, left, tokens, friendly):
        super().__init__(x, y, 30, 30)
        self.left = left
        self.tokens = tokens
        self.friendly = friendly
        self.speed = random.randint(3, 6)

    def update(self, tokens):
        
        if self.left:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = self.speed

        if self.hitbox.x < 0 or self.hitbox.x > 1080:
            self.dead = True

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

    def render(self, g):
        pygame.draw.rect(g, (255, 255, 255), self.hitbox)

