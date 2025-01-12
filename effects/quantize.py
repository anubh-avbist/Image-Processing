from math import sqrt
from effects.effect import Effect
import pygame, math
from functools import reduce
import re, itertools
import sys
class Quantize(Effect):

    description = "Limits color pallete to a certain number of colors."
    optional_parameters = ["num_colors"]
    required_parameters = []

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:

        width = image.get_width()
        height = image.get_height()

        args = iter(parameters)
        
        try:
            num_colors = int(next(args,8))
        except Exception as e:
            print("Please insert an integer for num_colors")
            sys.exit()
        palette = Effect.median_cut_palette(image, num_colors)
        
        for j in range(height):
            for i in range(width):
                def get_closest(a:pygame.Color, b:pygame.Color):
                    if Quantize.euclidean_distance(a, image.get_at((i,j))) <Quantize.euclidean_distance(b, image.get_at((i,j))):
                        return a
                    return b
                color = reduce(get_closest, palette)
                image.set_at((i,j), color)
        print(f"Color pallete used: \n {palette}")
        return image
    
    