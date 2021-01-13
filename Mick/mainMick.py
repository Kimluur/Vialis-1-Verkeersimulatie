import pygame
import pandas as pd
import math
import json
import pygame_textinput

"""
Main file with pygame simulation
"""


# todo: Split in multiple .py files for readability.


# Functions and classes for setup / loading.
def aspect_scale(img, bx, by):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))


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
autoBreedte = 40
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


class Auto(object):
    def __init__(self, startLoc, eindLoc, lengteAuto, snelheid, kleur):
        self.breedte = autoBreedte
        self.lengte = lengteAuto
        self.startLoc = startLoc  # bijv:  (1,2) waar x = 1 en y = 2
        self.eindLoc = eindLoc  # bijv:  (1,2) waar x = 1 en y = 2
        self.snelheid = snelheid
        self.kleur = (255, 0, 0)  # rood temp standaard kleur
        self.hitbox = (self.breedte, self.lengte)
        self.x = startLoc[0]
        self.y = startLoc[1]

    def draw(self, win):
        self.hitbox = (self.x + self.breedte, self.lengte + self.y, self.breedte, self.lengte)
        pygame.draw.rect(win, self.kleur, self.hitbox, 2)


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
    return [x , (resolution[1] - y) ]


# define all objects:

# Alle autos --------
auto = Auto((43482 / 500, 30938 / 500), 100, 40, 3, "temp")
auto2 = Auto((45312 / 500, 31526 / 500), 100, 50, 10, "temp")
# Voor elke auto toevoegen aan deze lijst voor makkelijk tekenen
alleAutos = [auto, auto2]

print(latlngToScreenXY(51.6832962, 5.2938813))
# Alle Sensoren moeten hier toegevoegd worden die op het moment op het schermzijn:
# Dit gebeurd al automagisch
alleSensoren = []


def latllongtocoord(long, lat):
    """Small data miscommunication fix, 50000 to 5.0000 etc. so making it valid coordinates"""
    long = float(str(long)[:2] + '.' + str(long)[2:])
    lat = float(str(lat)[:1] + '.' + str(lat)[1:])

    return long, lat


def loadSensors(alleSensoren, dfkruis, dfstoplicht):
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


def createAlphaRect(size, alpha, colour):
    """Maakt een rectangle die ook transparant kan zijn, 
    de gewone draw van pygame kan dit niet.
    Vergeet deze niet te blitten naar het scherm!(comment voor example!)"""
    s = pygame.Surface(size)  # the size of your rect
    s.set_alpha(alpha)  # alpha level
    s.fill(colour)  # this fills the entire surface
    # after this use this is a blits:
    # windowSurface.blit(createalpharect(), (0, 0))  # (0,0) are the top-left coordinates
    return s


def toTime(timeString):
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


def toTimeArray(time):
    print(dfTime["time"][time])


def redrawGameWindow(time, currenttime):
    win.blit(background, (0, 0))
    for j in alleSensoren:
        j.draw(win, time)
    for i in alleAutos:
        i.draw(win)
    win.blit(createAlphaRect((300, 500), 125, (255, 255, 255)), (resolution[0] - 300, 20))
    win.blit(textsurface, (resolution[0] - 280, 55))
    win.blit(currenttime, (10, 10))
    win.blit(textinput.get_surface(), (resolution[0] - 275, 80))
    if textinput.update(events):
        if toTime(textinput.get_text()):
            time = toTime(textinput.get_text())[0]

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
