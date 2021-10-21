import pygame
import numpy as np
import math
import random as r

(WIDTH,HEIGHT) = (900,900) # Screen Dims
SIZE = 7 # Boid Size
SPEED = 5 # Velocity Multiplier for Boids
RADIUS = 35 # Visual Radius for Boids
BOIDS = 120 # Number of Boids
ALIGNMENT_BIAS = 0.1 # Bias for Boid Alignment
COHESION_BIAS = 0.03 # Bias for Boid Cohesion
SEPERATION_BIAS = 0.04 # Bias for Boid Seperation

class Boid():
    def __init__(self, position,velocity,acceleration):
        self.position = position
        self.velocity = np.add(velocity, 0.0000000000000001)
        self.acceleration = acceleration
        self.desired = position

    def draw(self):
        pygame.draw.line(win, (0,100,200), 
        [self.position[0], self.position[1]], 
        [self.position[0] + (self.velocity[0]*(50/SPEED)) ,
        self.position[1] + (self.velocity[1]*(50/SPEED))],1)

        pygame.draw.rect(win, (255,255,255), 
        (self.position[0] - SIZE/2,
        self.position[1] - SIZE/2,SIZE,SIZE))

    def update(self):
        self.position = np.add(self.position,self.velocity)
        self.velocity = np.add(self.velocity, self.acceleration)
        self.velocity = self.velocity / np.linalg.norm(self.velocity)
        self.velocity = np.multiply(self.velocity,SPEED)
        self.acceleration = 0
        # Wrap Screen
        if b.position[0] > WIDTH:
            b.position[0] = 0
            # b.position[1] = -b.position[1] + HEIGHT
        if b.position[0] < 0:
            b.position[0] = WIDTH
            # b.position[1] = -b.position[1] + HEIGHT
        if b.position[1] > HEIGHT:
            b.position[1] = 0
            # b.position[0] = -b.position[0] + HEIGHT
        if b.position[1] < 0:
            b.position[1] = HEIGHT
            # b.position[0] = -b.position[0] + HEIGHT


def isLocal(a,b):
    distSquared = (a.position[0] - b.position[0])**2 + (a.position[1] - b.position[1])**2
    if distSquared < RADIUS**2:
        return True;
    return False


def behaviour():
    for a in boids:
        A_Desired = [0,0]
        C_Desired = [0,0]
        S_Desired = [0,0]
        flag = False
        counter = 0
        for b in boids:
            if a is not b:
                # Bpos = np.subtract(b.position,a.position)
                # angle = np.arccos(np.dot(a.position,Bpos)/(np.linalg.norm(a.position) * np.linalg.norm(Bpos)))
                if isLocal(a, b):
                    # pygame.draw.line(win, (255,0,0), [a.position[0], a.position[1]], [b.position[0],b.position[1]],1)
                    counter += 1
                    if flag:
                        A_Desired = np.add(b.velocity,A_Desired)
                        C_Desired = np.add(b.position,C_Desired)
                        norm = np.linalg.norm(a.position-b.position)
                        S_Desired = np.add(np.multiply(np.multiply(np.subtract(a.position, b.position),1/norm) ,RADIUS - norm),S_Desired)
                    else:
                        A_Desired = b.velocity
                        C_Desired = b.position
                        norm = np.linalg.norm(a.position-b.position)
                        S_Desired = np.multiply(np.multiply(np.subtract(a.position, b.position),1/norm) ,RADIUS - norm)
                        flag = True
        if flag:
            a.acceleration = np.add(a.acceleration, np.multiply(A_Desired,1/counter) * ALIGNMENT_BIAS)
            a.acceleration = np.add(a.acceleration, np.subtract( np.multiply(C_Desired,1/counter), a.position  ) * COHESION_BIAS)
            a.acceleration = np.add(a.acceleration, S_Desired * SEPERATION_BIAS)
                    
        
# ----------- MAIN --------------
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Boids")
pygame.init()

boids = []

# Spawn Boids
i = 0
while i < BOIDS:
    boids.append( Boid( [r.randrange(0,WIDTH),r.randrange(0,HEIGHT)] , [r.randrange(-200,200),r.randrange(-200,200)], [0,0] ) )
    i += 1
i = 0

while True:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        break    
    win.fill((0,0,0))

    for b in boids:
        b.update()
        b.draw()
    behaviour()
    pygame.display.update()