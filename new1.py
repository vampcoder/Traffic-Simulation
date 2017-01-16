import os, sys, math, pygame, pygame.mixer, euclid, time
from pygame.locals import *
import random
import Tkinter
from collections import deque # double-ended queue

import simpy
from simpy.util import start_delayed
from operator import itemgetter


Velocity, NOC, SwitchTime = None, None, None

class gui():
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title = "Traffic Inputs"
        self.initialize()
        self.root.mainloop()

    def initialize(self):
        self.root.grid()

        label1 = Tkinter.Label()
        label1.grid(column = 2, row = 1)

        self.entry1 = Tkinter.Entry()
        self.entry1.grid(column=3, row=1, sticky='EW')

        label1 = Tkinter.Label(text = u"No of Cars :", anchor = "w", fg = "black")
        label1.grid(column = 1, row = 1)


        self.entry2 = Tkinter.Entry()
        self.entry2.grid(column=3, row=2, sticky='EW')

        label2 = Tkinter.Label(text=u"Velocity of car :", anchor="w", fg="black")
        label2.grid(column=1, row=2)


        self.entry3 = Tkinter.Entry()
        self.entry3.grid(column=3, row=3, sticky='EW')

        label3 = Tkinter.Label(text=u"Light Switching Time : ", anchor="w", fg="black")
        label3.grid(column=1, row=3)

        button = Tkinter.Button(text=u"Submit", command = self.SubmitWork)
        button.grid(column=3, row=4)
        self.root.grid_columnconfigure(0, weight = 4)

        self.root.resizable(True, True)
    def quit(self):
        self.root.destroy()
        pass

    def SubmitWork(self):
        global Velocity, NOC, SwitchTime

        NOC = int(self.entry1.get())
        Velocity = int(self.entry2.get())
        SwitchTime = int(self.entry3.get())

        #print Velocity, NOC, SwitchTime
        self.quit()

def inputGui():
    G = gui()

inputGui()

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
bigCircle = None
all_circles = []
all_lines = []
Road1 = None
Road2 = None
image = None
rect = None

