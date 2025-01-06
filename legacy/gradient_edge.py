import pygame
import pygame.camera
import math
import numpy
import numpy.linalg

image = pygame.image.load("../images/Ramona500.png")
image = pygame.transform.scale(image,(800,800))
width = image.get_width()
height = image.get_height()


pixel_size = 2


pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

pygame.camera.init()
cam_list = pygame.camera.list_cameras()
cam = None
if cam_list:
    cam = pygame.camera.Camera(cam_list[0], (width, height))
    cam.start()
cam = None

image = pygame.transform.scale(image, (width,height))
screen.blit(image,(0,0))


horizontal_kernal = numpy.matrix('1,0,-1; 2,0,-2; 1,0,-1')
vertical_kernal = numpy.matrix('1,2,1; 0,0,0; -1,-2,-1')

test_matrix = numpy.matrix('0,50,50;0,0,50;0,0,60')

def get_val(pixel):
    val = (pixel[0]+pixel[1]+pixel[2])/3 # Returns pixel brightness
    return val 

def create_image_matrix(image):
    cols = math.floor((image.get_height())/pixel_size)
    rows = math.floor((image.get_width())/pixel_size)
    image_matrix = numpy.empty((rows,cols))
    for j in range (0, cols):
        for i in range (0, rows):
            pixel = image.get_at((i*pixel_size,j*pixel_size))
            image_matrix[i][j] = get_val(pixel)
    return image_matrix

def convolve(frame,kernal):
    value = 0
    for j in range (0,3):
        for i in range (0,3):
            value += frame[i,j]*kernal[i,j]
    value = value /4
    return min(255,max(0,value))


def find_edges(image_matrix, hor_kernal, vert_kernal): # assuming all kernals are 3x3
    rows = image_matrix.shape[0]-2
    cols = image_matrix.shape[1]-2
    edge_matrix = numpy.empty((rows,cols))
    for j in range (1, cols):
        for i in range (1, rows):
            frame = numpy.empty((3,3))
            for a in range (-1,2):
                for b in range (-1,2):
                    frame[a+1][b+1] = image_matrix[i+a][j+b]
            edge_matrix[i][j] = (convolve(frame,hor_kernal) + convolve(frame,vert_kernal))/2
    return edge_matrix


def matrix_to_screen(matrix):
    screen.fill((0,0,0))

    rows = matrix.shape[0]
    cols = matrix.shape[1]

    for j in range (1, cols):
        for i in range (1, rows):
            rect = pygame.Rect(i*pixel_size, j*pixel_size, pixel_size,pixel_size)
            color = matrix[i,j]
            color = max(0,min(255,color))
            pygame.draw.rect(screen,(color,color,color),rect)

def edge_image(image):
    image_matrix = create_image_matrix(image)
    edge_matrix = find_edges(image_matrix, horizontal_kernal, vertical_kernal)
    matrix_to_screen(edge_matrix)

edge_image(image)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            running = False
        if pressed[pygame.K_c]:
            pygame.image.save(screen, "../output/gradient.jpeg")


    if cam is not None: 
        image = cam.get_image()
        image = pygame.transform.scale(image, (width,height))

        edge_image(image)
        
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
