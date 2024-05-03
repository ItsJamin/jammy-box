# jammy-box
 QR Code Music Box with Visualizing LED's

## Functions

Scan QR Codes, Read Em, Download The Audio Files, Play Audio Files, Visualize Them.

# Installation Guide

### Hardware - What You'll Need

- Raspberry Pi 4b 4GB (Other Raspberry Pi models should also work, I built and tested it on this model)
- Raspberry Camera (RPIZ CAM2 5MP)
- LED-Strip W2812B (if longer than 5m extra power supply could be necessary)
- (LED-Strip for internal light in Box Housing)
- (Speaker for playing the music)

Proper assets to control and power your Raspberry Pi (if you already have assets to control your Raspberry or are controlling it remotly skip this), I used:
- USB-C Cable
- HDMI Cable
- HDMI to Micro HDMI Adapter (GOOBAY 68842)
- Heat Sinks for Raspberry (RPI COOL 4XSI)
- Micro-SD-Card (LMEX1L064GG2)
- Display with HDMI-Port
- Mouse
- Keyboard

3D-Printer would be optimal to print the housing and the figures.

Printable objects are in the folder "TODO"

### Setting Up Raspberry Pi

For setting up a raspberry Pi look up a guide like [this](https://www.youtube.com/watch?v=BpJCAafw2qE&t=268s)

For adding the heat sinks look [here](https://www.youtube.com/watch?v=WMIniPIvYjM&t=283s)

### Setting Up Project

Clone the Project

`git clone https://github.com/ItsJamin/jammy-box`


Install reqiurements.txt

`cd jammy-box`
`pip3 install -r requirements.txt`

Essentially you will need:
- pygame (for running the audio)
- scipy (for analyzing wav files)
- yt-dlp (for downloading Music from YouTube)
And these 3 Commands for controlling LED:
```sudo pip3 install rpi_ws281x
sudo pip3 install adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka```
