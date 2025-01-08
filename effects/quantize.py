from math import sqrt
from effects.effect import Effect
import pygame, math
from functools import reduce
import re
class Quantize(Effect):

    description = "Limits color pallete to a certain number of colors. Distance parameter specifies the minimum euclidean distance between colors in palette."
    optional_parameters = ["distance"]
    required_parameters = ["num_colors"]

    @staticmethod 
    def euclidean_distance(a:pygame.Color, b:pygame.Color) -> float:
        return sqrt((b.r-a.r)**2 + (b.g-a.g)**2 + (b.b-a.b)**2)
    @staticmethod
    def get_color_palette(image:pygame.Surface, num: int=8, distance:float=10) -> list[pygame.Color]:
        output = []
        histogram = {}
        width = image.get_width()
        height = image.get_height()

        for j in range(height):
            for i in range(width):
                color = image.get_at((i,j))
                key = f"r{color.r}g{color.g}b{color.b}"
                if key in histogram.keys():
                    histogram[key]+=1
                else:
                    histogram[key] = 1
    
        ordered_histogram = []
        for key in histogram:
            ordered_histogram.append((key,histogram[key]))
        ordered_histogram = sorted(ordered_histogram, key=lambda count:count[1])
        def string_to_rgb(s):
            return pygame.Color(*list((map(lambda x: int(x), filter(lambda x:len(x)>0,re.split('r|g|b', s))))))

        colors = list(map(lambda x:string_to_rgb(x[0]), ordered_histogram))
        
        if len(colors) < num:
            return colors
        else:
            for color in colors:
                using = True
                for used in output:
                    if Quantize.euclidean_distance(color,used) < distance:
                        using = False
                    
                if using == True:
                    output.append(color)
                    
        return output[0:num]

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:

        width = image.get_width()
        height = image.get_height()

        args = iter(parameters)
        num_colors = int(next(args,8))
        distance = float(next(args, 150))
        palette = Quantize.get_color_palette(image, num_colors, distance)
        
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
    
    