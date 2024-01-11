# ToDo1: Import and initialise Pygame and from sys import exit
import pygame
from sys import exit
from random import randint, choice,shuffle
from Player import Player
from Obstacle import Obstacle


def display_score():
    # ToDo18: Increase the score for every iteration
    current_time = int(pygame.time.get_ticks()/100)-start_time
    score_surf = pixel_font.render(f'Score: {current_time}', False, 'black')
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#ToDo27: Using the random module, create 2 different numbers between 1 and 12
def new_question():
    num1 = randint(1,12)
    num2 = randint(1,12)
    correct_answer = num1 * num2
    incorrect_options = [choice(answers) for i in range(3)]
    while correct_answer in incorrect_options:
        incorrect_options = [choice(answers) for i in range(3)]
    options = {(1005,385):correct_answer,(1005,535):incorrect_options[0],(1080,460):incorrect_options[1],(930,460):incorrect_options[2]}
    temp = list(options.values())
    shuffle(temp)

    # reassigning to keys
    options = dict(zip(options, temp))
    return f"{num1} x {num2}", options,correct_answer

#ToDo30: Check if the correct answer was pressed
def check_answer(option,correct_answer):
    center = (option.centerx+5,option.centery+5)
    if center == correct_answer:
        return True
    else:
        return False

#ToDo32: Check if player has collided with obstacle
def collision_sprite():
    for i in obstacle_group:
        if i.mask.overlap(player.sprite.mask, (player.sprite.rect.x - i.rect.x, player.sprite.rect.y - i.rect.y)):
            obstacle_group.empty()
            lose.play()
            return False
        else: pass
        # ToDo33: If no, go through loop again, if yes then change gamestate = ‘End’

    return True

class Questions:
    def __init__(self, position):
        self.ogsurface = pygame.image.load('graphics/Diamond.png').convert_alpha()
        self.ogsurface = pygame.transform.rotozoom(self.ogsurface, 0, 0.7)
        self.surface = self.ogsurface.copy()
        self.rect = self.surface.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.surface)

class Buttons:
    def __init__(self, position,image):
        self.surface = pygame.image.load(image).convert_alpha()
        self.surface = pygame.transform.rotozoom(self.surface, 0, 0.3)
        self.rect = self.surface.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.surface)

# ToDo2: Create the Pygame screen display with width and height. Set a caption
pygame.init()
screen = pygame.display.set_mode((1200, 610))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

#ToDo9: Set score = ‘0’
score = 0
bg_music = pygame.mixer.Sound('graphics/music.mp3')
bg_music.set_volume(0.4)
bg_music.play(loops=-1)

wrong_answer = pygame.mixer.Sound('graphics/Wrong.mp3')
lose = pygame.mixer.Sound('graphics/Die.mp3')
lose.set_volume(0.3)

obstacle_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Player())

pixel_font = pygame.font.Font('graphics/pixeltype.ttf',50)
# ToDo8: Set gamestate = False
game_active = False
start_time = 0

#ToDo11: Load images for player character and background
bg_surf = pygame.image.load('graphics/background1.png').convert()
bg_surf = pygame.transform.rotozoom(bg_surf,0,1.8)
bg_rect = bg_surf.get_rect(topleft=(0, 0))

player_stand = pygame.image.load('graphics/Player1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,0.8)
player_stand_rect = player_stand.get_rect(center=(600, 330))

easy_button = pygame.image.load('graphics/Easy Button.png')
easy_button = pygame.transform.rotozoom(easy_button,0,0.3)
easy_button_rect = easy_button.get_rect(center=(250,550))

medium_button = pygame.image.load('graphics/Medium Button.png')
medium_button = pygame.transform.rotozoom(medium_button,0,0.3)
medium_button_rect = easy_button.get_rect(center=(600,550))

hard_button = pygame.image.load('graphics/Hard Button.png')
hard_button = pygame.transform.rotozoom(hard_button,0,0.3)
hard_button_rect = easy_button.get_rect(center=(950,550))

difficulty_group = [Buttons((250,550),'graphics/Easy Button.png'),
                    Buttons((600,550),'graphics/Medium Button.png'),
                    Buttons((950,550),'graphics/Hard Button.png')]

game_name = pixel_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(600, 60))
#ToDo7: Explain how the game works, scoring power ups etc. Have visuals to show controls of the game
welcome_message = pixel_font.render('Hello Y4! Welcome to this maths game!',False,(111,196,169))
welcome_message_rect = welcome_message.get_rect(center=(600, 90))
welcome_message1 = pixel_font.render('This will test your multiplication skills',False,(111,196,169))
welcome_message1_rect = welcome_message1.get_rect(center=(600, 120))
welcome_message2 = pixel_font.render('Click the correct answer to jump over obstacles',False,(111,196,169))
welcome_message2_rect = welcome_message2.get_rect(center=(600, 150))
welcome_message3 = pixel_font.render('Have Fun!',False,(111,196,169))
welcome_message3_rect = welcome_message3.get_rect(center=(600, 180))


question_group = [Questions((1000,380)),
                  Questions((1000,530)),
                  Questions((1075,455)),
                  Questions((925,455))]



answers = [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,18,20,21,22,24,25,27,28,30,32,33,35,36,40,42,44,45,48,49,50,54,55,56,60,63,64,66,70,72,77,80,81,84,88,90,96,99,100,108,110,120,132,144]

num1 = None
num2 = None
question, options_list,correct_answer = new_question()

