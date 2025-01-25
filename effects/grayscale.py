from effects.effect import Effect
import pygame, sys

class Grayscale(Effect):

    description = "Makes image grayscale."
    required_parameters = []
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        output = pygame.Surface(image.get_size())
        for j in range(image.get_height()):
            for i in range(image.get_width()):
                output.set_at((i,j), image.get_at((i,j)).grayscale())
        return output
    
    