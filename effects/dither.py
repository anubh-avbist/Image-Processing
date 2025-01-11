from effects.effect import Effect
import pygame

class Dither(Effect):

    description = "Dither effect description."

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        height = image.get_height()
        width = image.get_width()

        palette = Effect.median_cut_palette(image, 8)
        for j in range(height):
            for i in range(width):
                old_pixel = image.get_at((i,j))
                new_pixel: pygame.Color = Effect.find_closest_palette_color(old_pixel, palette)
                image.set_at((i,j), new_pixel)
                quant_error = [old-new for old,new in zip([old_pixel.r, old_pixel.g, old_pixel.b], [new_pixel.r, new_pixel.g, new_pixel.b])]

                def adjust_error(pixel, error, scalar):
                    red = max(0,min(255,int(pixel.r + error[0]*scalar)))
                    green = max(0,min(255,int(pixel.g + error[1]*scalar)))
                    blue = max(0,min(255,int(pixel.b + error[2]*scalar)))
                    return pygame.Color(red,green,blue)
                
                if(i+1 < width):
                    image.set_at((i+1, j), adjust_error(image.get_at((i+1,j)), quant_error, 7/16))
                if(j+1 < height -1):
                    if i > 0:
                        image.set_at((i-1, j+1), adjust_error(image.get_at((i-1,j+1)), quant_error, 3/16))
                    image.set_at((i, j+1), adjust_error(image.get_at((i,j+1)), quant_error, 5/16))
                    if i + 1 < width:
                        image.set_at((i+1, j+1), adjust_error(image.get_at((i+1,j+1)), quant_error, 1/16))
        return image
    
    