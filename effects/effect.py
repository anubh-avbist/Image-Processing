import pygame
import math
import numpy
from abc import ABC, abstractmethod
class Effect(ABC):

    @staticmethod
    def get_val(pixel):
        val = (pixel[0]+pixel[1]+pixel[2])/3 # Returns pixel brightness
        return val 

    @staticmethod
    def create_image_matrix(image):
        cols = math.floor((image.get_height()))
        rows = math.floor((image.get_width()))
        image_matrix = numpy.empty((rows,cols))
        for j in range (0, cols):
            for i in range (0, rows):
                image_matrix[i][j] = image.get_at((i,j))
        return image_matrix

    @staticmethod
    def matrix_to_screen(matrix, screen):
        screen.fill((0,0,0))

        rows = matrix.shape[0]
        cols = matrix.shape[1]

        for j in range (1, cols):
            for i in range (1, rows):
                color:tuple[int,int,int] = matrix[i,j]
                screen.set_at((i,j), color)

    @staticmethod
    @abstractmethod
    def apply(image:pygame.Surface, *parameters) -> pygame.Surface:
        ...
