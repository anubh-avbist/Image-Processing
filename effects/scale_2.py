import sys
from effects.effect import Effect
import pygame, numpy, math

class Scale2(Effect):

    description = "Scales by to desired dimensions by matching to nearest pixel. Alternatively, input only one number as scale factor."
    required_parameters = ["output_width", "output_height"]

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        width = image.get_width()
        height = image.get_height()
        
        args = iter(parameters)
        
        output_width = float(next(args,width))
        output_height = int(next(args,-1))
        if output_height == -1:
            output_height = int(height * output_width)
            output_width = int(width * output_width)
        output_width = int(output_width)
        
        
        def clamp(n, minn, maxn) -> int:
            return max(min(maxn, n), minn)
        
        
        output = pygame.Surface((output_width, output_height))
        output.fill(pygame.Color(0,0,0))

        for j in range(output_height):
            for i in range(output_width):
                
                x = int(i*width/output_width)
                y = int(j*height/output_height)

                col = image.get_at((x,y))

                try:
                    output.set_at((i,j), pygame.Color(col))
                except:
                    print(col)  
                    sys.exit()          

        return output
    
    