import pygame
import cv2 as cv
import numpy as np
import HARD_CODED_VALUES as HCV


class Barriers:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        # Convert windowSurface to cv2 Reference: https://stackoverflow.com/questions/19240422/display-cv2-videocapture-image-inside-pygame-surface
        self.view = pygame.surfarray.array3d(self.parent_screen)

        # Convert from (width, height, channel) to (height, width, channel)
        self.view = self.view.transpose([1, 0, 2])
        self.img_hsv = cv.cvtColor(self.view, cv.COLOR_BGR2HSV)

        # Define color ranges for masks
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])
        lower_blue = np.array([0, 100, 100])
        upper_blue = np.array([10, 255, 255])
        lower_red = np.array([110, 100, 100])
        upper_red = np.array([130, 255, 255])

        # create masks for boundary, parking spots, and entry
        self.boundary_mask = cv.inRange(self.img_hsv, lower_blue, upper_blue)
        self.parkingspot_mask = cv.inRange(self.img_hsv, lower_red, upper_red)
        self.entry_mask = cv.inRange(self.img_hsv, lower_green, upper_green)

        # Use mask to extract the area of interest
        self.boundary_result = cv.bitwise_and(self.img_hsv, self.img_hsv, mask=self.boundary_mask)
        self.parkingspot_result = cv.bitwise_and(self.img_hsv, self.img_hsv, mask=self.parkingspot_mask)
        self.entry_result = cv.bitwise_and(self.img_hsv, self.img_hsv, mask=self.entry_mask)

        # Clean image to decrease number of coordinates extracted later on
        kernel_erode = np.ones((2, 2), np.uint8)
        kernel_close = np.ones((15, 15), np.uint8)
        self.boundary_erode = cv.erode(self.boundary_result, np.ones((1, 1), np.uint8))
        self.boundary_closing = cv.morphologyEx(self.boundary_erode, cv.MORPH_CLOSE, kernel_close)
        self.parkingspot_erode = cv.erode(self.parkingspot_result, kernel_erode)
        self. parkingspot_closing = cv.morphologyEx(self.parkingspot_erode, cv.MORPH_CLOSE, kernel_close)
        self.entry_erode = cv.erode(self.entry_result, kernel_erode)
        self.entry_closing = cv.morphologyEx(self.entry_erode, cv.MORPH_CLOSE, kernel_close)

        # Extract pixel coordinates of boundaries, parking spots, and entries
        self.y_boundary, self.x_boundary = np.where(np.all(self.boundary_closing != HCV.BLACK, axis=2))
        self.y_parkingspot, self.x_parkingspot = np.where(np.all(self.parkingspot_closing != HCV.BLACK, axis=2))
        self.y_entry, self.x_entry = np.where(np.all(self.entry_closing != HCV.BLACK, axis=2))

        # Check if pixel locations are correct
        # for i in range(len(self.y_boundary)):
        #     pygame.draw.circle(self.parent_screen, [255, 255, 255], (self.x_boundary[i], self.y_boundary[i]), 1)
        # for i in range(len(self.y_parkingspot)):
        #     pygame.draw.circle(self.parent_screen, [255, 255, 255], (self.x_parkingspot[i], self.y_parkingspot[i]), 1)
        # for i in range(len(self.y_entry)):
        #     pygame.draw.circle(self.parent_screen, [255, 255, 255], (self.x_entry[i], self.y_entry[i]), 1)

        # Convert pixel coordinates to grid coordinates
        self.grid_boundary_coors = []
        self.grid_parkingspot_coors = []
        self.grid_entry_coors = []
        for i in range(len(self.y_boundary)):
            x = str(self.x_boundary[i] // HCV.BLOCK_WIDTH)
            y = str(self.y_boundary[i] // HCV.BLOCK_WIDTH)
            coor = x + ' ' + y
            self.grid_boundary_coors.append(coor)
        for i in range(len(self.y_parkingspot)):
            x = str(self.x_parkingspot[i] // HCV.BLOCK_WIDTH)
            y = str(self.y_parkingspot[i] // HCV.BLOCK_WIDTH)
            coor = x + ' ' + y
            self.grid_parkingspot_coors.append(coor)
        for i in range(len(self.y_entry)):
            x = str(self.x_entry[i] // HCV.BLOCK_WIDTH)
            y = str(self.y_entry[i] // HCV.BLOCK_WIDTH)
            coor = x + ' ' + y
            self.grid_entry_coors.append(coor)

        self.grid_boundary_coors = list(dict.fromkeys(self.grid_boundary_coors))
        self.grid_parkingspot_coors = list(dict.fromkeys(self.grid_parkingspot_coors))
        self.grid_entry_coors = list(dict.fromkeys(self.grid_entry_coors))

