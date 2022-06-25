#Создай собственный Шутер!
from pygame import *
import random
from time import sleep

max_x = 700
max_y = 500
window = display.set_mode((max_x,max_y))
display.set_caption("arkanoid")
background = transform.scale(image.load("galaxy.jpg"),(max_x,max_y))


clock = time.Clock()
FPS = 60

game = True
lose = True
font.init()

number1 = 0
number2 = 0


loser = font.SysFont("Arial",36).render("LOOOOOOSER",True,(255,0,0))
winer = font.SysFont("Arial",36).render("WIIIIIIINNNERR",True,(255,0,0))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))



class Enemy(GameSprite):
    def update(self):
        global number2
        self.rect.y += self.speed
        self.reset()
        if self.rect.y > 500:
            self.rect.y = -80
            self.rect.x = random.randint(50,600)
            number2 += 1
        return number2


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))


class Player(GameSprite):
    def move(self):

        keys_pressed = key.get_pressed()  
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys_pressed[K_RIGHT] and self.rect.x < max_x - 105:
            self.rect.x += self.speed
        self.reset()    

    def shoot(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, 15, 20,-self.speed)
        bullets.add(bullet)
            
def restart():
    number1 = 0
    number2 = 0 
    window.blit(background,(0,0))


window.blit(background,(0,0))
p_x = 100
p_y = 375
p_speed = 8
player = Player("rocket.png",p_x, p_y,75,75, p_speed)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monsters.add(Enemy("ufo.png",random.randint(75,max_x-75), -80, 75,75, random.randint(1,4)))

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


while game:
    window.blit(background,(0,0))        

    if lose:
        player.move()
        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        counter1 = font.SysFont("Arial",36).render("счет " + str(number1) ,True,(255,255,0))
        counter2 = font.SysFont("Arial",36).render("пропуск " + str(number2), True,(255,255,0))

        window.blit(counter1,(1,1))
        window.blit(counter2,(1,51))    

        if number1 >= 10:
            window.blit(winer,(100,100))

            number1 = 0 

        elif number2 >= 5:
            window.blit(loser,(100,100)) 

            number2 = 0
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()

    hits = sprite.groupcollide(monsters, bullets, True, True)
    if hits:
        for i in range(1):
            monsters.add(Enemy("ufo.png",random.randint(75,max_x-75), -80, 75,75, random.randint(1,4)))
            number1 += 1
    
    hits = sprite.spritecollide(player, monsters, False)
    if hits:
        game = False
        number1 = 0
        number2 = 0 


        


    clock.tick(FPS)
    display.update()


clock.tick(FPS)
display.update()

