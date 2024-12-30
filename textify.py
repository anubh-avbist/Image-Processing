import pygame
import pygame.camera
import math


pixel_size = 6
font_size = 6


image = pygame.image.load("images/Ramona.png")
image = pygame.transform.scale(image,(800,800))
width = image.get_width()
height = image.get_height()
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
    

grayscale = "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1\{\}[]?-_+~<>i!lI;:,."
#grayscale = "=======--------:::::::::........  "
#grayscale = "僵亁丵丣乑丱不丫丄一"
text_font = pygame.font.SysFont('Arial',font_size)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, (0,0,0))
    screen.blit(img, (x, y))

def pixel_to_char(pixel):
    val = get_val(pixel)
    ratio = val/255
    index = grayscale.__len__()*(ratio*ratio*ratio*ratio) 

    # Clamps index to scale length
    if index >= grayscale.__len__():
        index = grayscale.__len__()-1
    elif index <0:
        index = 0
    return grayscale[int(index)]


def get_val(pixel):
    val = (pixel[0]+pixel[1]+pixel[2])/3 # Returns pixel brightness
    return val 


def textify_img(image):
    image = pygame.transform.scale(image, (width,height))
    screen.blit(image, (0,0))

    # Creates text map
    ascii_array = []
    color_array = []
    for j in range (0, int(height/pixel_size)):
        ascii_array.append([])
        color_array.append([])
        for i in range (0,int(width/pixel_size)):
            pixel = screen.get_at((pixel_size*(i), pixel_size*(j)))
            ascii_array[j].append(pixel_to_char(pixel))
            color_array[j].append([pixel[0],pixel[1],pixel[2]])
    
    screen.fill((255,255,255))

    # Blits text onto screen
    for j in range (0, int(height/pixel_size)):
        for i in range (0,int(width/pixel_size)):
            pixel = screen.get_at((pixel_size*i,pixel_size*j))
            col = color_array[j][i]
            draw_text(ascii_array[j][i],text_font, col, i*pixel_size, j*pixel_size)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            running = False
        if pressed[pygame.K_c]:
            pygame.image.save(screen, "images/textified.jpeg")

    if cam is not None: 
        image = cam.get_image()
        image = pygame.transform.scale(image, (width,height))
        textify_img(image)
    else:
        textify_img(pygame.image.load("images/Ramona.png"))
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
