import pygame 
import random
pygame.init()

screen=pygame.display.set_mode((800,700))
run=True
clock=pygame.time.Clock()
counter=0
light_color=(0,255,0)
light_color1=(0,255,0)
timer=0
spawn_timer=0
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
cars = []
cars_ver=[]
car_opp=[]
car_ver_up=[]
car_all=[]
car_coll=[]
car_coll1=[]



class TrafficLight:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.time=0
        self.color=GREEN
    def update(self):
        self.time+=1
    def draw(self,screen):
        pygame.draw.rect(screen,(light_color1),(self.x,self.y,20,20))


class Car:
    def __init__(self, x, y, speed, direction, color=BLUE):
        self.speed =speed
        self.x=x
        self.y=y
        self.direction=direction
        self.width=40
        self.length=20
        self.color=color
        self.safe_distance = 75 # min gap between cars

    def move(self,lights,cars,all_cars):
        can_move=True

        # --- same lane collision (horizontal) ---
        for other in cars:
            if other is not self:
                if abs(self.y - other.y) < 10 and (0 < (other.x - self.x) < self.safe_distance):
                    can_move = False

        # --- sideways collision (check cars in intersection) ---
        for other in all_cars:
            if other is not self:
                # detect intersection area roughly (270–430 px zone)
                if (300 < self.x < 500 and 200 < other.y < 400) or (300 < other.x < 500 and 200 < self.y < 400):
                    # if both are close to the same center intersection
                    if abs(self.x - other.x) < 40 and abs(self.y - other.y) < 40:
                        can_move = False

        # --- movement ---
        if can_move:
            if light_color1==GREEN:
                self.x+=self.speed
            elif light_color1==RED and 140<self.x<150 or 480<self.x<520:
                self.x-=self.speed
            else:
                self.x+=self.speed

    def move_opp(self,cars_oppp,all_cars):
        can_move=True
       
        for car in car_opp:
            if light_color==RED and 640<self.x<650:
                     self.x+=self.speed
                

        # --- same lane collision (opposite horizontal) ---
        for other in cars_oppp:
            if other is not self:
                if abs(self.y - other.y) < 10 and (0 < (self.x - other.x) < self.safe_distance):
                    can_move=False

        # --- sideways collision ---
        for other in all_cars:
            if other is not self:
                if (300 < self.x < 500 and 200 < other.y < 400) or (300 < other.x < 500 and 200 < self.y < 400):
                    if abs(self.x - other.x) < 40 and abs(self.y - other.y) < 40:
                        can_move = False

        # --- movement ---
        if can_move:
            if light_color1==GREEN:
                self.x-=self.speed
                
                    
            elif light_color1==RED and 140<self.x<150 and 480<self.x<520 :
                self.x+=self.speed
                if 100<self.x<250 or  480<self.x<520:
                   for car in car_opp:
                        self.x-=self.speed
                
                               
            else:
                self.x-=self.speed

    def move_ver(self,cars,all_cars):
        can_move=True

        # --- same lane collision (vertical) ---
        for other in cars:
            if other is not self:
                if abs(self.x - other.x) < 10 and (0 < (self.y - other.y) < self.safe_distance):
                    can_move=False

        # --- sideways collision ---
        for other in all_cars:
            if other is not self:
                if (300 < self.x < 500 and 200 < other.y < 400) or (300 < other.x < 500 and 200 < self.y < 400):
                    if abs(self.x - other.x) < 40 and abs(self.y - other.y) < 40:
                        can_move = False

        # --- movement ---
        if can_move:

            if light_color==GREEN:
                self.y-=self.speed
            elif light_color==RED and 400<self.y<420:
                self.y+=self.speed
           
            else:
                self.y-=self.speed
            
        

    def move_ver_up(self,cars,all_cars):
        can_move=True

        # --- same lane collision (upward vertical) ---
        for other in cars:
            if other is not self:
                if abs(self.x - other.x) < 10 and (0 < (other.y - self.y) < self.safe_distance):
                    can_move=False

        # --- sideways collision ---
        for other in all_cars:
            if other is not self:
                if (300 < self.x < 500 and 200 < other.y < 400) or (300 < other.x < 500 and 200 < self.y < 400):
                    if abs(self.x - other.x) < 40 and abs(self.y - other.y) < 40:
                        can_move = False

        # --- movement ---
        if can_move:
            if light_color==GREEN:
                self.y+=self.speed
            elif light_color==RED and 250<self.y<270:
                self.y-=self.speed
            else:
                self.y+=self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 40, 20))
    def draw_ver(self,screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 20, 40))
    def draw_coll(self):
        a=pygame.Rect(self.x-10, self.y-10, 60, 40)
        
        for hitbox in cars:
            pygame.draw.rect(screen, GRAY, a)
        for hitbox in car_opp:
            pygame.draw.rect(screen, GRAY, a)

    def draw_coll_ver(self):
        b=pygame.Rect(self.x-10, self.y-10, 40, 60)
        for hitbox in cars_ver:
          pygame.draw.rect(screen, GRAY, b)
    def draw_coll_ver_up(self):
        c=pygame.Rect(self.x-10, self.y-10, 40, 60)
        for hitbox in car_ver_up:
          pygame.draw.rect(screen, GRAY, c)

    def check_coll(self,car_verr):
        a=pygame.Rect(self.x-10, self.y-10, 60, 40)
        for car in car_verr:
          b = pygame.Rect(car.x, car.y, 20, 40)  # vertical car hitbox
          if a.colliderect(b):
            for car in cars:
                self.x-=self.speed
                break
    def check_collhor_up(self,car_hor_up):
        a=pygame.Rect(self.x-10, self.y-10, 60, 40)
        for car in car_hor_up:
          b = pygame.Rect(car.x, car.y, 20, 40)  # vertical car hitbox
          if b.colliderect(a):
            for car in car_ver_up:
                self.y-=self.speed
                break
    def check_coll_opp(self,carss):
         a=pygame.Rect(self.x-10, self.y-10, 60, 40)
         for car in carss:
          b = pygame.Rect(car.x, car.y, 20, 40)  # vertical car hitbox
          if b.colliderect(a):
            for car in car_ver_up:
                self.y-=self.speed
                break
    def check_coll_opp_down(self,carss):
         a=pygame.Rect(self.x-10, self.y-10, 60, 40)
         for car in carss:
          b = pygame.Rect(car.x, car.y, 20, 40)  # vertical car hitbox
          if b.colliderect(a):
            for car in car_ver_up:
                self.y+=self.speed
                break
          



        

