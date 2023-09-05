import pygame
import sys
import random

from pygame import mixer


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = random.randint(0, 1)

        if self.direction == 0:
            e1 = pygame.image.load("gameFiles/enemy1.png").convert_alpha()
            e2 = pygame.image.load("gameFiles/enemy2.png").convert_alpha()
            self.sprites = [e1, e2]
            self.enemy_x = -150
            print("0")
        elif self.direction == 1:
            e3 = pygame.image.load("gameFiles/enemy3.png").convert_alpha()
            e4 = pygame.image.load("gameFiles/enemy4.png").convert_alpha()
            self.sprites = [e3, e4]
            self.enemy_x = 1174
            print("1")
        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect(center=(self.enemy_x, random.randint(25, 500)))

    def movement(self):
        if self.direction == 0:
            self.rect.centerx += 5
        elif self.direction == 1:
            self.rect.centerx -= 5

    def animation(self):
        pass
        self.index += 0.1
        if self.index >= len(self.sprites):
            self.index = 0
        self.image = self.sprites[int(self.index)]

    def despawn(self):
        if self.direction == 0 and self.rect.left > 1024:
            self.kill()
        elif self.direction == 1 and self.rect.right < 0:
            self.kill()

    def update(self):
        self.movement()
        self.animation()
        self.despawn()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        p1 = pygame.image.load("gameFiles/p1.png").convert_alpha()
        p2 = pygame.image.load("gameFiles/p2.png").convert_alpha()
        p3 = pygame.image.load("gameFiles/p3.png").convert_alpha()
        p4 = pygame.image.load("gameFiles/p4.png").convert_alpha()
        self.sprites = [p1, p2, p3, p4]
        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect(center=(512, 300))
        self.gravity = 0
        self.recoil = 0
        self.last_jump_time = 500

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 626:
            self.rect.bottom = 625
            self.gravity = 0
        if self.rect.top <= 0:
            self.rect.top = 1

    def move(self):
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.last_jump_time >= 300:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < self.rect.centery:
                self.gravity = 5  # Apply downward force
            else:
                self.gravity = -22  # Apply upward force

            if mouse_pos[0] > self.rect.centerx:
                self.recoil = -15  # Apply recoil to the left
            else:
                self.recoil = 15  # Apply recoil to the right
            sound = mixer.Sound("gameFiles/gunshot.wav")
            sound.set_volume(0.1)
            sound.play()
            self.last_jump_time = pygame.time.get_ticks()  # Keeps track of time to stop shot spamming

    def apply_recoil(self):
        if self.rect.bottom == 625:  # If player is on floor, stops them from moving
            self.recoil = 0

        if self.recoil > 0:  # Slows down recoil and movement
            self.recoil += -0.2
        elif self.recoil < 0:
            self.recoil += 0.2

        self.rect.centerx += self.recoil  # Applies recoil to player

    def walk(self):
        if self.rect.bottom >= 625:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                print("pressed")
                self.rect.centerx += -5
            elif keys[pygame.K_d]:
                self.rect.centerx += 5
            elif keys[pygame.K_SPACE]:
                self.gravity += -15

    def look_around(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > self.rect.centerx:
            if mouse_pos[1] < self.rect.centery:
                self.index = 0
            else:
                self.index = 1
        elif mouse_pos[0] < self.rect.centerx:
            if mouse_pos[1] < self.rect.centery:
                self.index = 3
            else:
                self.index = 2
        self.image = self.sprites[self.index]

    def wall_wrap(self):  # Allows the player to wrap around the corners
        if self.rect.right < 10:  # If the player reaches the left side, they'll be wrapped to the right
            self.rect.left = 1014
            print('gone left')
        if self.rect.left > 1014:  # If the player reaches the right side, they'll be wrapped to the left
            self.rect.right = 10
            print('gone right')

    def update(self):  # Class all the methods of the player class
        self.move()
        self.walk()
        self.apply_gravity()
        self.apply_recoil()
        self.wall_wrap()
        self.look_around()


def sprite_collision():
    if pygame.sprite.spritecollide(player.sprite, enemies, False):
        enemies.empty()
        player.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_icon(pygame.image.load("gameFiles/p1.png"))
pygame.display.set_caption("gone huntin'")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

playerPos = (0, 0)

enemyY = 300
score = 0

background = pygame.image.load("gameFiles/backdrop.png").convert()
floor = pygame.image.load("gameFiles/floor.png").convert_alpha()
title = pygame.image.load("gameFiles/bitmap.png").convert_alpha()
text = font.render("Score: " + str(score), True, "white")
textRect = text.get_rect(center=(512, 25))

player = pygame.sprite.GroupSingle()

enemies = pygame.sprite.Group()

alive = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if alive:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not alive:
                alive = True

    if alive:
        if len(enemies) == 0:
            enemies.add(Enemy())

        if len(player) == 0:
            player.add(Player())

        screen.blit(background, (0, 0))
        screen.blit(floor, (0, 0))
        player.draw(screen)
        player.update()
        enemies.draw(screen)
        enemies.update()

        alive = sprite_collision()
    elif not alive:
        screen.blit(background, (0, 0))
        screen.blit(floor, (0, 0))
        screen.blit(title, (300, 300))
    pygame.display.update()
    clock.tick(60)
