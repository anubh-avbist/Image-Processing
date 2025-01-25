import pygame
import math
import numpy, itertools
from abc import ABC, abstractmethod
from functools import reduce

# The effect class is the base for building all image-processing effects.
class Effect(ABC):

    description = "Default description for effects/image processes."
    required_parameters = []
    optional_parameters = []

    @staticmethod
    def find_closest_palette_color(pixel, palette) -> pygame.Color:
        def get_closest(a:pygame.Color, b:pygame.Color):
            if Effect.euclidean_distance(a, pixel) < Effect.euclidean_distance(b, pixel):
                return a
            return b
        return reduce(get_closest, palette)



    @staticmethod 
    def euclidean_distance(a:pygame.Color, b:pygame.Color) -> float:
        return math.sqrt((b.r-a.r)**2 + (b.g-a.g)**2 + (b.b-a.b)**2)
    
    @staticmethod
    def median_cut_palette(image:pygame.Surface, num: int=8) -> list[pygame.Color]:

        width = image.get_width()
        height = image.get_height()
        pixels = [image.get_at(pos) for pos in itertools.product(range(width),range(height))]

        def bucket(pixels:list[pygame.Color], num:int) -> list[pygame.Color]:
            if num <= 1:
                rgb = [0,0,0]
                for pixel in pixels:
                    rgb[0] += pixel.r
                    rgb[1] += pixel.g
                    rgb[2] += pixel.b
                
                rgb = [int(channel/len(pixels)) for channel in rgb]
                return [pygame.Color(*rgb)]
            
            maxes = [-1,-1,-1]
            mins = [256,256,256]

            for pixel in pixels:
                maxes[0] = max(maxes[0], pixel.r)
                maxes[1] = max(maxes[1], pixel.g)
                maxes[2] = max(maxes[2], pixel.b)
                mins[0] = min(mins[0], pixel.r)
                mins[1] = min(mins[1], pixel.g)
                mins[2] = min(mins[2], pixel.b)
                                    
            ranges = [a-b for a,b in zip(maxes,mins)]
            index = ranges.index(max(ranges))
            pixels = sorted(pixels, key=lambda p:p[index])
            
            return bucket(pixels[:math.floor(len(pixels)/2)], int(num/2)) + bucket(pixels[math.floor(len(pixels)/2):], int(num/2)) 

        return bucket(pixels, num)       

    @staticmethod
    def get_val(pixel:pygame.Color):
        return pixel.grayscale().r # Returns pixel brightness
    
    @staticmethod
    @abstractmethod
    def apply(image:pygame.Surface, *parameters) -> pygame.Surface:
        ...
