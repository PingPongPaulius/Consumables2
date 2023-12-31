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
        self.add_item(starting_item)
        self.add_item(JumpTracker(tokens))
        for i in range(5):
            self.add_item(Teleporter(tokens))
        self.inventory_render_type = True
        self.space_pressed_prev_frame = False 
        self.pressed_frame = [False, False, False, False, False]

    def add_item(self, item):
        starting_item = item
        starting_item.state = 1
        self.inventory.add(starting_item)

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
            if keys[key] and not self.pressed_frame[index]:
                self.pressed_frame[index] = True
                item = self.inventory.use(index)
                if item is not None:
                    item.use(self, tokens)
            elif not keys[key]:
                self.pressed_frame[index] = False

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
        self.id = -1

    def start_drop(self):
        self.velocity.y = -10

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, Item):
            return False
        return self.id == other.id

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

        collided = False
        if self.friendly:
            for coll in self.collisions:
                if isinstance(coll, Enemy):
                    coll.dead = True
                    collided = True
        else:
            for coll in self.collisions:
                if isinstance(coll, Player):
                    coll.dead = True
                    collided = True
        
        return collided

    def dropped_render(self, g):
        pygame.draw.rect(g, (0,0,0), self.hitbox)

    def active_render(self, g):
        pass

    def render(self, g):
        if self.state == 0:
            if self.velocity.y > 0 :
                for c in self.collisions:
                    if isinstance(c, Platform):
                        self.hitbox.y = c.hitbox.y - self.hitbox.height
                        self.is_on_ground = True
                        self.velocity.y = 0
            elif self.velocity.y < 0:
                for c in self.collisions:
                    if isinstance(c, Platform):
                        self.hitbox.y = c.hitbox.y + c.hitbox.height
                        self.is_on_ground = False 
                        self.velocity.y = 0
            self.dropped_render(g)
        elif self.state == 2:
            self.active_render(g)

class FireBall(Item):


    def __init__(self, x, y, left, tokens, friendly):
        super().__init__(x, y, 30, 30, left, tokens, friendly)
        self.speed = random.randint(3, 6)
        self.ticks = 150
        self.id = 1

    def active(self, tokens):
        
        if self.left:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = self.speed

        if self.ticks <= 0:
            self.dead = True
        else:
            self.ticks -= 1
         
        if self.kill():
            self.dead = True

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
        self.id = 2

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

class Teleporter(Item):

    def __init__(self, tokens):
        super().__init__(0,0,1,1, False, tokens, True)
        self.id = 3
    
    def active(self, tokens):
        
        if self.friendly:
            self.user = tokens[0]
        else:
            print("Enemy Teleports")

        mouse_pos = pygame.mouse.get_pos()
        self.user.hitbox.x = mouse_pos[0]
        self.user.hitbox.y = mouse_pos[1]
        self.dead = True

class JumpTracker(Item):

    def __init__(self, tokens):
        super().__init__(0,0,1,1, False, tokens, True)
        self.ticks = 120
        self.pos = []
        self.render_list = []
        self.done = False
        self.id = 4
    
    def active(self, tokens):
        
        if self.done:
            return

        if self.friendly:
            self.user = tokens[0]
        else:
            print("Enemy Teleports")

        self.ticks -= 1
        self.pos.append([self.user.hitbox.x - self.user.hitbox.width/2, self.user.hitbox.y + self.user.hitbox.height/2])

        if self.ticks < 0 and not self.done:
            self.done = True
            curr = self.pos.pop(0)
            repetative = {}
            while len(self.pos) > 0:
                nxt  = self.pos[0] 
                if curr[0] == nxt[0] and curr[1] == nxt[1]:
                    curr = self.pos.pop(0)

                if curr[0] > nxt[0]:
                    curr[0] -= 1
                elif curr[0] < nxt[0]:
                    curr[0] += 1

                if curr[1] > nxt[1]:
                    curr[1] -= 1
                elif curr[1] < nxt[1]:
                    curr[1] += 1

                values = repetative.get(curr[0]) 
                if values is not None:
                    if curr[1] not in values:
                        self.render_list.append(pygame.Rect(curr[0], curr[1], 1, 1))
                        repetative[curr[0]] = repetative[curr[0]].append(curr[1])
                else:
                    repetative[curr[0]] = [curr[1]]
                    self.render_list.append(pygame.Rect(curr[0], curr[1], 1, 1))

            for t in self.render_list:
                tokens.append(DeathParticle(t.x, t.y, 1, 1, 1000))
            
class DeathParticle(Token):

    def __init__(self, x, y, w, h, ticks):
        super().__init__(x, y, w, h)
        self.transparent = True
        self.ticks = ticks

    def update(self, tokens):
            for token in tokens:
                if isinstance(token, Enemy):
                    if self.hitbox.colliderect(token.hitbox):
                        token.dead = True
            self.ticks -= 1
            if self.ticks < 0:
                self.dead = True

    def render(self, g):
        pygame.draw.rect(g, (0,0,0), self.hitbox)


