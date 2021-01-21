import pygame
from pygame.math import Vector2
import pandas as pd
import numpy as np
import math
import json
from Main_Program.code import pygame_textinput
from Main_Program.code import pygame_extras
from Main_Program.code import get_car_dataframe #import main_dataframe
from Main_Program.code import car_class
from Main_Program.code.coord_functions import latllongtocoord,latlngToScreenXY
from Main_Program.code.get_car_dataframe import main_dataframe
from Main_Program.code.pygame_extras import createAlphaRect

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


def loadcsvtoDf(filename,delimiter = ";"):
    # try:
        dftime = pd.read_csv(filename, delimiter=delimiter, low_memory=False)
        print(bcolors.OKBLUE + "Loaded csv for ", filename, bcolors.HEADER)
        return dftime
    # except:
    #     print(bcolors.FAIL + "Loading csv for ", filename, " failed" + bcolors.HEADER)
    #     return False


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
background = pygame.image.load('data/bg.png')

myfont = pygame.font.SysFont('Ariel', 36, bold=True)
# Json/ data related imports_
dfKruis1 = loadJsontoDf("data/bos210.json")
dfTime = loadcsvtoDf("../BOS210_20210108_20210112.csv")
dfStoplicht1 = loadJsontoDf("data/b210_stoplicht.json")
dfWachtrij = loadcsvtoDf("../Wachtrij.csv",",")
# visualisatie settings:
lusSizeDefault = (8, 8)

# Create TextInput-object
textsurface = myfont.render('Afspeel tijd:', False, (0, 0, 0))

textinput = pygame_textinput.TextInput("10-01-2021 15:15:50", text_color=(0, 0, 0), max_string_length=20)


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
            self.kleur = (49, 2, 179)
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

def get_color(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return g, b, 0

class HeatLane(object):
    def __init__(self, locatie, kleur, name):
        self.locatie = locatie
        self.kleur = kleur
        self.offKleur = kleur
        self.name = name

    def draw(self, win, time):
        #instellingen voor lussen
        if self.name in dfWachtrij.columns :
            percent = 255 / 100
            number = int(dfWachtrij[self.name].iloc[time])

            self.kleur = (get_color(0,10,number))

            pygame.draw.polygon(win, self.kleur, self.locatie)
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
            color = (3, 215, 252)
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

def findGroup(number,lanes):
    group = (str(number.name[0])+str(number.name[1]))
    if group in lanes:
        if number in lanes[group]:
            pass
        else:
            lanes[group].append(number)
    else:
        lanes[group] = [number]

def mapLane(lanes, heatLanes):
    print(lanes)
    for i in lanes:
        print("alles in: ",i,"\n")
        count = 0
        for j in lanes[i]:

            print(j)
            if j.locgeo and count < 2:
                if count == 0:
                    firstSensor = j
                elif count == 1:
                    lastSensor = j
                else:
                    break
                count += 1

                if count == 2:
                    locA = firstSensor.locatie[0]
                    locB = firstSensor.locatie[1]
                    locC = lastSensor.locatie[0]
                    locD = lastSensor.locatie[2]
                    coords = [(locA),(locB),(locC),(locD)]
                    heatLanes.append(HeatLane(coords,(255, 204, 204),i))


def createHeat(alleSensoren,heatlanes):
    lanes = {}
    for i in alleSensoren:
        findGroup(i,lanes)
    mapLane(lanes,heatlanes)

heatlanes = []
createHeat(alleSensoren,heatlanes)
dfWachtrij.set_index("time")
print(heatlanes)

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


def redrawGameWindow(time, currenttime):
    win.blit(background, (0, 0))
    for j in alleSensoren:
        j.draw(win, time)
    for y in heatlanes:
        y.draw(win, time)
    win.blit(createAlphaRect((300, 500), 125, (255, 255, 255)), (resolution[0] - 300, 20))
    win.blit(textsurface, (resolution[0] - 280, 55))
    win.blit(currenttime, (10, 10))
    win.blit(textinput.get_surface(), (resolution[0] - 275, 80))
    if textinput.update(events):
        if toTime(textinput.get_text()):
            time = toTime(textinput.get_text())[0]

    timestamp = dfTime["time"][time]
    all_sprites.update(timestamp)
    all_sprites.draw(win)

    pygame.display.flip()

    pygame.display.update()

    return time

dataframe = main_dataframe()
all_sprites = pygame.sprite.Group(car_class.Car(dataframe, "black"))


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
