from Tokens.token import Token, Player, Platform
import pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

tokens = [Player(), Platform(50, 400, 200, 10)]
dt = 0


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
        for collision in collisions:
            if token.velocity.x > 0:
                token.hitbox.x = collision.hitbox.x - token.hitbox.w
            if token.velocity.x < 0:
                token.hitbox.x = collision.hitbox.x + collision.hitbox.w
    if token.velocity.y != 0:
        token.moveY(dt)
        collisions = get_all_collisions(token)
        for collision in collisions:
            if token.velocity.y > 0:
                #print("Collision")
                token.hitbox.y = collision.hitbox.y - token.hitbox.h
            if token.velocity.y < 0:
                token.hitbox.y = collision.hitbox.y + collision.hitbox.h
                #print("Collision")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("gray")

    for token in tokens:
        token.update()

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

