from effects.effect import Effect
import pygame
import numpy

class Sobel(Effect):

    description = "Highlights the edges in the image and returns a grayscale image."
    required_parameters = []
    optional_parameters = []

    @staticmethod
    def convolve(frame,kernal):
        value = 0
        for j in range (0,3):
            for i in range (0,3):
                value += frame[i,j]*kernal[i,j]
        return min(255,max(0,value))

    @staticmethod
    def find_edges(image: pygame.Surface, hor_kernal, vert_kernal) -> pygame.Surface: # assuming all kernals are 3x3
        rows = image.get_size()[0]-2
        cols = image.get_size()[1]-2
        edged_image = pygame.Surface(image.get_size())
        
        edged_image.fill((0,0,0))
        
        for j in range (1, cols):
            for i in range (1, rows):
                frame = numpy.empty((3,3))
                for a in range (-1,2):
                    for b in range (-1,2):
                        frame[a+1][b+1] = Effect.get_val(image.get_at((i+a,j+b)))
                value = (Sobel.convolve(frame,hor_kernal) + Sobel.convolve(frame,vert_kernal)) /2
                
                value = int(value)
                
                edged_image.set_at((i,j), pygame.Color(value,value,value))
        return edged_image
    
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        horizontal_kernal = numpy.matrix('1,0,-1; 2,0,-2; 1,0,-1')
        vertical_kernal = numpy.matrix('1,2,1; 0,0,0; -1,-2,-1')
        
        edge_image = Sobel.find_edges(image, horizontal_kernal, vertical_kernal)
        
        return edge_image