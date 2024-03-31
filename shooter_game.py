# import pygame
# from pygame.locals import *

# pygame.init()
# screen_info = pygame.display.Info()
# screen_width, screen_height = screen_info.current_w, screen_info.current_h
# screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h, speed):
        super().__init__()
        self. image = transform.scale(image.load(img), (w,h))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.rect.h = h
        self.rect.w = w
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w-5-self.rect.width:
            self.rect.x += self.speed
    def fire(self):
        y= self.rect.y
        x = self.rect.centerx
        bullet = Bullet('syx.png', x-45, y , 28, 56,5)
        bullets.add(bullet)
    def fire_top(self):
        y= self.rect.y
        x = self.rect.centerx    
        giper_bullet = Bullet('chips.png', x-45, y , 56, 56,5)
        giper_bullets.add(giper_bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_h-self.rect.height:
            self.rect.x = randint(0, win_w - 5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,4)
            lost += 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()

class Giper_Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()


#создай окно игры
# infoOdject = display.Info()
win_h = 768
win_w = 1366
win = display.set_mode((win_w,win_h),FULLSCREEN)
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'),(win_w,win_h))
button = GameSprite('button.png', 580, 350, 200, 100,0)
player = Player('maz.png',win_w /2 - 100/2,win_h - 140,180,140,15,)

enemy_count = 5
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('amnimgot.png', randint(5,win_w-5-100), -50, 100, 85, randint(2, 4))
    enemyes.add(enemy)

bos = Enemy('amnimgot.png', randint(5,win_w-5-100), -50, 300, 255, randint(2, 4))
                              # x  y  w  h speed

# asteroid_count = 3
# asteroids = sprite.Group()
# for i in range(asteroid_count):
#     asteroid = Enemy('asteroid.png', randint(5,win_w-5-100), -50, 100, 85, randint(15, 25)/10)
#     asteroids.add(asteroid)                              

bullets = sprite.Group()
giper_bullets = sprite.Group()

# полдключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

# подключение шрифтов
font.init()
font1 = font.Font(None, 36)


game = True
finish= True
menu = True
lost = 0
score = 0
text = 0
font_lose = font1.render('ТЫ ЛОООХ', 1, (255,255,255))
font_win = font1.render('ЙОУ ТЫ БРО',  1, (255,255,255))
bos_f = 0
bos_l = False

clock = time.Clock()
FPS = 60

while game:
    # поверка нажатия на кнопку выход
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_e:
                player.fire()
            if e.key == K_TAB:
                menu = False
                finish = False
            if e.key == K_q and score == 5:
                player.fire_top()

    if menu == True:
        win.blit(background,(0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
        if text == 1:
             win.blit(font_win, (580, 300))
        elif text == 2:
            win.blit(font_lose, (580, 300))
        lost = 0
        score = 0

        enemyes.empty()
        for i in range(enemy_count):
            enemy = Enemy('amnimgot.png', randint(5,win_w-5-100), -50, 100, 85, randint(2, 4))
            enemyes.add(enemy)
        bullets.empty()
        giper_bullets.empty()

    if finish != True:           
        # рисовка объектов сцены
        win.blit(background,(0,0))
        player.update()
        enemyes.update()
        bullets.update()
        giper_bullets.update()
        # asteroids.update()

        player.reset()
        enemyes.draw(win)
        bullets.draw(win)
        giper_bullets.draw(win)
        # asteroids.draw(win)

        sprite_list1= sprite.spritecollide(player, enemyes,False)
        # sprite_list2= sprite.spritecollide(player, asteroids,False)
        if len(sprite_list1)>0 or lost>3:
            # font_lose = font1.render('ТЫ ЛООХ', 1, (255,255,255))
            # win.blit(font_lost,(250,250))
            text = 2
            finish= True
            menu=True

        sprite_list= sprite.groupcollide(enemyes, bullets, True, True)
        sprite_list1 = sprite.groupcollide(enemyes, giper_bullets, True, True)
        for m in sprite_list:
            score += 1
            enemy = Enemy('amnimgot.png', randint(5,win_w-5-100), -50, 100, 85, randint(1, 4))
            enemyes.add(enemy)
        for m in sprite_list1:
            score += 1
            enemy = Enemy('amnimgot.png', randint(5,win_w-5-100), -50, 100, 85, randint(1, 4))
            enemyes.add(enemy)
        if score >9:
            text = 1
            finish = True
            menu = True
        if score== 5 and bos_l!= True :
            bos_l!= True
            bos.update()
            bos.reset()
            sprite_list= sprite.spritecollide(bos, giper_bullets, True)
            for  i in sprite_list:
                bos_f += 1
            if bos_f>5:
                bos_l = False


        # рисовка текста
        font_lost = font1.render('Пропущенно:'+ str(lost), 1, (255,255,255))
        win.blit(font_lost,(10,50))
        font_score = font1.render('Счет:'+ str(score), 1, (255,255,255))
        win.blit(font_score,(10,90))
        font_lost = font1.render('Убито:'+ str(score), 1, (255,255,255))
        win.blit(font_lost,(10,730))

    display.update()
    clock.tick(FPS)