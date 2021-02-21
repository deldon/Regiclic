from lxml import etree
from array import *
from gpiozero import Button
from signal import pause

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from gpiozero import LED


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()





fichier = "loop/data.xml"
arbre = etree.parse(fichier)
racine = arbre.getroot()
a = 0
arr = []



for noeud in arbre.xpath('//Tops'):
    for plat in noeud.iter('Top'):
        arr.append([])
        arr[a].append(plat.xpath("num")[0].text)
        arr[a].append(plat.xpath("Media")[0].text)
        arr[a].append(plat.xpath("Direct")[0].text)
        #print(plat.xpath("num")[0].text)
        arr[a].append(plat.xpath("Lum1")[0].text)
        arr[a].append(plat.xpath("Lum2")[0].text)
        #print("Metier : {}".format(plat.xpath("metier")[0].text))
        #print(a)
        a += 1



count = -1
a -= 1

def OnOff(num):
    global count
    if arr[count][num] == 'on':
        arr[count][num] = "off"
        pass

    elif arr[count][num] == 'off':
        arr[count][num] = "on"
        pass
    pass


def say_up():
    global count
    global a
    if count < a:
        count += 1
        Affi()
    else:
        print("ajouter")
        pass


def say_down():
    global count
    if count > 0:
        count -= 1
        Affi()
        pass

def say_Lum1():
    global count
    OnOff(3)
    Affi()
    pass

def say_Lum2():
    global count
    OnOff(4)
    Affi()
    pass

def say_Rec():
    print("rec")
    disp.clear()
    disp.display()
    pass

buttonUp = Button(16)
buttonDown = Button(20)
buttonLum1 = Button(21)
buttonLum2 = Button(26)
Lum1_led = LED(19)
Lum2_led = LED(4)

buttonUp.when_pressed = say_up
buttonDown.when_pressed = say_down
#buttonRec.when_pressed = say_Rec
buttonLum1.when_pressed = say_Lum1
buttonLum2.when_pressed = say_Lum2

def Affi():
    shhAffi()
    OledAffi()
    LedAffi()
    Rec()

def shhAffi():
    print("NNumero : {}".format(arr[count][0]))
    print("Media : {}".format(arr[count][1]))
    print("Direct : {}".format(arr[count][2]))
    print("Lum1 : {}".format(arr[count][3]))
    print("lum2 : {}".format(arr[count][4]))

def OledAffi():
    global count
    global arr
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    padding = 2
    shape_width = 20
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    font = ImageFont.load_default()

    draw.text((x, top),    str(count),  font=font, fill=255)
    draw.text((x, top+10), "Direct : {}".format(arr[count][2]), font=font, fill=255)
    draw.text((x, top+20), "Media : {}".format(arr[count][1]), font=font, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    pass

def LedAffi():

    if arr[count][3] == 'on':
        Lum1_led.on()
    elif arr[count][3] == 'off':
        Lum1_led.off()
    pass

    if arr[count][4] == 'on':
        Lum2_led.on()
    elif arr[count][4] == 'off':
        Lum2_led.off()
    pass

count = 0

def Rec():
    titre = ['num', 'Media', 'Direct', 'Lum1', 'Lum2']
    z = 0

    New_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Tops>\n'
    for row in arr:
        New_xml = New_xml + '\t<Top>\n'
        for elem in row:
            New_xml = New_xml + '\t\t<' + titre[z] + '>' + elem + '</' + titre[z] + '>\n'
            z = z + 1
        New_xml = New_xml + '\t</Top>\n'
        z = 0
    New_xml = New_xml + '</Tops>'

    fichier = open("loop/data.xml", "w")
    fichier.write(New_xml)
    fichier.close()
    #print(New_xml)
    pass
#arr.append(['NEW', 'Media', 'on', 'on', 'on'])
Affi()
pause()
