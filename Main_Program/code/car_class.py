from Main_Program.code import coord_functions
import pygame


class Car(pygame.sprite.Sprite):
    def __init__(self,  df, color):
        super().__init__()
        self.image = pygame.Surface((12, 12))  # De auto (12x12 pixel rechthoek)
        self.image.fill(pygame.Color(color))
        self.position = [-200, -200]  # Positie buiten het scherm
        self.rect = self.image.get_rect(center=self.position)  # Tekent het vierkantje
        self.df = df

    def update(self, timestamp):
        """De update functie wordt elke frame gerund. Hierin word de nieuwe positie van de auto berekend"""
        df_cor = self.df.loc[self.df['timestamp'] == timestamp][['latitude', 'longitude']]

        if len(df_cor) == 1:  # Doet geen update als er geen positie is voor de auto op deze tijd
            df_cor = df_cor.reset_index()
            self.position = coord_functions.latlngToScreenXY(df_cor['latitude'][0], df_cor['longitude'][0])
            self.rect.center = self.position
