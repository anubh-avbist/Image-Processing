from effects.effect import Effect
import pygame
import numpy

class Identity(Effect):
    
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        return image