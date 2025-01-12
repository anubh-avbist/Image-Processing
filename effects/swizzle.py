from effects.effect import Effect
import pygame, sys

class Swizzle(Effect):

    description = "Applies a swizzle on the rgb color channels."
    required_parameters = ["channels"]
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        width = image.get_width()
        height = image.get_height()
        args = iter(parameters)
        
        input = str(next(args,"rgb")).lower()

        if len(input) != 3:
            print("Please input a 3-character string, ie \'bbr\' or \'grb\'")
            sys.exit()
        for char in input:
            if char != 'r' and char != 'g' and char != 'b':
                print("Please only include the characters r, g, and b")
                sys.exit()

        for j in range(height):
            for i in range(width):
                old_pixel = image.get_at((i,j))
                new_pixel = pygame.Color(getattr(old_pixel, input[0]), getattr(old_pixel, input[1]), getattr(old_pixel, input[2]))
                image.set_at((i,j), new_pixel)


        return image