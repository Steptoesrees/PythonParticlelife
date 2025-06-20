import random
import pygame
import math
from time import sleep
import colorsys
global running
global matrix
global forcefactor


def randomMatrix():
    rows = []
    for i in range(0, ColourNum):
        row = []
        for j in range(0, ColourNum):
            row.append(random.uniform(0, 1) * 2 - 1)
        rows.append(row)
    print(rows)
    return rows


def force(r, a):
    beta = 0.5
    if (r < beta):
        return r / beta - 1
    elif beta < r and r < 1:
        return a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
    else:
        return 8

radius = 1
flowDiv = 15000000
forcefactor = 10
edgeDistance = 150
ParticleNum = 300
ColourNum = 3
Dimensions = 2
ScreenDims = 500
DeltaTime = 0.01
frictionHalfLife = 0.040
MaxRadius = 0.2
frictionfactor = math.pow(0.5, DeltaTime / frictionHalfLife)
matrix = randomMatrix()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 64, 255)
purple = (255, 0, 255)
white = (255, 255, 255)
colour6 = (0, 0, 128)
colour7 = (0, 128, 0)
colour8 = (128, 0, 0)
colour9 = (1, 1, 1)
colours = [RED, GREEN, BLUE, purple,white]
color = [0] * ParticleNum
positionsx = [0] * ParticleNum
positionsy = [0] * ParticleNum

decay = [0] * ParticleNum

velocitiesx = [0] * ParticleNum
velocitiesy = [0] * ParticleNum

for iteration in range(0, ParticleNum):
    color[iteration] = random.randint(0, ColourNum - 1)
    positionsx[iteration] = random.uniform(0, 1)
    positionsy[iteration] = random.uniform(0, 1)

    velocitiesx[iteration] = 0.0
    velocitiesy[iteration] = 0.0




def updateparticles():
    iteration = 0
    global count
    global forcefactor
    global matrix

    for iteration in range(0, ParticleNum):
        jiteration = 0
        totalforcex = 0
        totalforcey = 0
        flowxl = ((edgeDistance - positionsx[iteration]*ScreenDims)**4)/flowDiv
        flowyl = ((edgeDistance - positionsy[iteration]*ScreenDims)**4)/flowDiv
        flowxr = ((ScreenDims - edgeDistance - positionsx[iteration]*ScreenDims)**4)/flowDiv
        flowyr = ((ScreenDims - edgeDistance - positionsy[iteration]*ScreenDims)**4)/flowDiv


        for jiteration in range(0, ParticleNum):
            if jiteration == iteration:
                continue

            else:
                rx = positionsx[jiteration] - positionsx[iteration]
                ry = positionsy[jiteration] - positionsy[iteration]

                radius = math.hypot(rx,ry)

                if (radius > 0 and radius < MaxRadius):
                    f = force(radius / MaxRadius, matrix[color[iteration]][color[jiteration]])
                    decay[iteration] = 0
                    totalforcex += rx / radius * f
                    totalforcey += ry / radius * f
                if radius > MaxRadius:
                    decay[iteration] = decay[iteration]+1
                    if decay[iteration] > 10000:
                        color[iteration] = color[iteration+1]
                        positionsx[iteration] = random.uniform(0, 1)
                        positionsy[iteration] = random.uniform(0, 1)
                        decay[iteration] = 0


        totalforcex *= MaxRadius * forcefactor
        totalforcey *= MaxRadius * forcefactor


        velocitiesx[iteration] *= frictionfactor
        velocitiesy[iteration] *= frictionfactor

        velocitiesx[iteration] += totalforcex * DeltaTime
        velocitiesy[iteration] += totalforcey * DeltaTime



        positionsx[iteration] += velocitiesx[iteration] * DeltaTime
        positionsy[iteration] += velocitiesy[iteration] * DeltaTime


        positionsx[iteration] = ((positionsx[iteration])* ScreenDims)
        positionsy[iteration] = ((positionsy[iteration])* ScreenDims)

        if positionsx[iteration] < edgeDistance:
            positionsx[iteration] = ((positionsx[iteration])) + flowxl
        if positionsy[iteration] < edgeDistance:
            positionsy[iteration] = ((positionsy[iteration])) + flowyl
        if positionsx[iteration] > ScreenDims-edgeDistance:
            positionsx[iteration] = ((positionsx[iteration])) - flowxr
        if positionsy[iteration] > ScreenDims-edgeDistance:
            positionsy[iteration] = ((positionsy[iteration])) - flowyr


        if positionsx[iteration] < 0:

            positionsx[iteration] = 0
        if positionsx[iteration] > ScreenDims:
            positionsx[iteration] = ScreenDims
        if positionsy[iteration] < 0:
            positionsy[iteration] = 0
        if positionsy[iteration] > ScreenDims:
            positionsy[iteration] = ScreenDims

        pygame.draw.circle(screen, (colours[color[iteration]]), (int(positionsx[iteration]), int(positionsy[iteration])), 2)
        positionsx[iteration] = (positionsx[iteration])/ ScreenDims
        positionsy[iteration] = (positionsy[iteration])/ ScreenDims
        count = count+1

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                matrix = randomMatrix()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                forcefactor = forcefactor+1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                forcefactor = forcefactor-1
            if event.type == pygame.QUIT:
                running = False



count = 0
count2 = 0
running = True
screen = pygame.display.set_mode((ScreenDims, ScreenDims))
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    updateparticles()

    pygame.display.flip()

pygame.quit()
