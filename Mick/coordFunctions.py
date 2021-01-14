import math
resolution = (1376, 984)
radius = 6371

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