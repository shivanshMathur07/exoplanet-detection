from re import X
import pygame
pygame.init()
import math

WIDTH , HEIGHT = 750,750    #in pixels
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")

#initialize the font
FONT = pygame.font.SysFont("comicsans",16)

#create planetary object class
class Planet():
    # creating the constants
    AU = 149.6e6 * 1000     #1 AU is approx distance of Earth and Sun
    G = 6.67428E-11
    SCALE = 200 / AU    # 1AU = 100 px
    TIMESTEP = 60*60*24     #TIMESTEP defines for how we want the simulation to show. It tell everytime the loop will update planet will move by 1 earth day
    # timestep se jab bhii loop update hgaa, simulation 1 din se aage ho jyega

    def __init__(self,name,x,y,radius,color,mass):
        # x,y are the position coordinates
        self.x = x
        self.y = y
        # radius of planet
        self.radius = radius
        # color of planet
        self.color = color
        # mass of planet in kg
        self.mass = mass

        self.name = name

        # now since planets move in around circular orbit we need the velocity(speed components)
        self.x_vel = 0
        self.y_vel = 0

        self.star = False   # to tell if the object is a star or regular planet.
        self.distance_to_star = 0

        self.orbit = []     #this wil be all the points our planet moves in the orbit.

    # this will draw the planet
    def draw(self,win):
        # since x & y will be a huge number we need to scale it down to fit in the window
        # in pygame 00 coordinate in the top-left, hence we need to offset it to draw objects in center of screen
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        # making the orbital path
        if len(self.orbit) > 2 :
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x,y))

            # drawing orbital path
            pygame.draw.lines(win, self.color,False,updated_points)

        if not self.star :
            distance_text = FONT.render(f"{self.name} {round(self.distance_to_star/100000000,1)}*10^5 km",1,self.color)
            win.blit(distance_text,(x,y))

        # this will draw and color the object
        pygame.draw.circle(win,self.color,(x,y),self.radius)

    # attraction between two objects
    def attraction(self,other):
        other_x,other_y = other.x,other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.star :
            self.distance_to_star = distance

        force = (self.G * self.mass * other.mass) / distance**2
        theta = math.atan2(distance_y , distance_x) 
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force

        return(force_x,force_y)

    def update(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx,fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # this is using the eq F=ma -> a = F/m.... timestep helps in updation
        # since the force component will give both negative and positive values hence this x_vel will help in maintaining the elliptical orbit.
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        #this will give the exact position of the planet in orbit
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # now will append it in orbit list.
        self.orbit.append((self.x, self.y))



def main():
    run = True
    clock = pygame.time.Clock()     #this is to regulate the frame-rate or else the game will on the speed of your processor.

    #creating planets & star
    sun = Planet(sun,0,0,50,(255,255,0),1.988 * 10**30)
    sun.star = True

    mercury = Planet(mercury,0.387*Planet.AU , 0 , 6,(156, 5, 5), 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(venus,0.723*Planet.AU , 0 , 8,(123, 183, 201), .868 * 10**23)
    venus.y_vel = -35.02 * 1000
    earth = Planet(earth,-1*Planet.AU , 0 , 15,(0,0,255), 5.974 * 10**24)
    earth.y_vel = 29.783 * 1000 #in m/s
    mars = Planet(mars,-1.524*Planet.AU , 0 , 12,(230, 72, 9), 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000


    planets = [sun,earth,mars,mercury,venus]

    
    while(run):
        clock.tick(60)  #this is the max framerate..ie the loop will at max run 60 times per second.
        WIN.fill((0,0,0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()