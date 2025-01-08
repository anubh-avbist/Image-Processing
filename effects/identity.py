from effects.effect import Effect
import pygame
import numpy

class Identity(Effect):
    
    description = "Returns the input image exactly."
    required_parameters = []
    optional_parameters = []
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        return image