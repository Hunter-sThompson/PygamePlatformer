import pygame
import random, math
import time, sys
from settings import *
from platform_1 import Platform
from platform_1 import MovingPlatform
from player import Player

class Level:
    def __init__(self) -> None:
        # DisplaySurface
        self.displaySurf = pygame.display.get_surface()

        self.bg = Background() 
        self.scoreFont = pygame.font.SysFont("Ariel", 18)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.P1 = Player(self.all_sprites, self.platforms)
        self.setup()


    # Setting Up Platforms
    def setup(self) -> None:

        testPlat = MovingPlatform(self.all_sprites, self.platforms)
        testPlat.surf = pygame.Surface((WIDTH/6, 20))
        testPlat.surf.fill((0,0,255))
        testPlat.rect = testPlat.surf.get_rect(center = (WIDTH/2, HEIGHT-80-320))
        PT1 = Platform(self.all_sprites, self.platforms)
        PT1.surf = pygame.Surface((WIDTH, 20))
        PT1.surf.fill((255,0,0))
        PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))
        PT1.point = False

        self.all_sprites.add(PT1)
        self.all_sprites.add(self.P1)
        self.platforms.add(PT1)
        self.platforms.add(testPlat)
        for _ in range(8):
            self.generate_platform()
            

    # TODO Make it so each platform generates at a max y bounry of the jump height 
    def generate_platform(self):
        while len(self.platforms) < 9:

            V = False
            while not V:
                
                if random.random() <= MOVE_CHANCE:
                    p = MovingPlatform(self.all_sprites, self.platforms)
                else:
                    p = Platform(self.all_sprites, self.platforms)
                #p.rect.center = (random.randrange(0, WIDTH - width),
                #                random.randrange(-50, 0))

                V = p.valid_platform()
                if not V:
                    p.kill() 
                    continue
            
            self.platforms.add(p)
            self.all_sprites.add(p)

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
        self.bgImage = pygame.image.load('./assets/background_wooden.png') 
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

        
        
