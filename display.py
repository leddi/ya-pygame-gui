import sys, os
import pygame
import pygame.event as GUI_EVENT
from pygame.locals import *
import time
import paho.mqtt.client as mqtt

os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

gotNewMessage = True
newMessage = ["topic/topic", b'-.---']

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("spritpreise/alz/diesel")
    client.subscribe("counter/down")

def on_message(client, userdata, msg):
    global gotNewMessage
    gotNewMessage = True
    global newMessage
    newMessage = [msg.topic, msg.payload]
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("vsrv.ledderboge.net", 1883, 60)


def quitgui():
    pygame.quit()
    sys.exit()


pygame.init()
pygame.mouse.set_visible(False)

DISPLAY = pygame.display.set_mode((0,0), flags=pygame.FULLSCREEN)
WIDTH=int(DISPLAY.get_width())
HEIGHT=int(DISPLAY.get_height())

DISPLAY.fill(RED)
pygame.draw.line(DISPLAY, WHITE, [1,1], [WIDTH, 1], 1)
pygame.draw.line(DISPLAY, WHITE, [WIDTH/2, 1], [WIDTH/2, HEIGHT], 5)

backimage = pygame.image.load("/home/pi/pygame/image.png")
backimage.convert_alpha()
backimage = pygame.transform.scale(backimage,(WIDTH, HEIGHT))

font = pygame.font.SysFont("quicksand", 45, bold=1)
#textscreen = font.render("ALZ-HOF", 1, BLACK)

# display backgound image
#DISPLAY.blit(backimage, (0, 0), (0, 0, WIDTH, HEIGHT))


while True:
    client.loop_start()
    for event in GUI_EVENT.get():
        if event.type == MOUSEBUTTONDOWN:
            print("Mousebutton: " + str(event.button))
            print("MouseXY: " + str(event.pos))
            quitgui()
    if gotNewMessage:
        topic, message = newMessage
        message = message.decode('UTF-8')
        textscreen = font.render(str(message), 1, WHITE)
        DISPLAY.fill(BLACK)
        DISPLAY.blit(textscreen, (10, 10))
        pygame.display.update()
        gotNewMessage = False

pygame.quit()
