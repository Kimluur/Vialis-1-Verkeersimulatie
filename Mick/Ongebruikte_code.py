"""Omdat we tijdens het project een aantal keer van 'richting' zijn veranderd hebben we uiteindelijk verschillende
functies niet gebruikt. Omdat hier toch veel tijd en moeite in hebben gestoken gooien we deze niet weg maar laten
we alsnog zien wat we gemaakt hebben. We leggen bij elke functie uit waarvoor deze diende en waarom we deze niet
meer hebben gebruikt"""

import pandas as pd
import json
import numpy as np


"""We hebben deze functie oorspronkelijk gemaakt om alle waypoint van elke rijstrook te verzamelen in 1 lijst.
Deze lijst konden we vervolgens plotten op de kaart waarmee we konden zien dat de test auto's van waypoint
naar waypoint rijden. Puur voor de ontwikkelingsfase dus."""
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

# route_points = create_routes()

"""Hoe we de waypoints plotte"""
for point in route_points:
        pygame.draw.rect(win, (90, 200, 40), (point, (4, 4)))
    pygame.draw.rect(screen, (255, 0, 0), ([1277.3794196302945, 194.5669175480581], (5, 5)))


"""We hebben deze functie (uitleg over functionaliteit hier onder) was erg nuttig omdat we makkelijk informatie
over de rijbanen en bochten konden opvragen. Omdat we uiteindelijk geen individuele auto's (behalve onze eigen)
plotten was dit niet meer nodig."""
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
                # print(type(int(curve_node_data['node-LatLon']['lat']) / divider), int(curve_node_data['node-LatLon']['lon']) / divider)
                curve_waypoints.append(latlngToScreenXY(int(curve_node_data['node-LatLon']['lat']) / divider,
                                                        int(curve_node_data['node-LatLon']['lon']) / divider))
            curves[row['name']] = curve_waypoints
    return lanes, curves

# lanes, curves = get_lanes_dict()


"""Deze functie was een eerste poging tot het maken van een route voor een individuele auto. Deze gaf je de rijbaan
waarop de auto begon en op welke rijbaan hij voor de stopstreep eindigde, hierop konden we baseren welke bocht 
de auto zou maken. Ook deze functie gebruiken we niet meer omdat we niet alle individuele auto's laten zien."""
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



"""Functie om een datetime string op juiste volgorde te zetten. Onnodig..."""
def clean(x):
    x = str(x)
    year = x[0:4]
    month = x[5:7]
    day = x[8:10]
    time = x[-8:]
    extraTime = '.0'
    new = f"{day}-{month}-{year} {time}{extraTime}"

    return new


"""Dit was de eerste versie van de Car klasse. Deze was gefocst op het kunnen plotten van meerdere auto's die hun
eigen weg af legde. Ook speelde snelheid hier nog een rol (bij de nieuwe functie staat de positie gekoppeld
aan de tijd) Met deze functie konden we dus meerdere auto's routes laten rijden. Dit hebben we uiteindelijk niet
meer nodig gehad, maar was wel de basis voor de nieuwe functie."""
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

    def update(self, tekst):
        # print(tekst)
        # print(self.position)

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

"""Hiermee werden de auto's aangemaakt"""
all_sprites = pygame.sprite.Group(Car((300, 100), waypoints, 15, 'red'),
                              Car((300, 100), create_path('03-1', '03-1'), 15, 'yellow'),
                              Car((300, 100), create_path('05-1', '05-1'), 15, 'orange'),
                              Car((300, 100), create_path('41-1', '41-1'), 15, 'purple'),
                              Car((300, 100), create_path('04-1', '04-1'), 15, 'brown'),
                              Car((200, 500), create_path('11-1', '11-1'), 13,'green'))