import pygame
import random
import sys
import os



#Background set:
class Background:
    
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.background_img=pygame.image.load("images/background.jpg")
        self.bg_img=pygame.transform.scale(self.background_img,(self.width,self.height))
        self.bg_x=0
        self.bg_y=0

    def draw(self,gameDisplay):
        gameDisplay.blit(self.bg_img,(self.bg_x,self.bg_y))


#Start Button
class StartButton:
    def __init__(self):
        
        self.font = pygame.font.Font(None, 36)
        self.button_text = self.font.render("Start Game", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(400, 300))

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0, 255, 0), self.button_rect, border_radius=10)
        gameDisplay.blit(self.button_text, self.button_rect.topleft)
        

    def clicked(self, mouse_pos):
        return self.button_rect.collidepoint(mouse_pos)

# Player car Class
class Playercar:
    def __init__(self,width,height,speed,x,y):
        
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.speed=speed
        self.carimg=pygame.image.load("images/car.png")      
        self.car=pygame.transform.scale(self.carimg,(width,height))
        self.crashed=False
        self.sound_method=Sound()
        
    def draw(self,gameDisplay):
        gameDisplay.blit(self.car,(self.x,self.y))
            
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 115:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 655:
            self.x += self.speed

    def check_collision(self, enemy_cars):
        for enemy_car in enemy_cars.enemy_instances:
            if (
                    self.x < enemy_car['x'] + 40 and
                    self.x + 40 > enemy_car['x'] and
                    self.y < enemy_car['y'] + 80 and
                    self.y + 80 > enemy_car['y']):
                self.crashed = True  # Set the crashed flag
                    
        
# Score        
class Scoretext:
    def __init__(self):
        
        self.x=10
        self.y=10
        self.count=0
        self.white=(255,255,255)
        self.font=pygame.font.Font(None,25)

        
        
    def draw(self,gameDisplay):
        
        text = self.font.render("Score: " + str(self.count), True, self.white)
        gameDisplay.blit(text, (self.x, self.y))

    def increment_score(self):
        self.count += 1
        
        
#Sound
class Sound:
    def __init__(self):
        self.sound=os.path.join('Car_crash_sound.mp3')


    def play(self):
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play()
        
      
#Crash
class Crash:
    def __init__(self,player_car):
        self.player_car=player_car
        self.sound_method=Sound()
        self.width=40
        self.height=80
        self.image = pygame.image.load("images/crash.png")
        self.img=pygame.transform.scale(self.image,(self.width,self.height))
        
        
    def draw(self,gameDisplay):
        
        self.sound_method.play()
        gameDisplay.blit(self.img,(self.player_car.x,self.player_car.y))
        pygame.time.delay(3000)
        print("You crashed! Total Score:",game_window.score.count)
        
        pygame.quit()
        sys.exit()

    
    


##enemy car
class Enemycar:
    def __init__(self,score):
        
        self.score = score
        self.speed = 7
        height=80
        width=40
        self.enemy = pygame.image.load("images/enemy.jpg")
        self.car1=pygame.transform.scale(self.enemy,(width,height))
        self.enemy1 = pygame.image.load("images/enemy2.png")
        self.car2=pygame.transform.scale(self.enemy1,(width,height))
        self.enemy2 = pygame.image.load("images/enemy3.jpg")
        self.car3=pygame.transform.scale(self.enemy2,(width,height))
        self.enemy_cars = [self.car1, self.car2, self.car3]  # List to store enemy car images
        self.spawn_timer = 0
        self.enemy_instances = []  # List to store enemy car instances
        

    def move(self):
        for enemy_car in self.enemy_instances:
            enemy_car['y'] += self.speed
            if enemy_car['y'] > 600:
                self.enemy_instances.remove(enemy_car)
                self.score.increment_score()

            
        self.spawn_timer += 1
        if self.spawn_timer == 50:  # Adjust spawn rate as needed
            self.spawn()
            self.spawn_timer = 0

    
    def spawn(self):
        self.x = random.randint(120, 660)
        self.y = 0
        enemy_index = random.randint(0, len(self.enemy_cars) - 1)
        enemy_image = self.enemy_cars[enemy_index]
        enemy_car = {'x': self.x, 'y': self.y, 'image': enemy_image}
        self.enemy_instances.append(enemy_car)

    def draw(self, gameDisplay):
        for enemy_car in self.enemy_instances:
            gameDisplay.blit(enemy_car['image'], (enemy_car['x'], enemy_car['y']))
        
            
## for grass           
class Grass:
    def __init__(self):
        self.grass =pygame.image.load("images/grass.jpg")
        
    def draw(self,gameDisplay):
        gameDisplay.blit(self.grass, (0, 0))
        gameDisplay.blit(self.grass, (700, 0))
        
        
## for track       
class Track:
    def __init__(self ):
        self.width=10
        self.height=600
        
        self.yellow_strip = pygame.image.load("images/yellow_strip.png")
        self.white_strip =pygame.image.load("images/white_strip.jpg")
        self.white=pygame.transform.scale(self.white_strip,(self.width,self.height))
       
        
    def draw(self,gameDisplay):
        gameDisplay.blit(self.yellow_strip, (400, 0))
        gameDisplay.blit(self.yellow_strip, (400, 150))
        gameDisplay.blit(self.yellow_strip, (400, 300))
        gameDisplay.blit(self.yellow_strip, (400, 450))
        gameDisplay.blit(self.white, (100, 0))
        gameDisplay.blit(self.white, (700, 0))


class GameWindow:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Game')
        
        self.car = Playercar(40,80,5,386,510)
        self.score = Scoretext()
        self.enemycars=Enemycar(self.score)
        self.grass=Grass()
        self.track=Track()
        self.crash=Crash(self.car)
        self.paused = False
        self.start=True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.clicked(mouse_pos):
                    self.start = not self.start  # Start the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'p' to pause/unpause
                    self.paused = not self.paused
                elif event.key == pygame.K_r:  # Press 'r' to reset
                    self.reset_game()

    def reset_game(self):
        # Reset player position and status
        self.car.x = 386
        self.car.y = 510
        self.car.crashed = False
        self.score.count = 0

         # Reset enemy cars
        self.enemycars.enemy_instances.clear()

    def run_game(self):
        clock = pygame.time.Clock()
        
        while True:
            
            self.handle_events()
            if not self.start:
                self.gameDisplay.fill((128, 128, 128))
                
                self.score.draw(self.gameDisplay)
                self.grass.draw(self.gameDisplay)
                self.track.draw(self.gameDisplay)
                self.car.draw(self.gameDisplay)
            
                self.score.draw(self.gameDisplay)
            
                self.enemycars.draw(self.gameDisplay)
                
            
            # Only update the game if it's not paused
                if not self.paused:  
                    keys = pygame.key.get_pressed()
                    self.car.move(keys)
                    self.enemycars.move()

            if self.car.crashed:
                self.crash.draw(self.gameDisplay)
            self.car.check_collision(self.enemycars)


            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    
    game_window = GameWindow()
    background=Background(800,600)
   
    background.draw(game_window.gameDisplay)
    start_button = StartButton()
    start_button.draw(game_window.gameDisplay)
    
    game_window.run_game()
    
    
  
    
        
        


    
