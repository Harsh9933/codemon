import os.path

import pygame

from settings import *
from os.path import join


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.direction = vector()
        self.facing_direction = 'down'
        self.speed = 250
        self.frame_index, self.frames = 0, frames
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center=pos)

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
        if keys[pygame.K_w]:
            input_vector.y -= 1
        if keys[pygame.K_s]:
            input_vector.y += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_d]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += (self.direction * self.speed * dt)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


class Character(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)


