import pygame
from pygame.locals import *
from random import randint

pygame.init()
bigfont = pygame.font.SysFont("", 100)
font = pygame.font.SysFont("", 50)


def textobjekt(text, color, pos, chosenfont=font):
    textflache = chosenfont.render(text, True, color)
    screen.blit(textflache, pos)


class Regler():
    def __init__(self, x, y, lange, text, wert, maxw):
        self.x = x
        self.y = y
        self.lange = lange
        self.rx = x + lange / 2
        self.aktiv = False
        self.text = text
        self.wert = wert
        self.maxwert = maxw * 1.1111111111111111111

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.lange, round(self.lange / 10)))
        pygame.draw.rect(screen, (200, 200, 200),
                         (self.rx, self.y - self.lange / 7 / 8, self.lange / 10, self.lange / 7))
        textgrund, textkasten = textobjekt(self.text + "   " + str(round(self.wert)), font)
        textkasten.center = ((self.x + (self.lange / 2)), self.y - self.lange / 10)
        screen.blit(textgrund, textkasten)

    def get_regler(self):
        self.rx = self.wert * (self.lange / self.maxwert) + self.x

    def get_wert(self):
        self.wert = (self.rx - self.x) * (self.maxwert / self.lange)


class Button():
    def __init__(self, tag, x, y, image, pressed):
        self.x = x
        self.y = y
        self.tag = tag
        self.image = image
        self.pressedimage = pressed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pressed = False
        self.cooldown = 50

    def gotpressed(self):
        screen.blit(self.image, (self.x, self.y))
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            if mouse[0] > self.x and mouse[0] < self.x + self.width:
                if mouse[1] > self.y and mouse[1] < self.y + self.height:
                    screen.blit(self.pressedimage, (self.x, self.y))
                    if click[0]:
                        self.cooldown = 30
                        return True

def open(chains):

    width = 1000
    size = width / len(chains[0])

    height = len(chains) * size * 1.5 - size / 2
    zoom = 1

    print(chains)
    print(len(chains), size)
    print(width, height)

    colors = {
        "R":(255, 0, 0),
        "B":(0, 0, 255),
        "G":(0, 150, 0),
        "Y":(255, 255, 0),
        "A":(100, 100, 255),
        "C":(0, 200, 200),
        "O":"orange",
        "W":(255, 255, 255),
        "L":(0, 255, 0),
        "P":(200, 0, 200),
    }

    screen = pygame.display.set_mode((int(width * zoom - (size - size / 1.1)), int(height * zoom)))
    pygame.display.set_caption("Grafische Darstellung")
    buttons = []

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    finish = True
                if event.key == pygame.K_SPACE:
                    finish = True
        for i in buttons:
            if i.gotpressed():
                pass

        yind = 0
        for row in chains:
            xind = 0
            for element in row:
                pygame.draw.rect(screen, colors[element], (xind * size, yind * size, size / 1.1, size / 1.1))
                xind += 1
            yind += 1.5

        pygame.display.update()
        pygame.display.flip()
        screen.fill("#19232d")

        if not running:
            break

    pygame.quit()