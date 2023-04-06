import pygame
import random
from settings import *
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.all_sprites = group

        self.initial_pos = (WIDTH/2, HEIGHT/2)

class Crabby(Enemy):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.import_assets()
        
        self.frame_index = 1
        self.status = 'crabThings'

        self.surf = self.animations[self.status][self.frame_index]
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))

    # TODO optimize this shit. Maybe make animate a parent class method huh?
    def animate(self, dt) -> None:
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.surf = self.animations[self.status][int(self.frame_index)]

    def import_assets(self):
        self.animations = {'crabThings': []}
        for animation in self.animations.keys():
            full_path = './assets/crabby/' + animation
            self.animations[animation] = import_folder(full_path)

    def update(self, dt) -> None:
        self.animate(dt)

class Sharky(Enemy):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.import_assets()

        self.frame_index = 1
        self.status = 'swim_right'

        self.surf = self.animations[self.status][self.frame_index]
        self.rect = self.surf.get_rect(center = self.initial_pos)

        self.speed = 2
        self.move_bounds = 100

    def move(self) -> None:
        if (self.rect.center[0] > self.initial_pos[0] + self.move_bounds):
            self.status = 'swim_left'
            self.speed = -self.speed
        elif (self.rect.center[0] < self.initial_pos[0] - self.move_bounds):
            self.status = 'swim_right'
            self.speed = -self.speed
        self.rect.move_ip(self.speed, 0)

    def animate(self, dt) -> None:
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.surf = self.animations[self.status][int(self.frame_index)]

    def import_assets(self):
        self.animations = {'swim_left': [], 'swim_right': []}
        for animation in self.animations.keys():
            full_path = './assets/shark_enemy/' + animation
            self.animations[animation] = import_folder(full_path)

    def update(self, dt) -> None:
        self.move()
        self.animate(dt)
