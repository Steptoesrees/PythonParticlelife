import math
import random
import pygame
from time import sleep

from time import sleep

global totalforcey
global totalforcex


def randomMatrix():
    rows = []
    for i in range(0, ColourNum):
        row = []
        for j in range(0, ColourNum):
            row.append(random.uniform(0, 1) * 2 - 1)
        rows.append(row)
    return rows


def force(r, a):
    beta = 0.3
    if (r < beta):
        return r / beta - 1
    elif beta < r and r < 1:
        return a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
    else:
        return 0

pygame.font.init()
forcefactor = 20
particleNum = 1000
ColourNum = 3
Dimensions = 2
ScreenDims = 800
DeltaTime = 0.02
frictionHalfLife = 0.040
MaxRadius = 0.6
frictionfactor = math.pow(0.5, DeltaTime / frictionHalfLife)
matrix = randomMatrix()


class rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (point.x * screenSize >= self.x and
                point.x * screenSize <= self.x + self.width and
                point.y * screenSize >= self.y and
                point.y * screenSize <= self.y + self.height)

    def intersects(self, ranges):
        return (ranges.x > self.x + self.width or
                ranges.x + ranges.width < self.x or
                ranges.y < self.y + self.height or
                ranges.y + ranges.height > self.y)


class circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.area = radius * radius

    def contains(self, point):
        d = math.pow((point.x * screenSize - self.x), 2) + math.pow((point.y * screenSize - self.y), 2)
        return d <= self.radius

    def intersects(self, ranges):
        xDist = abs(ranges.x - self.x)
        yDist = abs(ranges.y - self.y)

        r = self.radius
        w = ranges.width
        h = ranges.height

        edges = math.pow((xDist - w), 2) + math.pow((yDist - h), 2)

        if xDist > (r + w) or yDist > (r + h):
            return False
        if xDist <= w or yDist <= h:
            return True
        return edges <= self.area


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocitiesx = 0
        self.velocitiesy = 0
        self.colour = random.randint(0, 2)

    def updateloc(self, x, y):
        self.x = x
        self.y = y


class quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        width = self.boundary.width
        height = self.boundary.height
        nw = rectangle(x, y, width / 2, height / 2)
        self.northwest = quadtree(nw, self.capacity)
        ne = rectangle(x + width / 2, y, width / 2, height / 2)
        self.northeast = quadtree(ne, self.capacity)
        sw = rectangle(x, y + height / 2, width / 2, height / 2)
        self.southwest = quadtree(sw, self.capacity)
        se = rectangle(x + width / 2, y + height / 2, width / 2, height / 2)
        self.southeast = quadtree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if self.boundary.contains(point) == False:
            return

        if len(self.points) < self.capacity:
            self.points.append(point)
        else:
            if self.divided == False:
                self.subdivide()

            self.northwest.insert(point)
            self.northeast.insert(point)
            self.southwest.insert(point)
            self.southeast.insert(point)

    def query(self, ranges, found):
        if found == False:
            found = []
        if ranges.intersects(self.boundary) == False:
            return found
        else:
            for point in self.points:
                if ranges.contains(point):
                    found.append(point)
        if self.divided:
            self.northwest.query(ranges, found)
            self.northeast.query(ranges, found)
            self.southwest.query(ranges, found)
            self.southeast.query(ranges, found)

        return found

    def show(self, screen):
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height), 1)
        if self.divided == True:
            self.northwest.show(screen)
            self.northeast.show(screen)
            self.southwest.show(screen)
            self.southeast.show(screen)


screenSize = ScreenDims
capacity = 2
colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
boundary = rectangle(0, 0, screenSize, screenSize)

qt = quadtree(boundary, capacity)

screen = pygame.display.set_mode((screenSize, screenSize))

particles = [0] * particleNum
for i in range(0, particleNum):
    particles[i] = point(random.uniform(0, 1), random.uniform(0, 1))
    qt.insert(particles[i])

running = True
while running:
    screen.fill((0, 0, 0))
    qt.show(screen)
    for po in particles:

        totalforcex = 0
        totalforcey = 0
        ranges = circle(po.x * ScreenDims, po.y * ScreenDims, 100)
        points = qt.query(ranges, [])

        for p in points:

            if po == p:
                continue
            else:
                rx = p.x - po.x
                ry = p.y - po.y
                radius = math.sqrt(rx ** 2 + ry ** 2)
                if radius <= MaxRadius and radius > 0:
                    f = force(radius / MaxRadius, matrix[p.colour][po.colour])

                    totalforcex += rx / radius * f
                    totalforcey += ry / radius * f

        totalforcey *= MaxRadius * forcefactor
        totalforcex *= MaxRadius * forcefactor

        po.velocitiesx *= frictionfactor
        po.velocitiesy *= frictionfactor
        po.velocitiesx *= totalforcex * DeltaTime
        po.velocitiesy *= totalforcey * DeltaTime

        po.x += (po.velocitiesx) * (DeltaTime)
        po.y += (po.velocitiesy) * (DeltaTime)

        po.x = po.x * ScreenDims
        po.y = po.y * ScreenDims
        if po.x < -1 or po.x > ScreenDims + 1 or po.y < -10 or po.y > ScreenDims + 1:
            po.x = (po.x + ScreenDims) % ScreenDims
            po.y = (po.y + ScreenDims) % ScreenDims
        pygame.draw.circle(screen, (colours[po.colour]), (po.x, po.y), 1)
        po.x = po.x / ScreenDims
        po.y = po.y / ScreenDims



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    font = pygame.font.SysFont("arial", 32)
    text = font.render("Masterpiece Animation", True, (0,0,0))
    screen.blit(text, (4 // 2 - text.get_width() // 2, 20))
    pygame.display.flip()
pygame.quit()
