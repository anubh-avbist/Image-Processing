import sys
from effects.effect import Effect
import pygame, numpy, math

class Scale(Effect):

    description = "Scales by to desired dimensions using bilinear interpolation. Alternatively, input only one number as scale factor."
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
                x = i*width/output_width
                y = j*height/output_height

                x1 = int(x)
                y1 = int(y)
                x2 = x1+1
                y2 = y1+1


                factor1 = numpy.array([x2-x, x-x1])

                factor2 = numpy.array([[y2-y], [y-y1]])
                if abs(x2-x) > 1 or abs(y2-y) > 1:
                    print("WHOAHFOIW")
                    sys.exit()
                
                q11 = (clamp(x1,0, width-1),clamp(y1,0,height-1))
                q12 = (clamp(x1,0, width-1),clamp(y2,0,height-1))
                q21 = (clamp(x2,0, width-1),clamp(y1,0,height-1))
                q22 = (clamp(x2,0, width-1),clamp(y2,0,height-1))
                cols = {}

                if abs(x2-x1) >= 2:
                    print(x2, x1)
                for attr in ["r", "g", "b"]:
                    matrix = numpy.array([
                        [getattr(image.get_at(q11), attr), getattr(image.get_at(q12), attr)],
                        [getattr(image.get_at(q21), attr), getattr(image.get_at(q22), attr)]
                    ])
                    cols[attr] = int(numpy.matmul(factor1, numpy.matmul(matrix, factor2)))
                
                try:
                    output.set_at((i,j), pygame.Color(cols["r"], cols["g"], cols["b"]))
                except:
                    print(factor1)
                    print(x, i)
                    print(cols)  
                    sys.exit()          

        return output
    
    