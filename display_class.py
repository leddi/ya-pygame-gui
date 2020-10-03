import sys, os
import pygame
import pygame.event as GUI_EVENT
from pygame.locals import *
import time
import paho.mqtt.client as mqtt


if len(sys.argv) > 1:
    HP = True
else:
    HP = False

if not HP:
    os.environ["SDL_VIDEODRIVER"] = "fbcon"
    os.environ["SDL_FBDEV"] = "/dev/fb0"

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

gotNewMessage = True
newMessage = ["topic/topic", b'-.---']


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        pygame.mixer.quit()
        if not HP:
            screensize = (0,0)
            flags = FULLSCREEN
        else:
            screensize = (480,240)
            flags = RESIZABLE
        App.screen = pygame.display.set_mode(screensize, flags)
        App.t = Text('Pygame App', pos=(20, 20), fontname="sourcecode-regular.ttf")

        App.running = True

    
    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            App.screen.fill(Color('gray'))
            App.t.draw()
            pygame.display.update()
        pygame.quit()    

class Text:
    """Create a text object."""

    def __init__(self, text, pos, fontname, **options):
        self.text = text
        self.pos = pos
        self.fontname = fontname
        
        self.fontsize = 32
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)


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

client.loop_start()



if __name__ == '__main__':
    App().run()
