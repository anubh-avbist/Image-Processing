from effects.effect import Effect
import pygame, sys

class Aberrate(Effect):

    description = "Applies chromatic aberration effect."
    required_parameters = []
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        width = image.get_width()
        height = image.get_height()
        
        args = iter(parameters)
        
        size = int(next(args,1))
        
        
        output = pygame.Surface(image.get_size())
        for j in range(height):
            for i in range(width):
                r,g,b = 0,0,0
                if j > size:
                    r = image.get_at((i,j-size)).r
                
                if j < height-size:
                    if i > size:
                        b = image.get_at((i-size,j+size)).b
                    if i < width-size:
                        g = image.get_at((i+size, j+size)).g

                output.set_at((i,j), pygame.Color(r,g,b))

        return output