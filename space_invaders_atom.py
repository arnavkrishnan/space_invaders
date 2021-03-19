import pygame
import random
pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill((0, 0, 0))

hero = pygame.image.load('images/player.png')
hero_size = 80
hero = pygame.transform.scale(hero, (hero_size, hero_size))
hero_x = screen_width/2 - hero_size/2
hero_y = screen_height - hero_size

screen.blit(hero, (hero_x, hero_y))

alien = pygame.image.load('images/space_alien.png')
alien_size = 40
alien = pygame.transform.scale(alien, (alien_size, alien_size))
alien_x = 50
alien_y = 50

screen.blit(alien, (alien_x, alien_y))

explode_vfx = 17*[0]
for i in range(17):
    explode_vfx[i] = pygame.image.load('Effects 2/Red Explosion/1_'+str(i)+'.png')
def explode(cx, cy):
    for i in range(17):
        explode_rect = explode_vfx[i].get_rect()
        explode_rect.center = (cx, cy)
        screen.blit(explode_vfx[i], explode_rect)
        pygame.display.update()
        pygame.time.delay(20)


def collide_cirle(cx1, cy1, r1, cx2, cy2, r2):
    if ((cx2 - cx1)*(cx2 - cx1)+(cy2 - cy1)*(cy2 - cy1)) < (r1+r2) * (r1+r2):
        return True
    else:
        return False

def collide_rect(x1, y1, w1, h1, x2, y2, w2, h2):
    if ((x2 > x1 and x2 - x1 < w1) or (x1 > x2 and x1 - x2 < w2)) and ((y2 > y1 and y2 - y1 < h1) or (y1 > y2 and y1 - y2 < h2)):
        return True
    else:
        return False

def collide_rect_circle(cx, cy, r, x1, x2, y1, y2):
    x = max(x1, min(cx, x2))
    y = max(y1, min(cy, y2))
    if ((cx - x) * (cx - x) + (cy - y) * (cy - y) < (r * r)):
        return True
    else:
        return False

def fire(x, y):
    bullet = pygame.Rect(x + hero_size/2-3, y, 6, 10)
    return bullet

bullet_list = []
alien_list = []
alien_counter = 0
Running = True
bullet = False
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            print(Running)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_list.append(fire(hero_x, hero_y))
    if alien_counter == 0:
        alien = pygame.image.load('images/space_alien.png')
        alien_size = 40
        alien = pygame.transform.scale(alien, (alien_size, alien_size))
        alien_x = random.randint(0, 800)
        alien_y = 50
        alien_list.append([alien, alien_x, alien_y])
    alien_counter = (alien_counter + 1)%60

    screen.fill((0, 0, 0))
    screen.blit(alien_list[0][0], (alien_x, alien_y))
    alien_y += 2
    alien_x += 0
    for alien in alien_list:
        alien[2] += 1
        alien_x = alien[1]; alien_y = alien[2]
        screen.blit(alien[0], (alien_x, alien_y))
        if collide_rect(alien_x, alien_y, alien_size, alien_size, hero_x, hero_y, hero_size, hero_size):
            explode(alien_x, alien_y)
            hero_x = 900
            hero_y = 40
        for bullet in bullet_list:
            bullet.move_ip(0,-4)
            pygame.draw.rect(screen, 'yellow', bullet)
            if collide_rect(alien_x, alien_y, alien_size, alien_size, bullet.left, bullet.top, bullet.width, bullet.height):
                explode(int(alien_x+alien_size/2), int(alien_y+alien_size/2))
                alien_list.remove(alien)
                bullet_list.remove(bullet)
                running = False
                screen.fill((0, 0, 0))
    keypressed = pygame.key.get_pressed()
    if  keypressed[pygame.K_LEFT]:
        hero_x -= 2
        if hero_x < 0:
            hero_x += 2
    if  keypressed[pygame.K_RIGHT]:
        hero_x += 2
        if hero_x > 900:
            hero_x -= 2
    if  keypressed[pygame.K_UP]:
        hero_y -= 2
        if hero_y < 0:
            hero_y += 2
    if  keypressed[pygame.K_DOWN]:
        hero_y += 2
        if hero_y > 700:
            hero_y -= 2
    screen.blit(hero, (hero_x, hero_y))
    pygame.display.update()
    ticks_passed =  pygame.time.Clock().tick(60)
