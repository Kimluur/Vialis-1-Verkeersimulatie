import pygame
from pygame.math import Vector2
import pandas as pd
import numpy as np
import math
import json
import pygame_textinput
from coordFunctions import *
from pygameExtras import *
"""
Main file with pygame simulation
"""

class bcolors:
    # Colours for pretty printing warnings etc.
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def loadcsvtoDf(filename):
    try:
        dftime = pd.read_csv(filename, delimiter=";", low_memory=False)
        print(bcolors.OKBLUE + "Loaded csv for ", filename, bcolors.HEADER)
        return dftime
    except:
        print(bcolors.FAIL + "Loading csv for ", filename, " failed" + bcolors.HEADER)
        return False


def loadJsontoDf(filename):
    """Load json data in df and normalize."""
    try:
        with open(filename) as file:
            data = json.load(file)

            df = pd.json_normalize(data, max_level=2)
            print("Loaded json for ", filename)
            return df
    except:
        print(bcolors.FAIL + "Loading json for ", filename, " failed" + bcolors.HEADER)
        return False


# pygame / window related settings
pygame.init()
resolution = (1376, 984)
win = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("AutoSim")
background = pygame.image.load('../bg.png')

myfont = pygame.font.SysFont('Ariel', 36, bold=True)
# Json/ data related imports
dfKruis1 = loadJsontoDf("../bos210.json")
dfKruis2 = loadJsontoDf("bos211.json")  # unused TODO: NEEDS TO BE ADDED LATER!
dfTime = loadcsvtoDf("../BOS210.csv")
dfStoplicht1 = loadJsontoDf("../b210_stoplicht.json")

# visualisatie settings:
lusSizeDefault = (8, 8)

# Create TextInput-object
textsurface = myfont.render('Afspeel tijd:', False, (0, 0, 0))

textinput = pygame_textinput.TextInput("08-01-2021 00:00:00", text_color=(0, 0, 0), max_string_length=20)


# mainloop
class Sensor(object):
    def __init__(self, locatie, kleur, breedte, lengte, name, locgeo=False):
        self.locatie = locatie
        self.kleur = kleur
        self.offKleur = kleur
        self.breedte = breedte
        self.lengte = lengte
        self.hitbox = (self.breedte, self.lengte)
        self.locgeo = locgeo
        self.name = name
        self.x = self.locatie[0]
        self.y = self.locatie[1]

    def draw(self, win, time):
        #instellingen voor lussen
        if dfTime[self.name].iloc[time] == "|":
            self.kleur = (255, 50, 50)
        else:
            self.kleur = self.offKleur
        #instellingen voor stoplichten
        if dfTime[self.name].iloc[time] == "#":
            self.kleur = (0,255,0)
        elif dfTime[self.name].iloc[time] == "Z":
            self.kleur = (245, 242, 51)
        #daadwerkelijke draw functies
        if not self.locgeo:
            self.hitbox = (self.x + self.breedte, self.lengte + self.y, self.breedte, self.lengte)
            pygame.draw.rect(win, self.kleur, self.hitbox, 2)
        else:
            pygame.draw.polygon(win, self.kleur, self.locatie)

class Car(pygame.sprite.Sprite):
    def __init__(self, position, waypoints, speed, color):
        super().__init__()
        self.image = pygame.Surface((12, 12)) # De auto (12x12 pixel rechthoek)
        self.image.fill(pygame.Color(color))
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




# define all objects:

# Alle Sensoren moeten hier toegevoegd worden die op het moment op het schermzijn:
# Dit gebeurd al automagisch
alleSensoren = []




