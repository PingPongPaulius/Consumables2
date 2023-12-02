import pygame
class Token:

    def __init__(self, x, y, w, h):
        self.dead = False
        self.hitbox = pygame.Rect(x, y, w, h)
        self.velocity = pygame.Vector2(0, 0)

    def is_dead(self):
        return self.dead

    def update(self):
        pass

    def render(self, g):
        pass

    def collides(self, token):
        return self.hitbox.colliderect(token.hitbox)

    def moveX(self, dt):
        self.hitbox.x += self.velocity.x# * dt

    def moveY(self, dt):
        self.hitbox.y += self.velocity.y# * dt

class Player(Token):

    def __init__(self):
        super().__init__(100, 100, 40, 100)
    
    def update(self):
        self.velocity.y = 1

    def render(self, g):
        pygame.draw.rect(g, (255, 0, 0), self.hitbox)

class Platform(Token):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        

    def render(self, g):
        pygame.draw.rect(g, (255, 255, 0), self.hitbox)