light1 = TrafficLight(150, 270)
light2=TrafficLight(500, 270)

lights = [light1 ,light2]


# --- Main Loop ---
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    timer+=1
    spawn_timer+=1
    if  timer<60:
        light_color1=GREEN
    if 120<timer<240:
        light_color1=RED
    if  timer==240:
        timer=0
    if  light_color1==RED:
        light_color=GREEN
    else:
        light_color=RED

    direction=random.choice(["horizontal","vertical","ver_right"])
    if spawn_timer>=40:
        spawn_timer=0
        if direction=="horizontal":
            which_dir1=random.choice(["left","right"])
            if which_dir1=="left":
                car_x=random.randint(0,21)
                car_y=380
                cars.append(Car(car_x, car_y, 2, "horizontal", BLUE))
                car_all.append(cars[-1])
            elif which_dir1=="right":
                car_y=320
                car_x=700
                car_opp.append(Car(car_x, car_y, 2, "horizontal", BLUE))
                car_all.append(car_opp[-1])
        elif direction=="vertical":
            which_dir=random.choice(["left","up"])
            if which_dir=="left":
                car_x=random.randint(680,701)
                car_y=260
                cars_ver.append(Car(car_y, car_x, 2, "vertical", BLUE))
                car_all.append(cars_ver[-1])
            elif which_dir=="up":
                car_x=0
                car_y=200
                car_ver_up.append(Car(car_y, car_x, 2, "vertical", BLUE))
                car_all.append(car_ver_up[-1])
        elif direction=="ver_right":
            which_dir=random.choice(["down","up"])
            if which_dir=="down":
                car_x=700
                car_y=600
                cars_ver.append(Car(car_y, car_x, 2, "vertical", BLUE))
                car_all.append(cars_ver[-1])
            elif which_dir=="up":
                car_x=0
                car_y=550
                car_ver_up.append(Car(car_y, car_x, 2, "vertical", BLUE))
                car_all.append(car_ver_up[-1])


    for light in lights:
        light.update()

    for car in cars[:]:
        car.move(lights, cars, car_all)
    for car in cars_ver:
        car.move_ver(cars_ver, car_all)
    for car in car_opp:
        car.move_opp(car_opp, car_all)
    for car in car_ver_up:
        car.move_ver_up(car_ver_up, car_all)

    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, 300, 800, 120))  # horizontal road
    pygame.draw.rect(screen, GRAY, (180, 0, 120, 700))  # vertical left
    pygame.draw.rect(screen, GRAY, (530, 0, 120, 700))  # vertical right
    pygame.draw.rect(screen, light_color, (310, 430, 20, 20))
    pygame.draw.rect(screen, light_color, (660, 425, 20, 20))   

    for light in lights:
        light.draw(screen)
    for car in cars :
        car.draw_coll()
    for car in car_opp:
        car.draw_coll()
    for car in cars_ver:
        car.draw_coll_ver()
    for car in car_ver_up:
        car.draw_coll_ver_up()
    for car in cars:
        car.draw(screen)
    for car in cars_ver:
        car.draw_ver(screen)
    for car in car_opp:
        car.draw(screen)
    for car in car_ver_up:
        car.draw_ver(screen)
    for car in cars:
        car.check_coll(cars_ver)
    for car in car_ver_up:
        car.check_collhor_up(cars)
    for car in car_ver_up:
        car.check_coll_opp(car_opp)
    for car in cars_ver:
        car.check_coll_opp_down(car_opp)

  
    

    

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