def loadSensors(alleSensoren, dfkruis, dfstoplicht):
    """
    Een grote functie die alle type sensoren en stoplichten inlaad, en hierbij belangrijke informatie toevoegt.
    """
    for column in dfkruis[['name', 'sensorDeviceType', 'sensorPosition.lat', 'sensorPosition.long']]:
        if column == "name":
            name = dfkruis[column]
        elif column == "sensorPosition.long":
            long = dfkruis[column]
        elif column == "sensorPosition.lat":
            lat = dfkruis[column]

    for i in range(len(long)):
        a, b = latllongtocoord(lat[i], long[i])
        sid = name[i]
        # add alle sensoren uit de csv
        if dfkruis['sensorDeviceType'][i] == "inductionLoop":
            color = (252, 144, 30)
            # omdat onderstaande erg lange regels zijn hier uitleg:
            # ik pak elke hoek van de lus uit de json, vorm dit naar het correcte format,
            # en dan projecteer ik het naar de correcte x en y locatie.
            a = latllongtocoord(dfkruis['geoShape.indexPoint'][i][1]['lat'],
                                dfkruis['geoShape.indexPoint'][i][1]['long'])
            a = latlngToScreenXY(a[0], a[1])
            b = latllongtocoord(dfkruis['geoShape.indexPoint'][i][2]['lat'],
                                dfkruis['geoShape.indexPoint'][i][2]['long'])
            b = latlngToScreenXY(b[0], b[1])
            c = latllongtocoord(dfkruis['geoShape.indexPoint'][i][3]['lat'],
                                dfkruis['geoShape.indexPoint'][i][3]['long'])
            c = latlngToScreenXY(c[0], c[1])
            d = latllongtocoord(dfkruis['geoShape.indexPoint'][i][4]['lat'],
                                dfkruis['geoShape.indexPoint'][i][4]['long'])
            d = latlngToScreenXY(d[0], d[1])
            # hier maak ik de daadwerkelijke sensor aan, en plaats het gelijk in een lijst met alle sensoren.
            alleSensoren.append(Sensor([a, b, c, d], color, lusSizeDefault[0] + 2, lusSizeDefault[1] + 2, sid, True))
        else:
            color = (255, 0, 255)
            alleSensoren.append(
                Sensor((latlngToScreenXY(a, b)), color, lusSizeDefault[0], lusSizeDefault[1], sid, False))

    for i in dfstoplicht.values:
        print()
        kleur = (255, 0,0)

        xy = latlngToScreenXY(i[1], i[2])
        alleSensoren.append(Sensor([xy[0], xy[1]], kleur, 10, 3, i[0], False))
        print(dfstoplicht)


loadSensors(alleSensoren, dfKruis1, dfStoplicht1)




def toTime(timeString):
    """
    Gegeven een specifieke tijd string zoekt deze functie op welke tijd uit de csv het meest dichtbij is
    en returned deze tijd in de vorm van array numbers. Returned false en print een error message
    als de tijd niet in het correcte format is.
    """
    print(textinput.get_text())
    timedate = dfTime["time"]
    if len(timeString) > 18:
        if (timeString[13] == ":" and timeString[16] == ":"):
            for i in timedate:
                if timeString in i:
                    return timedate.index[timedate == i].tolist()
        else:
            print(bcolors.FAIL + "Input string wrongsyntax. Please check." + bcolors.HEADER)
            return False
    else:
        print(bcolors.FAIL + "Input string tooshort. Please check." + bcolors.HEADER)
        return False




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
    """
    DIT IS EEN VOORBEELDFUNCTIE
    Deze functie stippelt een route/pad uit tussen een begin en eind.
    De auto kan voor het stoplicht nog van baan wisselen.
    """
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
all_sprites = pygame.sprite.Group(Car((300, 100), create_path('11-1', '12-1'), 15, 'red'),
                              Car((300, 100), create_path('03-1', '03-1'), 15, 'yellow'),
                              Car((300, 100), create_path('05-1', '05-1'), 15, 'orange'),
                              Car((300, 100), create_path('41-1', '41-1'), 15, 'purple'),
                              Car((300, 100), create_path('04-1', '04-1'), 15, 'brown'),
                              Car((200, 500), create_path('11-1', '11-1'), 13,'green'))


def redrawGameWindow(time, currenttime):
    win.blit(background, (0, 0))
    for j in alleSensoren:
        j.draw(win, time)
    win.blit(createAlphaRect((300, 500), 125, (255, 255, 255)), (resolution[0] - 300, 20))
    win.blit(textsurface, (resolution[0] - 280, 55))
    win.blit(currenttime, (10, 10))
    win.blit(textinput.get_surface(), (resolution[0] - 275, 80))
    if textinput.update(events):
        if toTime(textinput.get_text()):
            time = toTime(textinput.get_text())[0]

    all_sprites.update()
    all_sprites.draw(win)

    for point in route_points:
        pygame.draw.rect(win, (90, 200, 40), (point, (4, 4)))
    # pygame.draw.rect(screen, (255, 0, 0), ([1277.3794196302945, 194.5669175480581], (5, 5)))
    pygame.display.flip()

    pygame.display.update()
    return time


time = 0
run = True
# main game loop, everything in here updates every frame.
while run:
    clock.tick(27)

    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    currenttime = myfont.render(dfTime["time"][time], False, (0, 0, 0))
    # Blit its surface onto the screen

    time = time + 1
    time = redrawGameWindow(time, currenttime)

pygame.quit()
