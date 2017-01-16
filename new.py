import os, sys, math, pygame, pygame.mixer, euclid, time
from pygame.locals import *
import random


black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
timediff = 1
colors = [white, green, blue, red, yellow]
screen = None
screen_size = None
clock = pygame.time.Clock()
center_circle = None
Road1 = None
Road2 = None
image = None
rect = None

def initialize():
    global center_circle, Road1, Road2, screen, screen_size

    screen_size = screen_width, screen_height = 1000, 800
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Traffic Simulation")
    screen.fill(white)
    Road1 = MyRect(euclid.Vector2(0, 200), (1000, 150), green)
    Road1.display()
    Road2 = MyRect(euclid.Vector2(430, 0), (150, 800), black)
    Road2.display()
    circle_boundary = Mycircle(euclid.Vector2(screen_width/2, screen_height/3), 31, white, width=2)
    circle_boundary.display()
    center_circle = Mycircle(euclid.Vector2(screen_width/2, screen_height/3), 30, green)
    center_circle.display()

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("grass.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, 0
Background = Background()

class Mycircle:
    def __init__(self, position, size, color = (255, 255, 255),velocity = euclid.Vector2(0, 0) , width = 0):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.size, self.width)

    def changeColor(self, color):
        self.color = color

    def move(self):
        self.position += self.velocity* timediff

    def change_velocity(self, velocity):
        self.velocity = velocity

class MyRect:
    def __init__(self, position, size, color, velocity = euclid.Vector2(0, 0), text = False, arrival = 0, departure = 0, final_position = 1000000):
        self.position = position
        self.size = size
        self.color = color
        self.velocity = velocity
        self.text = text
        self.arrival = arrival
        self.departure = departure
        self.final_position = final_position

    def display(self):
        # if not self.text == False:
        #     font = pygame.font.SysFont('Arial', 7)
        #     screen.blit(font.render(self.text, True, (255, 255, 255)), (self.position.x+2, self.position.y+2))

        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.rect(screen, self.color, Rect((rx, ry), self.size))

    def move(self):
        self.position += self.velocity* timediff

    def change_velocity(self, velocity):
        self.velocity = velocity

initialize()
cars = []

arrivals = [(1, 4.706264455118397), (2, 15.594714535598944), (3, 18.829246685923685), (4, 30.226438060158664), (5, 30.375982045752924), (6, 42.595158931138315), (7, 47.11692845871228), (8, 62.351645833870094), (9, 66.75744207433607), (10, 78.7851392090482), (11, 80.97582562985436), (12, 81.61560864274665), (13, 85.4266627261512), (14, 89.86232972754983), (15, 93.04483593049945), (16, 103.17567536698627), (17, 106.40815567870084), (18, 115.31161157625463), (19, 125.27690661377648), (20, 127.86986765210443), (21, 142.56061076190417), (22, 145.81383671299253), (23, 156.0280717265405), (24, 157.47032040319183), (25, 160.06557203961177), (26, 164.97120224328467), (27, 165.04918324817675), (28, 172.42785253817047), (29, 175.25524771954292), (30, 179.43381541768744), (31, 184.67240422064157), (32, 184.77744519838924)]
departures = [(1, 4.706264455118397), (2, 15.594714535598944), (3, 18.829246685923685), (4, 72.01023786310968), (5, 74.26509456505437), (6, 76.16141127153269), (7, 77.78199074182288), (8, 79.80235288794665), (9, 81.91760664733539), (10, 83.5576261642781), (11, 85.27316218047328), (12, 87.1011985703569), (13, 88.76505227418525), (14, 89.86232972754983), (15, 93.04483593049945), (16, 141.8630027263266), (17, 143.7539026497418), (18, 145.82676501265598), (19, 148.05995926402443), (20, 149.87148605895217), (21, 151.817146806803), (22, 153.9375567569273), (23, 156.0280717265405), (24, 157.47032040319183), (25, 160.06557203961177), (26, 164.97120224328467), (27, 165.04918324817675)]
ini = 20

for i in range(100):
   x = random.randint(ini, ini + 10)
   ini += 10
   cars.append(MyRect(euclid.Vector2(430-x*10, 210), (12, 10), random.choice(colors), text = `i+1`, velocity=euclid.Vector2(15, 0)))

sorted(cars, key= lambda MyRect: MyRect.position.x)
for car in cars:
    print car.position.x

def reprint():
    global Road1, Road2, circle_boundary, center_circle, screen_width, screen_height
    screen.blit(Background.image, Background.rect)
    Road1 = MyRect(euclid.Vector2(0, 200), (1000, 150), black)
    Road1.display()
    Road2 = MyRect(euclid.Vector2(430, 0), (150, 800), black)
    Road2.display()

def work():
    now = time.time()
    lastSwitch = time.time()
    global timediff, center_circle, green, red
    flag = True
    color = 'green'
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        dtime_ms = clock.tick(60)
        timediff = dtime_ms/100.0
        reprint()
        for car in cars:
            if color == 'red':
                x = car.position.x
                if x < car.final_position:
                    car.change_velocity(euclid.Vector2(15, 0))
                else:
                    car.change_velocity(euclid.Vector2(0, 0))
            else:
                car.change_velocity(euclid.Vector2(15, 0))
            car.move()
            car.display()

        if color == 'red' and time.time()-lastSwitch > 5:
            lastSwitch = time.time()
            color = 'green'
            center_circle.changeColor(green)
            for car in cars:
                car.final_position = 1000000
        if color == 'green' and time.time()-lastSwitch > 5:
            lastSwitch = time.time()
            color = 'red'
            center_circle.changeColor(red)
            i = 1
            for car in cars:
                if car.position.x < 420:
                    car.final_position = 430-20*i
                    i += 1
        center_circle.display()
        pygame.display.flip()

work()
pygame.quit()