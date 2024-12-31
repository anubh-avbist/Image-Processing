from effects.effect import Effect
import pygame

class Textify(Effect):

    @staticmethod
    def draw_text(screen, text, font, color, x, y):
        img = font.render(text, True, (0,0,0))
        screen.blit(img, (x, y))

    @staticmethod
    def pixel_to_char(pixel):
        grayscale = "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{[]?-_+~<>i!lI;:,."

        val = Effect.get_val(pixel)
        ratio = val/255
        index = len(grayscale)*(ratio*ratio) 

        # Clamps index to scale length
        if index >= grayscale.__len__():
            index = grayscale.__len__()-1
        elif index <0:
            index = 0
        return grayscale[int(index)]

    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:

        width = image.get_width()
        height = image.get_height()
        
        

        args = iter(parameters)
        font_family = next(args,'monospace')
        font_size = int(next(args,12))
        pixel_size:int = int(next(args,12))
        pygame.font.init()
        text_font = pygame.font.SysFont(font_family,font_size)

        # font = parameters[0]
        # font_size = parameters[1]
        # Creates text map
        ascii_array = []
        color_array = []
        for j in range (0, int(height/pixel_size)):
            ascii_array.append([])
            color_array.append([])
            for i in range (0,int(width/pixel_size)):
                pixel = image.get_at((pixel_size*(i), pixel_size*(j)))
                ascii_array[j].append(Textify.pixel_to_char(pixel))
                color_array[j].append([pixel[0],pixel[1],pixel[2]])
        
        # Blits text onto screen
        screen = pygame.display.set_mode((width, height))
        screen.fill((255,255,255))
        for j in range (0, int(height/pixel_size)):
            for i in range (0,int(width/pixel_size)):
                pixel = image.get_at((pixel_size*i,pixel_size*j))
                col = color_array[j][i]
                Textify.draw_text(screen, ascii_array[j][i],text_font, col, i*pixel_size, j*pixel_size)
        return screen
    
    