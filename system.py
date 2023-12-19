# gravsim - a simple gravity simulator
# @author: Noam-dv based off of las3r12

import pygame
import math
import random

weirdMultForSomeFixes = 0.8
class Planet:
    def __init__(self, mass,radius, distance,color,initialAngle, angularV):
        self.mass = mass #mass
        self.radius = radius*weirdMultForSomeFixes #circle radius
        self.distance=distance*weirdMultForSomeFixes #distance from sun
        self.color=color #color of planet 
        self.angle=initialAngle #angle rotating around sun
        self.angularV = angularV #angular velocity

class StarRand:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        for pp in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            spd = random.random() * (random.random() * 5)
            self.stars.append([x, y, spd])

    def moveStars(self, barV):
        for star in self.stars:
            star[1] += star[2] * (barV / 40)
            if star[1] > self.height:
                star[0] = random.randint(0, self.width)
                star[1] = random.randint(-10, 0)

class SolarSystem:
    def __init__(self):
        self.bigG = 6.67430E-11
        self.originaltimeStep = 1
        self.timeStep = self.originaltimeStep 
        self.barM = 10

        self.sun = Planet(1.989E30, 35, 0, (255,255,0),0, 0) # YES I KNOW ITS NOT A PLANET...,.,.....
        self.planets = [
            Planet(3.3011E23, 5,46, (218,165, 32), 0, math.radians(360/88)), # haha thanks seva for teaching me E
            Planet(4.8675E24, 8,107, (30, 144,255), 0, math.radians(360 /225)),
            Planet(5.97237E24,10, 147, (0, 255,0),0,math.radians(360 / 365)),
            Planet(6.4171E23, 7, 206, (178, 34,34),0,math.radians(360 / 687)),
            Planet(1.8982E27, 20, 740, (244, 164, 96),0,math.radians(360 / 4333))
        ]

        self.Width, self.Height = 1280, 720
        self.Screen = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption('gravsim')
        self.stars = StarRand(self.Width, self.Height)

    def drawStarrySky(self):
        for star in self.stars.stars:
            pygame.draw.circle(self.Screen, (255, 255, 255), (star[0], star[1]), 1)

    def finalPlanetDraw(self, body):
        x = self.Width // 2+body.distance * math.cos(body.angle)
        y = self.Height // 2+body.distance * math.sin(body.angle)
        pygame.draw.circle(self.Screen, body.color, (int(x), int(y)), body.radius)

    def speedBar(self, barV): # simple slider thanks stackoverflow!
        pygame.draw.rect(self.Screen, (255, 255, 255), (70, 10, 150, 10))
        pygame.draw.rect(self.Screen, (0, 0, 255), (70, 10, barV, 10))

    def runSimulation(self):
        pygame.init()
        clock = pygame.time.Clock()
        running = True
        barV = 75
        isDragging = False

        while running:
            self.Screen.fill((0, 0, 0))
            self.stars.moveStars(barV)
            self.drawStarrySky()
            pygame.draw.circle(self.Screen, self.sun.color, (self.Width // 2, self.Height // 2), self.sun.radius)

            for planet in self.planets:
                distance = planet.distance * 1000
                force = (self.bigG * self.sun.mass*planet.mass) / (distance**2)
                acceleration = force / planet.mass
                planet.angle +=planet.angularV * self.timeStep
                self.finalPlanetDraw(planet)

            self.speedBar(barV)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 70 <= event.pos[0] <= 220 and 5 <= event.pos[1] <= 15:
                        isDragging = True
                elif event.type==pygame.MOUSEBUTTONUP:
                    isDragging = False
                elif event.type==pygame.MOUSEMOTION and isDragging:
                    barV =max(0, min(event.pos[0] - 70, 150)) + 1
                    self.timeStep = self.originaltimeStep * (barV / self.barM)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

solarSystem=SolarSystem()
solarSystem.runSimulation()
