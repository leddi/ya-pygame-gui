import os
import pygame
import time
#from pygame.locals import *
import paho.mqtt.client as mqtt

os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

gotNewMessage = False
newMessage = ["topic/topic", "0.00"]

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


pygame.init()

DISPLAY = pygame.display.set_mode((0,0), flags=pygame.FULLSCREEN)
WIDTH=int(DISPLAY.get_width())
HEIGHT=int(DISPLAY.get_height())

DISPLAY.fill(RED)
pygame.draw.line(DISPLAY, WHITE, [1,1], [WIDTH, 1], 1)
pygame.draw.line(DISPLAY, WHITE, [WIDTH/2, 1], [WIDTH/2, HEIGHT], 5)

backimage = pygame.image.load("/home/pi/pygame/image.png")
backimage.convert_alpha()
backimage = pygame.transform.scale(backimage,(WIDTH, HEIGHT))

font = pygame.font.SysFont("verdana", 35, bold=1)
#textscreen = font.render("ALZ-HOF", 1, BLACK)

print("backgound")
#DISPLAY.blit(backimage, (0, 0), (0, 0, WIDTH, HEIGHT))

print("schift")
#DISPLAY.blit(textscreen, (20, 20))
#pygame.display.update()


for i in range(1, 100):
    textscreen = font.render(str(i), 1, BLACK)
#   DISPLAY.blit(backimage, (0, 0), (0, 0, WIDTH, HEIGHT))
    DISPLAY.fill(RED)
    DISPLAY.blit(textscreen, (20,20))
    pygame.display.update()
#    time.sleep(1)


while True:
    client.loop_start()
    if gotNewMessage:
        topic, message = newMessage
        message = message.decode('UTF-8')
        font = pygame.font.SysFont("quicksand", 85, bold=1)
        textscreen = font.render(str(message), 1, WHITE)
        DISPLAY.fill(BLACK)
        DISPLAY.blit(textscreen, (100, 100))
        pygame.display.update()
        gotNewMessage = False
    #client.loop_stop()

pygame.quit()
