#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Fighter')
SPACE = pygame.transform.scale(pygame.image.load('assets/space.png'), (WIDTH, HEIGHT))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets/spaceship_yellow.png'), (55, 40)), 90)
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets/spaceship_red.png'), (55, 40)), 270)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
BULLET_HIT = pygame.mixer.Sound('assets/Gun+Silencer.ogg')
BULLET_FIRE = pygame.mixer.Sound('assets/Grenade+1.ogg')
BACKGROUND_MUSIC = pygame.mixer.Sound('assets/StarWars.ogg')
SHIP_WIDTH = 40
SHIP_HEIGHT = 55
SHIP_VEL = 4
BULLET_VEL = 10
BULLET_HEIGHT = 5
BULLET_WIDTH = 10
PARTITION_WIDTH = 10
PARTITION = pygame.Rect(WIDTH//2-PARTITION_WIDTH//2, 0, 10, HEIGHT)
MAX_BULLETS = 4
WHITE = (255, 255, 255)
YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2

def main():
    clock = pygame.time.Clock()
    yellow = pygame.Rect(300, 250, SHIP_WIDTH, SHIP_HEIGHT)
    red = pygame.Rect(700, 250, SHIP_WIDTH, SHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    BACKGROUND_MUSIC.play(loops=-1)
    pygame.event.clear()
    run = True
    while run:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-2, BULLET_WIDTH, BULLET_HEIGHT)
                    BULLET_FIRE.play()
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x-BULLET_WIDTH, red.y+yellow.height//2-2, BULLET_WIDTH, BULLET_HEIGHT) # using // to round up the division since we want an integer
                    BULLET_FIRE.play()
                    red_bullets.append(bullet)
                
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT.play()
        
        winner_text = ''
        if red_health <= 0:
            winner_text = 'Game Over, Yellow Wins!'
        if yellow_health <= 0:
            winner_text = 'Game Over, Red Wins!'
        if winner_text != '':
            BACKGROUND_MUSIC.stop()
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed() # checks for all the keys pressed not just the last one, this allows two keys to work and move the ship diagonally
        if keys_pressed[pygame.K_a] and yellow.x > 0:
            yellow.x -= SHIP_VEL
        if keys_pressed[pygame.K_d] and yellow.x + SHIP_WIDTH < WIDTH/2 - PARTITION_WIDTH/2:
            yellow.x += SHIP_VEL
        if keys_pressed[pygame.K_w] and yellow.y > 0:
            yellow.y -= SHIP_VEL
        if keys_pressed[pygame.K_s] and yellow.y + SHIP_HEIGHT < HEIGHT:
            yellow.y += SHIP_VEL
            
        if keys_pressed[pygame.K_LEFT] and red.x > WIDTH/2 + PARTITION_WIDTH/2:
            red.x -= SHIP_VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + SHIP_HEIGHT < WIDTH:
            red.x += SHIP_VEL
        if keys_pressed[pygame.K_UP] and red.y > 0:
            red.y -= SHIP_VEL
        if keys_pressed[pygame.K_DOWN] and red.y + SHIP_HEIGHT < HEIGHT:
            red.y += SHIP_VEL

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

def draw(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, 'blue', PARTITION)
    yellow_health_text=HEALTH_FONT.render(f'Health:{yellow_health}',1,'white')
    red_health_text=HEALTH_FONT.render(f'Health:{red_health}',1,'white')
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10,10))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, 'yellow', bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, 'red', bullet)
    WIN.blit(YELLOW_SHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SHIP,(red.x,red.y))
    pygame.display.update()

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x +=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    winner_text = HEALTH_FONT.render(text,1,'white')
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)

if __name__=="__main__":
    main()

# In[ ]:





# In[ ]:




