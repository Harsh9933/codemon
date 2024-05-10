import os.path

import pygame

from settings import *
from os.path import join


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']
        self.direction = vector()
        self.facing_direction = 'down'
        self.speed = 250
        self.frame_index, self.frames = 0, frames
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(midbottom=pos)
        self.hitbox = self.rect.inflate(-self.rect.width /2, -60)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            self.next = ''
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'
        else:
            self.next = '_idle'

        return f'{self.facing_direction}{self.next}'


class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def input(self):

        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += (self.direction * self.speed * dt)
        self.hitbox.center = self.rect.center

    def collision(self, axis):
        pass

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


class Character(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)


