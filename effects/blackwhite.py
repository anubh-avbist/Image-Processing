from effects.effect import Effect
import pygame, sys

class BlackWhite(Effect):
    description = "Makes image black and white based on a ratio."
    required_parameters = ["ratio"]
    
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:

        args = iter(parameters)
                
        try:
            ratio = max(0,min(float(next(args,0.5)),1))
        except ValueError:
            print("Please insert a number between 0 and 1 for num_colors")
            sys.exit()

        output = pygame.Surface(image.get_size())
        for j in range(image.get_height()):
            for i in range(image.get_width()):
                color = 255 if (Effect.get_val(image.get_at((i,j)))/255.0)>ratio else 0
                output.set_at((i,j), pygame.Color(color, color, color))
        return output