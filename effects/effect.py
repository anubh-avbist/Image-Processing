import pygame
import math
import numpy
from abc import ABC, abstractmethod

# The effect class is the base for building all image-processing effects.
class Effect(ABC):

    description = "Default description for effects/image processes."
    required_parameters = []
    optional_parameters = []
    @staticmethod
    def get_val(pixel):
        val = (0.299*pixel[0]+0.587*pixel[1]+0.114*pixel[2]) # Returns pixel brightness
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
