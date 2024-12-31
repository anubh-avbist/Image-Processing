from effects.effect import Effect
import pygame
import numpy

class Edge(Effect):

    @staticmethod
    def convolve(frame,kernal):
        value = 0
        for j in range (0,3):
            for i in range (0,3):
                value += frame[i,j]*kernal[i,j]
        value = value /4
        return min(255,max(0,value))

    @staticmethod
    def find_edges(image_matrix, hor_kernal, vert_kernal): # assuming all kernals are 3x3
        rows = image_matrix.shape[0]-2
        cols = image_matrix.shape[1]-2
        edge_matrix = numpy.empty(shape=(rows,cols), dtype=tuple)
        edge_matrix.fill((0,0,0))
        
        for j in range (1, cols):
            for i in range (1, rows):
                frame = numpy.empty((3,3))
                for a in range (-1,2):
                    for b in range (-1,2):
                        frame[a+1][b+1] = image_matrix[i+a][j+b]
                value = (Edge.convolve(frame,hor_kernal) + Edge.convolve(frame,vert_kernal))/2
                edge_matrix[i][j] = (value,value,value)
        return edge_matrix
    
    @staticmethod
    def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
        
        horizontal_kernal = numpy.matrix('1,0,-1; 2,0,-2; 1,0,-1')
        vertical_kernal = numpy.matrix('1,2,1; 0,0,0; -1,-2,-1')
        image_matrix = Effect.create_image_matrix(image)
        edge_matrix = Edge.find_edges(image_matrix, horizontal_kernal, vertical_kernal)
        Effect.matrix_to_screen(edge_matrix, image)
        return image