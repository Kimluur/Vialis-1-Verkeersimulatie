from coordFunctions import *
import pygame

class NewCar(pygame.sprite.Sprite):
    def __init__(self, position,  df, color):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((12, 12))  # De auto (12x12 pixel rechthoek)
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(center=position)
        self.df = df

    def update(self, timestamp):

        df_cor = self.df.loc[self.df['timestamp'] == timestamp][['latitude','longitude']]
        # self.position[0] += 10

        if len(df_cor) == 1:
            df_cor = df_cor.reset_index()
            self.position = latlngToScreenXY(df_cor['latitude'][0], df_cor['longitude'][0])
            # print(timestamp)
            # print(self.position)
            self.rect.center = self.position
        else:
            pass