def initialize():
    global center_circle, Road1, Road2, screen, screen_size, bigCircle
    screen_size = screen_width, screen_height = 1000, 700
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Traffic Simulation")
    screen.fill(white)
    Road1 = MyRect(euclid.Vector2(0, 200), (1000, 150), black, final_position=0)
    Road2 = MyRect(euclid.Vector2(430, 0), (150, 800), black, final_position=0)
    circle = Mycircle(euclid.Vector2(420, 275), 10, green)
    all_circles.append(circle)
    circle = Mycircle(euclid.Vector2(505, 190), 10, red)
    all_circles.append(circle)
    circle = Mycircle(euclid.Vector2(590, 275), 10, red)
    all_circles.append(circle)
    circle = Mycircle(euclid.Vector2(505, 360), 10, red)
    all_circles.append(circle)
    line = Myline((0, 275), (400, 275), (255, 255, 0))
    all_lines.append(line)
    line = Myline((505, 0), (505, 170), (255, 255, 0))
    all_lines.append(line)
    line = Myline((1000, 275), (610, 275), (255, 255, 0))
    all_lines.append(line)
    line = Myline((505, 380), (505, 800), (255, 255, 0))
    all_lines.append(line)
    bigCircle = Mycircle(euclid.Vector2(505, 275), 20, white)

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("grass.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, 0
Background = Background()

class Myline:
    def  __init__(self, startpos, endpos, color, width = 1):
        self.startpos = startpos
        self.endpos = endpos
        self.color = color
        self.width = width

    def display(self):
        sx, sy = int(self.startpos[0]), int(self.startpos[1])
        ex, ey = int(self.endpos[0]), int(self.endpos[1])
        pygame.draw.line(screen, self.color, (sx, sy), (ex, ey), self.width)

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
    def __init__(self, position, size, color, final_position, velocity = euclid.Vector2(0, 0), text = False, arrival = 0, departure = 0, ):
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

ini = 20
cars1 =[]
for i in range(NOC):
   x = random.randint(ini, ini + 10)
   ini += 10
   cars1.append(MyRect(euclid.Vector2(430-x*10, 310), (12, 10), random.choice(colors), text = `i+1`, velocity=euclid.Vector2(Velocity, 0), final_position=100000000))

ini = 20
cars2 = []
for i in range(NOC):
   x = random.randint(ini, ini + 10)
   ini += 10
   cars2.append(MyRect(euclid.Vector2(450, 188-x*10), (10, 12), random.choice(colors), text = `i+1`, velocity=euclid.Vector2(0, Velocity), final_position=10000000))

ini = 20
cars3 = []
for i in range(NOC):
   x = random.randint(ini, ini + 10)
   ini += 10
   cars3.append(MyRect(euclid.Vector2(580+x*10, 230), (12, 10), random.choice(colors), text = `i+1`, velocity=euclid.Vector2(-Velocity, 0), final_position=-10000000))

ini = 20
cars4 = []
for i in range(NOC):
   x = random.randint(ini, ini + 10)
   ini += 10
   cars4.append(MyRect(euclid.Vector2(540, 350 + x*10), (10, 12), random.choice(colors), text = `i+1`, velocity=euclid.Vector2(0, -Velocity), final_position=-10000000))


sorted(cars1, key= lambda MyRect: MyRect.position.x)
sorted(cars2, key= lambda MyRect: MyRect.position.x)
#cars1.reverse()



def reprint():
    global Road1, Road2, circle_boundary, center_circle, screen_width, screen_height
    screen.blit(Background.image, Background.rect)
    Road1.display()
    Road2.display()
    for circle in all_circles:
        circle.display()
    for line in all_lines:
        line.display()
    bigCircle.display()

def changeLight(turn):
    global all_circles
    for i in range(len(all_circles)):
        if i == turn:
            all_circles[i].changeColor(green)
        else:
            all_circles[i].changeColor(red)
        all_circles[i].display()

def perform(turn):
    global cars1, cars2, cars3, cars4
    if turn == 0:
        for car in cars1:
            car.move()
            car.display()
        for car in cars2:
            y = car.position.y
            if int(y) < car.final_position:
                car.move()
            car.display()
        for car in cars3:
            x = car.position.x
            if int(x) > car.final_position:
                car.move()
            car.display()
        for car in cars4:
            y = car.position.y
            if int(y) > car.final_position:
                car.move()
            car.display()
    elif turn == 1:
        for car in cars1:
            x = car.position.x
            if int(x) < car.final_position:
                car.move()
            car.display()
        for car in cars2:
            car.move()
            car.display()
        for car in cars3:
            x = car.position.x
            if int(x) > car.final_position:
                car.move()
            car.display()
        for car in cars4:
            y = car.position.y
            if int(y) > car.final_position:
                car.move()
            car.display()
    elif turn == 2:
        for car in cars1:
            x = car.position.x
            if int(x) < car.final_position:
                car.move()
            car.display()
        for car in cars2:
            y = car.position.y
            if int(y) < car.final_position:
                car.move()
            car.display()
        for car in cars3:
            car.move()
            car.display()
        for car in cars4:
            y = car.position.y
            if int(y) > car.final_position:
                car.move()
            car.display()
    else:
        for car in cars1:
            x = car.position.x
            if int(x) < car.final_position:
                car.move()
            car.display()
        for car in cars2:
            y = car.position.y
            if int(y) < car.final_position:
                car.move()
            car.display()
        for car in cars3:
            x = car.position.x
            if int(x) > car.final_position:
                car.move()
            car.display()
        for car in cars4:
            car.move()
            car.display()

def printPosition():
    global cars1, cars2
    for car in cars1:
        print car.position.x , car.final_position, " " ,
    print " "

    for car in cars2:
        print car.position.x , car.final_position, " " ,
    print ""
    print ""


#printPosition()

def changeFinalPostion(turn):
    if turn == 0:
        for car in cars1:
            car.final_position = 1000000
        i = 1
        for car in cars2:
            if int(car.position.y) < 200:
                car.final_position = 200 - 20 * i
                i += 1
        i = 1
        for car in cars3:
            if int(car.position.x) >580:
                car.final_position = 580 + 20*i
                i += 1
        i = 1
        for car in cars4:
            if int(car.position.y) > 350:
                car.final_position = 350+20*i
                i += 1
    elif turn == 1:
        i = 1
        for car in cars1:
            if int(car.position.x) < 430:
                car.final_position = 430-20*i
                i += 1
        for car in cars2:
            car.final_position = 1000000
        i = 1
        for car in cars3:
            if int(car.position.x) > 580:
                car.final_position = 580 + 20 * i
                i += 1
        i = 1
        for car in cars4:
            if int(car.position.y) > 350:
                car.final_position = 350 + 20 * i
                i += 1
    elif turn == 2:
        i = 1
        for car in cars1:
            if int(car.position.x) < 430:
                car.final_position = 430 - 20 * i
                i += 1
        i = 1
        for car in cars2:
            if int(car.position.y) < 200:
                car.final_position = 200 - 20 * i
                i += 1
        for car in cars3:
            car.final_position = -10000000000
        i = 1
        for car in cars4:
            if int(car.position.y) > 350:
                car.final_position = 350 + 20 * i
                i += 1
    else:
        i = 1
        for car in cars1:
            if int(car.position.x) < 430:
                car.final_position = 430 - 20 * i
                i += 1
        i = 1
        for car in cars2:
            if int(car.position.y) < 200:
                car.final_position = 200 - 20 * i
                i += 1
        i = 1
        for car in cars3:
            if int(car.position.x) > 580:
                car.final_position = 580 + 20 * i
                i += 1
        for car in cars4:
            car.final_position = -1000000000

print NOC, Velocity, SwitchTime
def work():
    #inp = int(inputbox.ask(screen, 'Message'))

    #print inp
    turn = 0
    now = time.time()
    lastSwitch = time.time()-20
    global timediff, center_circle, green, red, cars1, cars2, SwitchTime
    flag = True


    while flag:

        #printPosition()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        dtime_ms = clock.tick(60)
        timediff = dtime_ms / 100.0
        reprint()
        if time.time()-lastSwitch > SwitchTime:
            if turn == 0:
                turn = 1
            elif turn == 1:
                turn = 2
            elif turn == 2:
                turn = 3
            else:
                turn = 0
            lastSwitch = time.time()
            changeFinalPostion(turn)
            changeLight(turn)

        perform(turn)
        pygame.display.flip()

work()
pygame.quit()

from numpy import random
class Struct(object):
   def __init__(self, **kwargs):
      self.__dict__.update(kwargs)
random.seed([1, 2, 3])
end_time= 20000.0
arrival_rate= 0.2
t_interarrival_mean = 1.0 / arrival_rate
t_green= 30.0; t_red= 40.0
t_depart_left= 1.6; t_depart_mode= 2.0; t_depart_right= 2.4
queue= deque()
arrival_count= departure_count= 0

Q_stats= Struct(count=0, cars_waiting=0)
W_stats= Struct(count=0, waiting_time=0.0)
printOutput = []
arrivals = []
departures = []
queues =[]
def arrival():
   global arrival_count, env, light, queue, printOutput, Q_stats, W_stats
   while True:
      arrival_count+= 1
      if light == 'red' or len(queue):
         queue.append((arrival_count, env.now))
         # print("Car #%d arrived and joined the queue at position %d at time"
         #   "%.3f." % (arrival_count, len(queue), env.now))
         otp = [arrival_count, "Car #%d arrived and joined the queue at position %d at time"
           "%.3f." % (arrival_count, len(queue), env.now)]
         printOutput.append(otp)
         arrivals.append((arrival_count, env.now))
         queues.append((arrival_count, len(queue)))
      else:
         # print("Car #%d arrived to a green light with no cars waiting at time"
         #   "%.3f." % (arrival_count, env.now))
         otp = [arrival_count, "Car #%d arrived to a green light with no cars waiting at time"
           "%.3f." % (arrival_count, env.now)]
         printOutput.append(otp)
         arrivals.append((arrival_count, env.now))
         W_stats.count+= 1
         departures.append((arrival_count, env.now))
         queues.append((arrival_count, len(queue)))
      yield env.timeout( random.exponential(t_interarrival_mean))

def departure():
   global env, queue, printOutput, Q_stats, W_stats
   while True:
      car_number, t_arrival= queue.popleft()
      # print("Car #%d departed at time %.3f, leaving %d cars in the queue."
      #   % (car_number, env.now, len(queue)))
      otp = [car_number, "Car #%d departed at time %.3f, leaving %d cars in the queue."
        % (car_number, env.now, len(queue))]
      printOutput.append(otp)
      W_stats.count+= 1
      W_stats.waiting_time+= env.now - t_arrival
      departures.append((car_number, env.now))
      if light == 'red' or len(queue) == 0:
         return
      delay= random.triangular(left=t_depart_left, mode=t_depart_mode,
        right=t_depart_right)
      yield env.timeout(delay)

def light():
   global env, light, printOutput, Q_stats, W_stats
   while True:
      light= 'green'
      # print("\nThe light turned green at time %.3f." % env.now)
      otp = [-1, "\nThe light turned green at time %.3f." % env.now]
      printOutput.append(otp)
      if len(queue):
         delay= random.triangular(left=t_depart_left, mode=t_depart_mode,
           right=t_depart_right)

         start_delayed(env, departure(), delay=delay)
      yield env.timeout(t_green)
      light= 'red'
      # print("\nThe light turned red at time %.3f."   % env.now)
      otp = [-1, "\nThe light turned red at time %.3f."   % env.now]
      printOutput.append(otp)
      yield env.timeout(t_red)

def monitor():
   global env, Q_stats, Q_stats, W_stats
   while True:
      Q_stats.count+= 1
      Q_stats.cars_waiting+= len(queue)
      yield env.timeout(1.0)

env= simpy.Environment()
env.process(light())
t_first_arrival= random.exponential(t_interarrival_mean)
start_delayed(env, arrival(), delay=t_first_arrival)
env.process(monitor())
env.run(until=end_time)

opt = ["\n\n      *** Statistics ***\n\n"]
printOutput.append(opt)
opt = ["Mean number of cars waiting: %.3f\n\n"
  % (Q_stats.cars_waiting / float(Q_stats.count))]
printOutput.append(opt)
opt = ["Mean waiting time (seconds): %.3f\n\n"
  % (W_stats.waiting_time / float(W_stats.count))]
printOutput.append(opt)

sorted(departures, key = itemgetter(0))
sorted(arrivals, key = itemgetter(0))
sorted(queues, key = itemgetter(0))

for line in printOutput:

    print len(line), line[-1]

class OutputGui():
    def __init__(self):
        self.root = Tkinter.Tk()

        txt_frm = Tkinter.Frame(self.root, width = 500, height = 800)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = Tkinter.Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        flag = True
        j = 1.0
        self.txt.insert(str(j), printOutput[0][-1])
        for i in range(len(printOutput)):
            if len(printOutput[i]) > 1:
                if printOutput[i][0] != -1 and printOutput[i][0] < NOC:
                    self.txt.insert(str(j), printOutput[i][-1])
                    j += 1
                    self.txt.insert(str(j), "\n")
                    j += 1
                if printOutput[i][0] == -1:
                    if flag:
                        self.txt.insert(str(j), printOutput[i][-1])
                        j += 1
                        self.txt.insert(str(j), "\n")
                        j += 1
                if printOutput[i][0] >= NOC:
                    flag = False

        self.txt.insert(str(j), printOutput[-3][0])
        j += 1
        self.txt.insert(str(j), printOutput[-2][0])
        j += 1
        self.txt.insert(str(j), printOutput[-1][0])
        j += 1
        # # create a Scrollbar and associate it with txt
        scrollb = Tkinter.Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
        self.root.mainloop()

OutputGui()