import random
import pygame
import pygame.camera
import math
import numpy
import numpy.linalg

image = pygame.image.load("images/CARKTEST.jpg")
if image.get_width() > 800:
    scale = 800 / image.get_width()
    image = pygame.transform.scale(image ,(image.get_width()*scale, image.get_height()*scale))
if image.get_height() > 900:
    scale = 900/image.get_height()
    image = pygame.transform.scale(image ,(image.get_width()*scale, image.get_height()*scale))
else:

    image = pygame.transform.scale(image,(800,800))
width = image.get_width()+10
height = image.get_height()+10


pixel_size = 1


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
    val = (0.299*pixel[0]+0.587*pixel[1]+0.114*pixel[2]) # Returns pixel brightness
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

def grayscale(image_matrix, bits = 1):
    rows = image_matrix.shape[0]-2
    cols = image_matrix.shape[1]-2
    grayed_image = numpy.empty((rows,cols))
    for j in range (1, cols):
        for i in range (1, rows):
            grayed_image[i][j] = math.floor(image_matrix[i][j]/(bits))*(bits)
    return grayed_image



def matrix_to_screen(matrix):
    screen.fill((0,0,0))

    rows = matrix.shape[0]
    cols = matrix.shape[1]

    for j in range (1, cols):
        for i in range (1, rows):
            rect = pygame.Rect(i*pixel_size, j*pixel_size, pixel_size,pixel_size)
            color = matrix[i,j]
            color = max(0,min(255,color))/255
            r = image.get_at((i*pixel_size, j*pixel_size))[0]
            g = image.get_at((i*pixel_size, j*pixel_size))[1]
            b = image.get_at((i*pixel_size, j*pixel_size))[2]
            finalColor = (int(r*color), int(g*color), int(b*color))

            pygame.draw.rect(screen, finalColor, rect)

def dither(image):
    
    cols = math.floor((image.get_height())/pixel_size)
    rows = math.floor((image.get_width())/pixel_size)
    
    gray_img = grayscale(create_image_matrix((image)), 64)
    dithered_image = numpy.empty((rows,cols))
    for j in range (1, cols-4):
        for i in range (1, rows-4):
            oldpixel = gray_img[i][j]
            newpixel = 0 if oldpixel/255 < 0.5 else 255
            dithered_image[i][j] = newpixel
            quant_error = oldpixel - newpixel
            gray_img[i+1][j] += quant_error*7/16
            gray_img[i-1][j+1] += quant_error*3/16
            gray_img[i][j+1] += quant_error*5/16
            gray_img[i+1][j+1] += quant_error*1/16
            # dithered_image[i][j] = min(i,j)
            # if get_val(image_matrix.get_at((i*pixel_size,j*pixel_size))) < 200:
            #     dithered_image[i][j] = 0
    return dithered_image




matrix_to_screen(dither(image))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            running = False
        if pressed[pygame.K_c]:
            pygame.image.save(screen, "images/dither.jpeg")


    if cam is not None: 
        image = cam.get_image()
        image = pygame.transform.scale(image, (width,height))
        matrix_to_screen(dither(image))
        
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
