from Tokens.token import *
import pygame
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

tokens = [Player(), Platform(50, 400, 200, 10), Platform(0, 550, 1280, 40), Gamer(400, 400, 40, 100)]
dt = 0
camera_scroll_speed = 1
half_camera_boundry = 300

def get_all_collisions(movable):
    
    collisions = []
    for token in tokens:
        if token != movable and movable.collides(token):
            collisions.append(token)

    return collisions

def move(token):

    if token.velocity.x != 0:
        token.moveX(dt)
        collisions = get_all_collisions(token)
        token.add_collisions(collisions)
        for collision in collisions:
            if token.velocity.x > 0:
                token.hitbox.x = collision.hitbox.x - token.hitbox.w
            if token.velocity.x < 0:
                token.hitbox.x = collision.hitbox.x + collision.hitbox.w
    if token.velocity.y != 0:
        token.moveY(dt)
        collisions = get_all_collisions(token)
        token.add_collisions(collisions)
        for collision in collisions:
            if token.velocity.y > 0:
                if isinstance(token, Player):
                    token.is_on_ground = True
                token.hitbox.y = collision.hitbox.y - token.hitbox.h
            if token.velocity.y < 0:
                token.velocity.y = 0
                token.hitbox.y = collision.hitbox.y + collision.hitbox.h

def handle_camera():

    if(isinstance(tokens[0], Player)):
        player = tokens[0]

        if player.hitbox.x > SCREEN_WIDTH/2 - half_camera_boundry:
            for token in tokens:
                token.hitbox.x -= (player.speed - camera_scroll_speed)

        if player.hitbox.x < SCREEN_HEIGHT/2 + half_camera_boundry:
            for token in tokens:
                 token.hitbox.x += (player.speed - camera_scroll_speed)

    else:
        print("main.py/handle_camera !! DEBUG:  Player is not index 0")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("gray")

    for token in tokens:
        token.update(tokens)
        token.reset_collisions()
    
    handle_camera()
    
    for token in tokens:
        move(token)

    for token in tokens:
        token.render(screen)

    for token in reversed(tokens):
        if token.is_dead():
            tokens.remove(token)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

