import pygame as pg
from pygame.math import Vector2
import math
import pandas as pd
import json

"""BEGIN CODE MICK"""
resolution = (1376, 984)
radius = 6371  # Earth Radius in KM


class referencePoint:
    def __init__(self, scrX, scrY, lat, lng):
        self.scrX = scrX
        self.scrY = scrY
        self.lat = lat
        self.lng = lng


# Calculate global X and Y for top-left reference point
p0 = referencePoint(0, 0, 51.68230193746829, 5.2926443213164776)
# Calculate global X and Y for bottom-right reference point
p1 = referencePoint(resolution[0], resolution[1], 51.68392685202088, 5.2963135830851416)


# This function converts lat and lng coordinates to GLOBAL X and Y positions
def latlngToGlobalXY(lat, lng):
    # Calculates x based on cos of average of the latitudes
    x = radius * lng * math.cos((p0.lat + p1.lat) / 2)
    # Calculates y based on latitude
    y = radius * lat
    return {'x': x, 'y': y}


# This function converts lat and lng coordinates to SCREEN X and Y positions
def latlngToScreenXY(lat, lng):
    # Calculate global X and Y for projection point
    pos = latlngToGlobalXY(lat, lng)
    p0.pos = latlngToGlobalXY(p0.lat, p0.lng)
    p1.pos = latlngToGlobalXY(p1.lat, p1.lng)
    # Calculate the percentage of Global X position in relation to total global width
    perX = ((pos['x'] - p0.pos['x']) / (p1.pos['x'] - p0.pos['x']))
    # Calculate the percentage of Global Y position in relation to total global height
    perY = ((pos['y'] - p0.pos['y']) / (p1.pos['y'] - p0.pos['y']))

    # Returns the screen position based on reference points
    x = p0.scrX + (p1.scrX - p0.scrX) * perX
    y = p0.scrY + (p1.scrY - p0.scrY) * perY
    return [x + 5, (resolution[1] - y) - 5 ]


""""EINDE CODE MICK"""

class Car(pg.sprite.Sprite):
    def __init__(self, position, waypoints):
        super().__init__()
        self.image = pg.Surface((12, 20)) # De auto (12x20 pixel rechthoek)
        self.image.fill(pg.Color('red'))
        self.rect = self.image.get_rect(center=position)

        self.vel = Vector2(0, 0)
        self.max_speed = 5
        self.position = Vector2(position)

        self.waypoints = waypoints
        self.waypoint_index = 0

        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 50

    def update(self):
        heading = self.target - self.position
        distance = heading.length()
        heading.normalize_ip()

        if distance <= 2:
            self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
            self.target = self.waypoints[self.waypoint_index]

        if distance <= self.target_radius:
            self.vel = heading * (distance / self.target_radius * self.max_speed)

        else:
            self.vel = heading * self.max_speed
        self.position += self.vel
        self.rect.center = self.position


def main():
    with open('bos210.json') as file:
        bos210 = json.load(file)
    df = pd.json_normalize(bos210, max_level=2)

    # data.iloc[::-1]
    df1 = df.loc[(df['name'].str[:2] == '12')]
    df1 = df1.iloc[::-1]

    df2 = df.loc[(df['name'].str[:2] == '01')]
    df2 = df2.iloc[::-1]

    divider = 10000000
    waypointscoor1 = []
    waypointscoor2 = []
    for index, row in df1.iterrows():
        waypointscoor1.append(latlngToScreenXY(int(row['sensorPosition.lat']) / divider, int(row['sensorPosition.long']) / divider))
    # print(waypointscoor1)
    for index, row in df2.iterrows():
        waypointscoor2.append(latlngToScreenXY(int(row['sensorPosition.lat']) / divider, int(row['sensorPosition.long']) / divider))
    # print(waypointscoor1)
    allway = waypointscoor1 + waypointscoor2
    print(allway)





    screen = pg.display.set_mode(resolution)
    clock = pg.time.Clock()
    background = pg.image.load('bg.png')

    all_sprites = pg.sprite.Group(Car((100, 300), waypointscoor1), Car((200, 500), waypointscoor2))

    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        screen.blit(background, (0, 0))


        all_sprites.update()
        # screen.fill((30, 30, 30))
        all_sprites.draw(screen)

        for point in allway:
            pg.draw.rect(screen, (90, 200, 40), (point, (4, 4)))
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()