#!/bin/python

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306
import sys

# Raspberry Pi pin configuration:
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)


draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()



def get_image(angle, info):
    arrow = Image.open('up.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    rotated = arrow.rotate(angle = angle, center = (22, 16))
    text = ImageDraw.Draw(rotated)
    for i in range(len(info)):
        #display each index of info on different line.
        text.text((48, top + i * 8 ),str(info[i]), fill=255)
    #rotated.show()
    return rotated


def update_screen(angle, info):
    assert len(info) <= 4, 'Length of info can not be more than 4 to fit on display.'
    image = get_image(angle, info)
    #Clear previous frame
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    #Draw info
    disp.image(image)
    disp.display()
    #sleep(0.1)


def update_text(info):
    #New image to draw text on
    img = Image.new('RGB', (disp.width, disp.height), color = (0, 0, 0)).convert('1')
    #img = Image.open('up.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    text = ImageDraw.Draw(img)
    for i in range(len(info)):
        #display each index of info on different line.
        text.text((5, top + i * 8 ),str(info[i]), fill=255)

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(img)
    disp.display()


def loading_screen():
    logo = Image.open('savox.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    text = ImageDraw.Draw(logo)
    text.text((48, top + 16 ), 'Loading...', fill=255)
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(logo)
    disp.display()



def main(): 
    update_text([i for i in sys.argv])


#Testing



if __name__ == "__main__":
    main()
