from math import sqrt
from effects.effect import Effect
import pygame, math
from functools import reduce
import re, itertools
class Quantize(Effect):

    description = "Limits color pallete to a certain number of colors. Distance parameter specifies the minimum euclidean distance between colors in pallette."
    optional_parameters = []
    required_parameters = ["num_colors"]

    @staticmethod 
    def euclidean_distance(a:pygame.Color, b:pygame.Color) -> float:
        return sqrt((b.r-a.r)**2 + (b.g-a.g)**2 + (b.b-a.b)**2)
    
    @staticmethod
    def get_color_pallette(image:pygame.Surface, num: int=8) -> list[pygame.Color]:

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

                rgb = [int(rgb[0]/len(pixels)), int(rgb[1]/len(pixels)), int(rgb[2]/len(pixels))] 
                #print(len(pixels))
                return [pygame.Color(*rgb)]
            
            maxes = [-1,-1,-1]
            mins = [256,256,256]

            for pixel in pixels:
                maxes[0] = max(maxes[0], pixel.r)
                maxes[1] = max(maxes[1], pixel.g)
                maxes[2] = max(maxes[2], pixel.b)
                maxes[0] = min(mins[0], pixel.r)
                mins[1] = min(mins[1], pixel.g)
                mins[2] = min(mins[2], pixel.b)
                                    
            ranges = [a-b for a,b in zip(maxes,mins)]
            index = ranges.index(max(ranges))
            pixels = sorted(pixels, key=lambda x:x[index])
            
            return bucket(pixels[:math.floor(len(pixels)/2)], int(num/2)) + bucket(pixels[math.floor(len(pixels)/2):], int(num/2)) 

        return bucket(pixels, num)       

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:

        width = image.get_width()
        height = image.get_height()

        args = iter(parameters)
        num_colors = int(next(args,8))
        pallette = Quantize.get_color_pallette(image, num_colors)
        
        for j in range(height):
            for i in range(width):
                def get_closest(a:pygame.Color, b:pygame.Color):
                    if Quantize.euclidean_distance(a, image.get_at((i,j))) <Quantize.euclidean_distance(b, image.get_at((i,j))):
                        return a
                    return b
                color = reduce(get_closest, pallette)
                image.set_at((i,j), color)
        print(f"Color pallete used: \n {pallette}")
        return image
    
    