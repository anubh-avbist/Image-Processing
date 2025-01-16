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
                col = int(Effect.get_val(image.get_at((i,j))))
                output.set_at((i,j), pygame.Color(col,col,col))
        return output
    
    