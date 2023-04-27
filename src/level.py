import pygame
import random, math
import time, sys
from settings import *
from platform_1 import Platform, MovingPlatform
from player import Player
from enemy import Crabby, Sharky

class Level:
    def __init__(self) -> None:
        # DisplaySurface
        self.displaySurf = pygame.display.get_surface()

        self.bg = Background() 
        self.scoreFont = pygame.font.SysFont("Ariel", 18)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Counter
        self.generated_platforms = 0

        self.setup()



    # Setting Up Platforms
    def setup(self) -> None:

        PT1 = Platform(self.all_sprites, self.platforms)
        PT1.surf = pygame.transform.scale(PT1.surf, (WIDTH, 20))
        PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))
        PT1.point = False

        # might not need to add, since __init__super is called
        # I didnt add testenemy to a group, but it still works
        # need testing (and learning dammit)
        self.platforms.add(PT1)

        testEnemy = Crabby(self.all_sprites)
        testEnemy.rect.center = (WIDTH/2, HEIGHT/2)

        testSharky = Sharky(self.all_sprites)
        testSharky.rect.center = (WIDTH/2, HEIGHT/2-100)

        self.generate_crab()

        self.all_sprites.add(PT1)
        
        self.P1 = Player(self.all_sprites, self.platforms, self.enemies)
        self.all_sprites.add(self.P1)
        for _ in range(8):
            self.generate_platform(True)
            

    # a function that generates enemies
    def generate_crab(self):

        e = Crabby(self.all_sprites)

        if self.generated_platforms % 9 == 0:
            latest_platform = self.platforms.sprites()[-1]
            spawn_point = latest_platform.initial_pos
            e.rect = e.surf.get_rect(center = (spawn_point[0], (spawn_point[1]-20)))
        self.all_sprites.add(e)
        self.enemies.add(e)
    # TODO Make it so each platform generates at a max y bounry of the jump height 
    def generate_platform(self, setup: bool = False):
        while len(self.platforms) < 7:

            if random.random() <= MOVE_CHANCE:
                p = MovingPlatform(self.all_sprites, self.platforms)
            else:
                p = Platform(self.all_sprites, self.platforms)
            
            attempts = 0
            V = False
            while not V and attempts <  100:

                if setup:
                    print("Setup")
                    p.initial_pos = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-10))
                else:
                    p.initial_pos = (random.randint(0, WIDTH-10), random.randint(-100, HEIGHT-10))

                V = p.valid_platform()
                attempts += 1

            if not V:
                print("Failed to generate platform after ", attempts, " attempts")
                continue
            
            self.generated_platforms += 1
            self.platforms.add(p)
            self.all_sprites.add(p)
            print("Platform Generated at location: ", p.rect.center)

    def check_game_over(self) -> None:
        if self.P1.rect.top > HEIGHT:
            for entity in self.all_sprites:
                entity.kill()
                time.sleep(1)
                self.displaySurf.fill((255,2,2))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()

    
    def run(self, dt) -> None:
        self.check_game_over()

        # Filling up the background of the screen 
        self.displaySurf.fill((100,12,5))
        # Generate platforms
        self.generate_platform()
        # Displaying background
        # Displaying all the sprites
        self.P1.camera_handler()
        self.bg.bg_handler(self.P1, self.displaySurf)
        for entity in self.all_sprites:
            self.displaySurf.blit(entity.surf, entity.rect)
            entity.update(dt)
        
        
        score_display = self.scoreFont.render(str(self.P1.score), False, (0,255,0))
        self.displaySurf.blit(score_display, (WIDTH/2, 50)) 

        # TODO Remove
        # pygame.display.update()
        #dt.tick(FPS)

class Background():
    def __init__(self) -> None:
        self.bgImage = pygame.image.load('./assets/background_sea.png') 
        self.rect = self.bgImage.get_rect()
        self.scroll = 0
    
    def get_rect(self):
        return self.rect

    def bg_handler(self, player, display) -> None:
        tiles = math.ceil(HEIGHT / self.bgImage.get_height())
        if player.rect.top <= HEIGHT / 3:
            self.scroll += abs(player.vel.y)

        i = -2 
        while i < tiles:
            y = self.bgImage.get_height()*i + self.scroll
            if y > HEIGHT + self.bgImage.get_height():
                self.scroll -= self.bgImage.get_height()
                print("Out of bounds")
            blitPos = (0, y)
            display.blit(self.bgImage, blitPos)
            i += 1

        
        
