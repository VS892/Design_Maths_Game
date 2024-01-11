import pygame
import random

#ToDo23: Create an obstacle class with a constructor function consisting of properties
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fireball':
            fireball_frame1 = pygame.image.load('graphics/Fireball1.png').convert_alpha()
            fireball_frame1 = pygame.transform.rotozoom(fireball_frame1, 0, 0.4)
            fireball_frame2 = pygame.image.load('graphics/Fireball2.png').convert_alpha()
            fireball_frame2 = pygame.transform.rotozoom(fireball_frame2, 0, 0.4)
            fireball_frame3 = pygame.image.load('graphics/Fireball3.png').convert_alpha()
            fireball_frame3 = pygame.transform.rotozoom(fireball_frame3, 0, 0.4)
            fireball_frame4 = pygame.image.load('graphics/Fireball4.png').convert_alpha()
            fireball_frame4 = pygame.transform.rotozoom(fireball_frame4, 0, 0.4)
            self.frames = [fireball_frame1, fireball_frame2, fireball_frame3, fireball_frame4]
            y_pos = 410
        elif type == 'spike1':
            spike1 = pygame.image.load('graphics/Spike1.png').convert_alpha()
            spike1 = pygame.transform.rotozoom(spike1, 0, 0.3)
            self.frames = [spike1]
            y_pos = 540
        elif type == 'spike2':
            spike2 = pygame.image.load('graphics/Spike2.png').convert_alpha()
            spike2 = pygame.transform.rotozoom(spike2, 0, 0.3)
            self.frames = [spike2]
            y_pos = 540
        else:
            spike3 = pygame.image.load('graphics/Spike3.png').convert_alpha()
            spike3 = pygame.transform.rotozoom(spike3, 0, 0.3)
            self.frames = [spike3]
            y_pos = 540

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(1200, 1500),y_pos))
        self.speed = 8
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # ToDo26: Once obstacle is past screen delete it
    def destroy(self):
        if self.rect.x <= -200:
            self.kill()

    def update(self):
        # ToDo25: Move the obstacle towards the left at the same speed as the background
        if len(self.frames) == 1:
            self.rect.x -= self.speed
        else:
            self.rect.x -= self.speed+2
        self.animation()
        self.destroy()
