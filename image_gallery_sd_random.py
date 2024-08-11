# This is a fork of the github repo: micropython/examples/inky_frame/image_gallery/image_gallery_sd_random.py
# The code is mainly to imrove the pre-existing code for my micropython learning and to get my Inky Frame going

# Moving from (to me odd) docquotes of python. Here's what Pimoroni says:
# An offline image gallery that displays a random image from your SD card and updates on a timer.
# Copy images to the root of your SD card by plugging it into a computer.
# If you want to use your own images they must be the screen dimensions (or smaller)
# and saved as *non-progressive* jpgs.

# Mac tips: can open an image in preview, click info, and JFIF tab to see if progressive image
# This code also ensures that we skip the "." files that MacOS creates on copying files

# Make sure to uncomment the correct size for your display!
from picographics import PicoGraphics, DISPLAY_INKY_FRAME as DISPLAY    # 5.7"
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"

from machine import Pin, SPI
import jpegdec
import sdcard
import os
import inky_frame
import random

# how often to change image (in minutes)
UPDATE_INTERVAL = 1

# set up the display
graphics = PicoGraphics(DISPLAY)

# set up the SD card
sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(22))
os.mount(sd, "/sd")

# Create a new JPEG decoder for our PicoGraphics
j = jpegdec.JPEG(graphics)


def display_image(filename):

    # Open the JPEG file
    j.open_file(filename)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    graphics.update()


inky_frame.led_busy.on()

# Get a list of files that are in the directory
files = os.listdir("/sd")
# remove files from the list that aren't .jpgs or .jpegs
files = [f for f in files if f.endswith(".jpg") or f.endswith(".jpeg")]
# and not mac generated hidden "." files
files = [f for f in files if not f.startswith(".")]
# initial variable "lastfile" so that we don't select the same picture twice in a row
lastfile = ""

while True:
    
    # pick a random file
    file = files[random.randrange(len(files))]
    
    # if the selected file is same as the last selection, re-choose
    while file == lastfile:
        file = files[random.randrange(len(files))]

    # once we know that we haven't picked the same file
    # can move on and update the lastfile variable for the next cycle
    lastfile = file

    # Open the file
    print(f"Displaying /sd/{file}")
    
    # Clear the screen
    # note that the picographics manual has this as display.clear()
    # but we initilaised this as graphics at top
    graphics.clear()
    
    # Display the image
    display_image("/sd/" + file) 

    # Sleep or wait for a bit
    print(f"Sleeping for {UPDATE_INTERVAL} minutes")
    inky_frame.sleep_for(UPDATE_INTERVAL)
