import pygame
import random
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, group, platforms) -> None:
        super().__init__(group)
        self.all_sprites = group
        self.platforms = platforms
        self.surf = pygame.image.load("./assets/platform.png")
        self.initial_pos = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30))
        self.rect = self.surf.get_rect(center = self.initial_pos)
        self.point = True
    
    def __str__(self) -> str:
        return "Platform: Pos= " + str(self.initial_pos[0]) + " " + str(self.initial_pos[1])
        
    def valid_platform(self) -> bool:
        if pygame.sprite.spritecollideany(self, self.platforms):
            print("Colliding Platform")
            return False

        for platform in self.platforms:
            print(platform)
            if self == platform:
                continue
            # Determines how far platforms can spawn away from each other
            # TODO Works well on 100 for both, but crashes often (BECAUSE IT GENERATES )
            if (abs(self.rect.x - platform.rect.bottom) < 100 and        # Spawn boundry Y
                abs(self.rect.bottom - platform.rect.top) < 100):          # Spawn boundry X
                return True
        return True
        
    def update(self) -> None:
        pass

class MovingPlatform(Platform):
    def __init__(self, group, platforms) -> None:
        self.speed = random.choice([-5,-2,2,5])
        # Determines how far moving platforms move on x axis
        # TODO Some platforms jitter, needs to be fixed
        self.move_bounds = random.randint(50,200)
        super().__init__(group, platforms)

    def move(self) -> None:
        if (self.rect.center[0] < self.initial_pos[0] - self.move_bounds or
            self.rect.center[0] > self.initial_pos[0] + self.move_bounds):
            self.speed = -self.speed
        self.rect.move_ip(self.speed, 0)
    def update(self) -> None:
        self.move()