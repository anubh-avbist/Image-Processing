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
    def get_val(pixel:pygame.Color):
        val = (0.299*pixel[0]+0.587*pixel[1]+0.114*pixel[2]) # Returns pixel brightness
        return val 
    
    @staticmethod
    @abstractmethod
    def apply(image:pygame.Surface, *parameters) -> pygame.Surface:
        ...
