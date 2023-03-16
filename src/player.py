import pygame
from settings import *
from support import *
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, group, platforms) -> None:
        super().__init__(group)
        self.import_assets()
        self.status = 'idle_left'
        self.frame_index = 1

        self.platforms = platforms
        self.surf = self.animations[self.status][self.frame_index]
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT-30))

        # Keeping track of the players position, velocity and acceleration vectors
        self.pos = vec((WIDTH/2, HEIGHT-30))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        
        self.jumping = False
        self.jumpSound = pygame.mixer.Sound("./audio/jumpSound.wav")
        self.score = 0

    def move(self) -> None:
        # Reseting acceleration to 0.5 (because gravity, and positive because 0,0 is top left, so increasing Y actually brings us down)

        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            if not self.jumping:
                self.status = 'walk_left'
            else:
                self.status = 'jump_left'

        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            if not self.jumping:
                self.status = 'walk_right'
            else:
                self.status = 'jump_right'
        
        # Taking into account velocity and friction when accelerating
        self.acc.x += self.vel.x * FRIC
        # Adding acc onto velocity
        self.vel += self.acc
        # Changing position (equation of motion)
        self.pos += self.vel + 0.5 * self.acc

        # If you go further than width of the screen, you end up on the other side (like snake)
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # updating your position, so you actually see movement
        self.rect.midbottom = self.pos

    def input(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.cancel_jump()
            
    def camera_handler(self) -> None:
        if self.rect.top <= HEIGHT / 3:
            self.pos.y += abs(self.vel.y)
            # TODO Make a scrolling background
            for plat in self.platforms:
                plat.rect.y += abs(self.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

    def collision_handler(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    

    def jump(self) -> None:
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits and not self.jumping:
            pygame.mixer.Sound.play(self.jumpSound)
            self.jumping = True
            self.vel.y = -15
        
    def cancel_jump(self) -> None:
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def animate(self, dt) -> None:
        self.frame_index += 4 * dt
        #print("For " + self.status + " there are " + str(len(self.animations[self.status])) + " images")
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.surf = self.animations[self.status][int(self.frame_index)]
    
    def get_status(self) -> None:
        if self.jumping:
            self.status = 'jump_' + self.status.split('_')[1]

        if abs(self.vel.x) < 0.5 and not self.jumping:
            self.status = 'idle_' + self.status.split('_')[1] 
        
        # print(self.status)
    
    def import_assets(self) -> None:
        self.animations = {'idle_left': [], 'idle_right': [], 'jump_left': [], 'jump_right': [], 'walk_left': [], 'walk_right': []}
        for animation in self.animations.keys():
            full_path = './assets/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def update(self, dt) -> None:
        # TODO input in main.py to access events, shoud move it here
        # self.input()
        # TODO camera_handler in level.run, should move it here
        # self.camera_handler()
        self.get_status()
        self.collision_handler()

        self.animate(dt)
        self.move()
        

            