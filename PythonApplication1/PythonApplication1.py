
import random
from secrets import randbelow
from timeit import Timer
from typing import Any
import pygame
import sys
import pygame.mixer
import pygame.freetype

def restart_game():
    global game_status, bird_speed, bird_rect
    game_status = 'start'
    bird_speed = 0
    bird_rect.center = (300, 300)
    wall_group.empty()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Flappy Bird')
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (1000, 600))
start_button = pygame.Rect(300, 400, 200, 50)
restart_button = pygame.Rect(300, 400, 200, 50)
bird_image = pygame.image.load('assets/0.png')
wall_image = pygame.image.load('assets/Truba.png')
bird_image = pygame.transform.scale(bird_image, (80, 60))
wall_image = pygame.transform.scale(wall_image, (100, 500))
bird_rect = bird_image.get_rect()
bird_rect.center = (300, 300)
font = pygame.freetype.Font(None, 30)

bird_speed = 0
gravity = 0.2
jump = 1

game_status = 'start'
score = 0

wall_group = pygame.sprite.Group()
spawn_wall_event = pygame.USEREVENT
pygame.time.set_timer(spawn_wall_event, 1500)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.scored = False
    
    def update(self):
        global game_status
        self.rect.x -= 5
        if self.rect.colliderect(bird_rect):
            game_status = 'menu'
    
    def passed(self):
        global score
        if self.rect.right < bird_rect.left and not self.scored:
            self.scored = True
            score += 1

def restart_game():
    global game_status, bird_speed, bird_rect, score
    game_status = 'start'
    bird_speed = 0
    bird_rect.center = (300, 300)
    score = 0
    wall_group.empty()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == spawn_wall_event:
            wall = Wall((1050, random.choice([-25, -65, -150])), wall_image)
            wall_group.add(wall)
            wall = Wall((1050, random.choice([650, 700, 750])), wall_image)
            wall_group.add(wall)
    
    screen.fill((100, 100, 100))
    
    if game_status == 'game':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird_speed -= jump
        bird_speed += gravity 
        bird_rect.centery += int(bird_speed)
        screen.blit(bird_image, bird_rect)
        wall_group.update()
        wall_group.draw(screen)
        for wall in wall_group:
            wall.passed()
    
    if game_status == 'start':
        font.render_to(screen, (300, 300), 'Flappy Bird', (200, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        font.render_to(screen, (310, 410), 'Start', (0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(mouse_pos):
            game_status = 'game'       
    
    if game_status == 'menu':    
        font.render_to(screen, (300, 300), 'Game over', (200, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        font.render_to(screen, (310, 410), 'Restart', (0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(mouse_pos):
            restart_game()
    
    font.render_to(screen, (10, 10), f'Score: {score}', (255, 255, 255))
    
    pygame.display.flip()
    clock.tick(60)
