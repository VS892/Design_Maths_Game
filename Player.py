import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player1.png').convert_alpha()
        player_walk1 = pygame.transform.rotozoom(player_walk1,0,0.3)
        player_walk2 = pygame.image.load('graphics/Player2.png').convert_alpha()
        player_walk2 = pygame.transform.rotozoom(player_walk2, 0, 0.3)
        player_walk3 = pygame.image.load('graphics/Player3.png').convert_alpha()
        player_walk3 = pygame.transform.rotozoom(player_walk3, 0, 0.3)
        self.player_walk = [player_walk1, player_walk2, player_walk3]
        self.player_index = 0
        self.player_jump = player_walk1

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,525))
        self.gravity = 0
        self.mask = pygame.mask.from_surface(self.image)

        self.jump_sound = pygame.mixer.Sound('graphics/jump1.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self,jump):
        if jump == True:
            # ToDo10: Set gravity = ‘0’
            if self.rect.bottom >= 525:
                self.gravity = -20
                self.jump_sound.play()

    def apply_gravity(self):
        # ToDo14: Set Player_rect.y += gravity
        self.rect.y += self.gravity
        # ToDo15: Increase gravity by 1 every iteration
        self.gravity += 1
        # ToDo16: Check if player_rect is below ground, if so set above ground again.
        if self.rect.bottom >= 525:
            self.rect.bottom = 525

    def animation(self):
        if self.rect.bottom >= 1000:
            self.image = self.player_jump
        else:
            self.player_index += 0.15
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self,jump):
        self.player_input(jump)
        self.apply_gravity()
        self.animation()