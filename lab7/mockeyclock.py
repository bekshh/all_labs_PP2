import pygame
import math
from datetime import datetime
from sys import exit
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("mickeymouse clock")
clock = pygame.time.Clock()
mickey_surface = pygame.image.load('images_for_pygame/clock.png').convert_alpha()
mickey_rect = mickey_surface.get_rect(center=(800 // 2, 600 // 2))
min_hand = pygame.image.load('images_for_pygame/min_hand.png').convert_alpha()
sec_hand = pygame.image.load('images_for_pygame/sec_hand.png').convert_alpha()
test_font = pygame.font.Font(None,35)
text_surface = test_font.render("mickey clocks time",True,'black')
def rotate(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    time_now = datetime.now()
    seconds = int(time_now.strftime("%S"))
    minutes = int(time_now.strftime("%M"))
    seconds_angle = -math.radians(seconds*6)
    minutes_angle = -math.radians(minutes*6) 
    screen.blit(mickey_surface,(0,0))
    screen.blit(text_surface,(300,550))
    rotated_right_hand, right_hand_rect = rotate(min_hand, math.degrees(minutes_angle)-55, mickey_rect.center)
    rotated_left_hand, left_hand_rect = rotate(sec_hand, math.degrees(seconds_angle)+55, mickey_rect.center)
    screen.blit(rotated_left_hand, left_hand_rect)
    screen.blit(rotated_right_hand, right_hand_rect)
    pygame.display.update()
    clock.tick(1)


