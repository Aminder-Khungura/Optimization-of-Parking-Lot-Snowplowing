# Use pygame for visualization, need to see:
# 1) The movement of snow plow
# 2) When plow is down and up
# 3) Use color gradient show where snow is being pilled up

import pygame
import pandas as pd


class ParkingLotBorders:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.boundary_coordinates = pd.read_csv(r'C:\Users\amind\PycharmProjects\Automated Parking Lot Snow Removal\boundary_coordinates.csv')
        self.parkingSpot_coordinates = pd.read_csv(r'C:\Users\amind\PycharmProjects\Automated Parking Lot Snow Removal\parkingSpot_coordinates.csv')
        self.entry_coordinates = pd.read_csv(r'C:\Users\amind\PycharmProjects\Automated Parking Lot Snow Removal\entry_coordinates.csv')

    def place_boundaries(self):
        blue = [0,   0, 255]
        for i in self.boundary_coordinates['0']:
            x = self.boundary_coordinates['0'][i]
            y = self.boundary_coordinates['1'][i]
            pygame.draw.circle(self.parent_screen, blue, [x, y], 1)

    def place_parkingspots(self):
        red = [255,   0,   0]
        for i in self.parkingSpot_coordinates['0']:
            x = self.parkingSpot_coordinates['0'][i]
            y = self.parkingSpot_coordinates['1'][i]
            pygame.draw.circle(self.parent_screen, red, [x, y], 1)

    def place_entries(self):
        green = [0, 255,   0]
        for i in self.entry_coordinates['0']:
            x = self.entry_coordinates['0'][i]
            y = self.entry_coordinates['1'][i]
            pygame.draw.circle(self.parent_screen, green, [x, y], 1)


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')

    def place_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow(self.screen)
        self.ParkingLotBorders = ParkingLotBorders(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Set snowplow character to display on user's click location
            try:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_coor, y_coor = pygame.mouse.get_pos()
                    x_coor -= 30
                    y_coor -= 30
                self.screen.blit(self.background_image, [0, 0])
                self.snowplow.place_snowplow(x_coor, y_coor)
            except NameError:  # Bypass NameError that occurs if mouse isn't clicked and variables x_coor/y-coor aren't created for snowplow() function
                pass
            self.ParkingLotBorders.place_boundaries()
            self.ParkingLotBorders.place_parkingspots()
            self.ParkingLotBorders.place_entries()
            pygame.display.flip()


if __name__ == '__main__':
    display = Display()
    display.run()
