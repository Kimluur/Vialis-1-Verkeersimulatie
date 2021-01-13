import pygame as pg
from pygame.math import Vector2
import math
import pandas as pd
import numpy as np
import json

all_sprites = []

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
    return [x + 1, (resolution[1] - y) - 3 ]


""""EINDE CODE MICK"""


class Car(pg.sprite.Sprite):
    def __init__(self, position, waypoints, speed, color):
        super().__init__()
        self.image = pg.Surface((12, 12)) # De auto (12x20 pixel rechthoek)
        self.image.fill(pg.Color(color))
        self.rect = self.image.get_rect(center=position)

        self.vel = Vector2(0, 0)
        self.max_speed = speed

        self.waypoints = waypoints
        self.waypoint_index = 0

        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 50
        self.end_target = self.waypoints[-1]
        self.position = Vector2(self.target[0]+5, self.target[1]+5) # Netter maken

    def update(self):

        if self.target != self.end_target:
            heading = self.target - self.position
            distance = heading.length()
            heading.normalize_ip()

            """Hieronder moeten snelheid/rem statements komen"""
            if distance <= 2:
                self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
                self.target = self.waypoints[self.waypoint_index]

            if distance <= self.target_radius:
                self.vel = heading * (distance / self.target_radius * self.max_speed)

            else:
                self.vel = heading * self.max_speed
            self.position += self.vel
            self.rect.center = self.position
        else:
            self.position = Vector2(self.waypoints[0][0], self.waypoints[0][1])
            self.waypoint_index = 1
            self.target = Vector2(self.waypoints[self.waypoint_index][0], self.waypoints[self.waypoint_index][1])

def main():

    def create_routes():
        """Deze functie haalt alle waypoints uit de JSON,
        alleen zodat we deze allemaal weer kunnen geven"""
        route_points = []
        divider = 10000000
        file_name = 'lanes.json'
        with open(file_name) as json_file:
            data = json.load(json_file)

        df = pd.json_normalize(data, 'genericLane')
        dfUseful = df[['laneID', 'name', 'nodes.nodeXY', 'connectsTo.connection.connectingLane.lane',
                       'connectsTo.connection.signalGroup', 'regional.addGrpC.nodes.nodeXY']]

        """Rechte rijbanen"""
        for node_data in dfUseful['nodes.nodeXY']:
            for node in node_data:
                route_points.append(latlngToScreenXY(int(node['node-LatLon']['lat']) / divider,
                                                     int(node['node-LatLon']['lon']) / divider))

        """Bochten"""
        for index, row in dfUseful.iterrows():
            if type(pd.notna(row['regional.addGrpC.nodes.nodeXY'])) == np.ndarray:
                for node_data in row['regional.addGrpC.nodes.nodeXY']:
                    route_points.append(latlngToScreenXY(int(node_data['node-LatLon']['lat']) / divider,
                                                         int(node_data['node-LatLon']['lon']) / divider))

        return route_points

    route_points = create_routes()

    def get_lanes_dict():
        """Deze functie maakt twee dictionaries, een voor de rijbanen en een voor de bochten
         Elke Rijbaan & bocht heeft een eigen nummer. Elke waypoint die bij een van die 2 hoort word
         netjes aan dat nummer gekoppelt zodat we deze snel kunnen vinden"""
        lanes = {}
        curves = {}
        divider = 10000000
        file_name = 'lanes.json'
        with open(file_name) as json_file:
            data = json.load(json_file)

        df = pd.json_normalize(data, 'genericLane')
        dfUseful = df[['laneID', 'name', 'nodes.nodeXY', 'connectsTo.connection.connectingLane.lane',
                       'connectsTo.connection.signalGroup', 'regional.addGrpC.nodes.nodeXY']]

        for index, row in dfUseful.iterrows():
            """Alle waypoints op de rechte rijbanen uitlezen & opslaan"""
            lane_waypoints = []
            for flat_node_data in reversed(row['nodes.nodeXY']):
                lane_waypoints.append((latlngToScreenXY(int(flat_node_data['node-LatLon']['lat']) / divider,
                                                        int(flat_node_data['node-LatLon']['lon']) / divider)))
            lanes[row['name']] = lane_waypoints

            """Alle waypoints in de bochten uitlezen & opslaan"""
            if type(pd.notna(row['regional.addGrpC.nodes.nodeXY'])) == np.ndarray:  # BETERE OPLOSSING VINDEN
                curve_waypoints = []
                for curve_node_data in row['regional.addGrpC.nodes.nodeXY']:
                    curve_waypoints.append(latlngToScreenXY(int(curve_node_data['node-LatLon']['lat']) / divider,
                                                            int(curve_node_data['node-LatLon']['lon']) / divider))
                curves[row['name']] = curve_waypoints
        return lanes, curves

    lanes, curves = get_lanes_dict()

    def create_path(start_lane, end_lane):
        """DIT IS EEN VOORBEELDFUNCTIE
        Deze functie stippelt een route/pad uit tussen een begin en eind.
        De auto kan voor het stoplicht nog van baan wisselen."""
        file_name = 'lanes.json'
        with open(file_name) as json_file:
            data = json.load(json_file)
        df = pd.json_normalize(data, 'genericLane')
        dfUseful = df[['laneID', 'name', 'nodes.nodeXY', 'connectsTo.connection.connectingLane.lane',
                       'connectsTo.connection.signalGroup', 'regional.addGrpC.nodes.nodeXY']]

        path = []

        path.extend(lanes[start_lane][:-1])
        path.extend(curves[end_lane])

        df_connected = dfUseful.loc[dfUseful['name'] == end_lane]
        if pd.notna(df_connected['connectsTo.connection.connectingLane.lane']).iloc[0]:
            connected_id = df_connected['connectsTo.connection.connectingLane.lane'].iloc[0]
            connected_name = dfUseful.loc[dfUseful['laneID'] == connected_id]['name'].iloc[0]
            path.extend(reversed(lanes[connected_name]))
        return path

    """AUTOS AANMAKEN"""
    all_sprites = pg.sprite.Group(Car((300, 100), create_path('11-1', '12-1'), 15, 'red'),
                                  Car((300, 100), create_path('03-1', '03-1'), 15, 'yellow'),
                                  Car((300, 100), create_path('05-1', '05-1'), 15, 'orange'),
                                  Car((200, 500), create_path('11-1', '11-1'), 13,'green'))

    screen = pg.display.set_mode(resolution)
    clock = pg.time.Clock()
    background = pg.image.load('bg.png')
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)

        for point in route_points:
            pg.draw.rect(screen, (90, 200, 40), (point, (4, 4)))
        # pg.draw.rect(screen, (255, 0, 0), ([1277.3794196302945, 194.5669175480581], (5, 5)))
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()