spawning_speed = 1500
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,spawning_speed)
#Easy = 2000,Medium = 1500, Hard = 1000

colour_timer = 0
max_timer = 500
clicked_sprites = []
speed = 8
speed_increase = 0

# ToDo3: Create a while True loop
while True:
    # ToDo5 Check if event.type is Pygame quit. If so, quit Pygame and exit the window within the loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ToDo12: Create if statement for whether gamestate = True
        if game_active:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = []
                for i in question_group:
                    if i.rect.collidepoint(pos) and i.mask.get_at((pos[0] - i.rect.x, pos[1] - i.rect.y)):
                        clicked_sprites.append(i)
                if len(clicked_sprites) >= 1:
                    if check_answer(clicked_sprites[0].rect,(list(options_list.keys())[list(options_list.values()).index(correct_answer)])):
                        # ToDo31: If correct answer pressed, change gravity variable to -20
                        player.update(True)
                        clicked_sprites[0].surface = pygame.image.load('graphics/GreenDiamond.png').convert_alpha()
                        clicked_sprites[0].surface = pygame.transform.rotozoom(clicked_sprites[0].surface, 0, 0.7)
                    else:
                        clicked_sprites[0].surface = pygame.image.load('graphics/RedDiamond.png').convert_alpha()
                        clicked_sprites[0].surface = pygame.transform.rotozoom(clicked_sprites[0].surface, 0, 0.7)
                        wrong_answer.play()
                    colour_timer = pygame.time.get_ticks()
                    question, options_list,correct_answer = new_question()

        else:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites1 = []
                for i in difficulty_group:
                    if i.rect.collidepoint(pos) and i.mask.get_at((pos[0] - i.rect.x, pos[1] - i.rect.y)):
                        clicked_sprites1.append(i)
                if len(clicked_sprites1) >= 1:
                    if clicked_sprites1[0].rect.center == (250,550):
                        spawning_speed = 3000
                        game_active = True
                    if clicked_sprites1[0].rect.center == (600,550):
                        spawning_speed = 1500
                        game_active = True
                    if clicked_sprites1[0].rect.center == (950,550):
                        spawning_speed = 1100
                        game_active = True
                    pygame.time.set_timer(obstacle_timer, spawning_speed)
                    start_time = int(pygame.time.get_ticks()/100)

        if game_active:
            # ToDo24: Every few seconds spawn an obstacle
            if event.type == obstacle_timer:
                new_obstacle = Obstacle(choice(['fireball','spike1','spike2','spike3']))
                obstacle_group.add(new_obstacle)

    if game_active:
        # ToDo13: Display all the surfaces using screen.blit()
        screen.blit(bg_surf, bg_rect)
        keys = pygame.key.get_pressed()
        # ToDo28: Print the multiplication question using these 2 numbers
        question_surf = pixel_font.render(question, False, (0, 0, 0))
        questions_rect = question_surf.get_rect(center=(600, 100))
        screen.blit(question_surf, questions_rect)
        # ToDo29: Create 4 different answers underneath with one being the accurate answer
        ans1 = pixel_font.render(str(options_list[(1005,385)]), False, (0, 0, 0))
        ans1_rect = question_surf.get_rect(center=(1015,385))
        ans2 = pixel_font.render(str(options_list[(1005, 535)]), False, (0, 0, 0))
        ans2_rect = question_surf.get_rect(center=(1015, 535))
        ans3 = pixel_font.render(str(options_list[(1080, 460)]), False, (0, 0, 0))
        ans3_rect = question_surf.get_rect(center=(1090,460))
        ans4 = pixel_font.render(str(options_list[(930, 460)]), False, (0, 0, 0))
        ans4_rect = question_surf.get_rect(center=(940,460))

        if len(clicked_sprites) > 0:
            if colour_timer > 0 and pygame.time.get_ticks() - colour_timer > max_timer:
                clicked_sprites[0].surface = clicked_sprites[0].ogsurface

        score = display_score()

        player.draw(screen)
        player.update(False)

        obstacle_group.draw(screen)
        obstacle_group.update()
        # ToDo17: Move the background towards the left by changing the x position
        bg_rect.x -= speed
        if bg_rect.centerx < 0:
            bg_rect.topleft = (0, 0)



        # Collision
        game_active = collision_sprite()

        for i in question_group:
            screen.blit(i.surface,i.rect)
        screen.blit(ans1, ans1_rect)
        screen.blit(ans2, ans2_rect)
        screen.blit(ans3, ans3_rect)
        screen.blit(ans4, ans4_rect)

    else:
        screen.fill((10, 60, 200))
        # ToDo34: Print the score on the screen
        score_message = pixel_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(600,490))
        screen.blit(game_name, game_name_rect)

        screen.blit(easy_button, easy_button_rect)
        screen.blit(medium_button, medium_button_rect)
        screen.blit(hard_button, hard_button_rect)

        if score == 0:
            screen.blit(welcome_message, welcome_message_rect)
            screen.blit(welcome_message1, welcome_message1_rect)
            screen.blit(welcome_message2, welcome_message2_rect)
            screen.blit(welcome_message3, welcome_message3_rect)

        else:
            screen.blit(score_message,score_message_rect)
            player_stand_rect.centery = 300
        screen.blit(player_stand, player_stand_rect)

    # ToDo4: Create the clock variable and set it to 60 within the loop.
    pygame.display.update()
    clock.tick(60)