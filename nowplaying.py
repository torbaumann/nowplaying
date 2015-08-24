"""
Version 1.0

Change log:

Version 1.0
Displays all live player state info and track info and updates appropriately
Issues with line length - todo: implement line scrolling
Progress bar non functional

"""
 
import pygame
from pygame.locals import *
import os
import time
from time import sleep
from mpd import MPDClient

# ---- GLOBAL DEFINITIONS ---- # 

# Colour definitions
COL_VERY_BRIGHT = (255, 166, 0)
COL_BRIGHT = (255, 120, 0)
COL_DULL = (166, 88, 0)
COL_WHITE = (255, 255, 255, 255)

#Set colour of background
BACKGROUND_COLOUR = (31, 16, 0)

# Fonts and media
FONTLCD = '/usr/share/fonts/truetype/digital7/digital-7.ttf'
FONTLCDITALIC = '/usr/share/fonts/truetype/digital7/digital-7 (italic).ttf'
FONTDROID = '/usr/share/fonts/truetype/droid/DroidSans.ttf'
FONTFUTURA = '/usr/share/fonts/truetype/futura/Futura-Medium.ttf'
FONTFUTURAITALIC = '/usr/share/fonts/truetype/futura/Futura-MediumItalic.ttf'
MEDIA_FILES = '/home/pi/tutorials/pygamelcd/' 



# ---- MPD CLIENT SETUP ----#

client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed)
client.idletimeout = None          # timeout for fetching
client.connect("localhost", 6600)  # connect to localhost:6600


# --- STATIC IMAGES ---#
# Progress bar
progress_bar = pygame.image.load(os.path.join(MEDIA_FILES, 'progress_bar.png'))
progress_bar_rect = progress_bar.get_rect()
progress_bar_rect.x = 16
progress_bar_rect.y = 210

# ---- FUNCTIONS ----#


""" Check state of MPD. Accepts the following fields in
 the checkfield var: random, consume, repeat, state """

def check_state(checkfield, checkstate, printon, printoff):
    varstate = client.status()[checkfield]
    if varstate == str(checkstate):
    	returnvar = str(printoff)
    else:
    	returnvar = str(printon)
    return returnvar



""" Check state of currently playing song. Accepts the following fields
in the checkfield var: artist, album, title, song, playlistlength """

def check_song(checkfield):
    try:
    	song_state = client.currentsong()[checkfield]
    except:
    	song_state = str('----------')
    	return song_state
    else:
    	return song_state


""" Check state of playlist. Accepts the following fields
 in the checkfield var: song, playlistlength """

def check_plist(checkfield):
    try:
    	returnvar = client.status()[checkfield]
    except:
    	returnvar = str('--')
    	return returnvar
    else:
    	return returnvar


""" Destructor to make sure pygame shuts down, etc. """
def __del__(lcd):
	" Destructor to make sure pygame shuts down, etc. "


# Image loader
def load_image(name, colorkey=None):
    fullname = os.path.join(MEDIA_FILES, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
        	colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



#Update player data
def updatelines():
	if done == False:
		ShuffleStatus.data = check_state('random', 0, 'RAND ON', 'RAND OFF')
		MpdStatus.data = check_state('state', 'play', 'STOPPED', 'PLAYING')
		ConsumeStatus.data = check_state('consume', 0, 'CON ON', 'CON OFF')
		RepeatStatus.data = check_state('repeat', 0, 'REP ON', 'REP OFF')
		ArtistStatus.data = check_song('artist')
		AlbumStatus.data = check_song('album')
		TrackStatus.data = check_song('title')
		TrackNumStatus.data = check_plist('playlistlength')
		
		

# ---- CLASSES ----#

class ShuffleStatus:
	fontsize = 12
	font = FONTFUTURA
	x_pos = 90
	y_pos = 12
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_state('random', 0, 'RAND ON', 'RAND OFF')
   
class MpdStatus:
	fontsize = 12
	font = FONTFUTURA
	x_pos = 16
	y_pos = 12
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_state('state', 'play', 'PLAYING', 'STOPPED')
	
class ConsumeStatus:
   fontsize = 12
   font = FONTFUTURA
   x_pos = 170
   y_pos = 12
   colour1 = COL_WHITE
   colour2 = COL_BRIGHT
   data = check_state('consume', 0, 'CON ON', 'CON OFF')
   
class RepeatStatus:
	fontsize = 12
	font = FONTFUTURA
	x_pos = 250
	y_pos = 12
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_state('repeat', 0, 'REP ON', 'REP OFF')

class ArtistStatus:
	fontsize = 16
	font = FONTFUTURA
	x_pos = 20
	y_pos = 85
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_song('artist')
   
class AlbumStatus:
	fontsize = 16
	font = FONTFUTURA
	x_pos = 16
	y_pos = 65
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_song('album')

  
class TitleStatus:
	fontsize = 28
	font = FONTFUTURA
	x_pos = 16
	y_pos = 110
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_song('title')

# Song name 
class TrackStatus:
	fontsize = 28
	font = FONTFUTURA
	x_pos = 16
	y_pos = 110
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_song('title')
   
class TrackNumStatus:
	fontsize = 12
	font = FONTFUTURA
	x_pos = 16
	y_pos = 180
	colour1 = COL_WHITE
	colour2 = COL_BRIGHT
	data = check_plist('playlistlength')
	
# Needle
class Needle(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image, self.rect = load_image('needle.png', None)
		self.area = lcd.get_rect()
		#   self.rect.topleft = 75, 205
		self.rect.x = 320 - 24
		self.rect.y = 205
		self.playing = 10
		self.paused = 0
		self.start = 0




# ---- SET SCREEN & INITIALISE PYGAME ----#

#Set up display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
screensize = (320, 240)
lcd = pygame.display.set_mode(screensize)
pygame.display.update()
sleep(1)

pygame.mouse.set_visible(False)
 

# Loop until the user clicks the close button.
done = False
 

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
 
    # --- Drawing code should go here
 
    # First, clear the screen to background colour. Don't put other drawing commands
    # above this, or they will be erased with this command.
    lcd.fill(BACKGROUND_COLOUR)
    font_repeat = pygame.font.Font(RepeatStatus.font, RepeatStatus.fontsize)
    line_repeat = str(RepeatStatus.data)

    
    font_lcon = pygame.font.Font(ConsumeStatus.font, ConsumeStatus.fontsize)
    line_con = str(ConsumeStatus.data)
    
    font_lshuf = pygame.font.Font(ShuffleStatus.font, ShuffleStatus.fontsize)
    line_shuf = str(ShuffleStatus.data)
    
    font_lmpd = pygame.font.Font(MpdStatus.font, MpdStatus.fontsize)
    line_mpd = str(MpdStatus.data)
    
    font_artist = pygame.font.Font(ArtistStatus.font, ArtistStatus.fontsize)
    line_artist = str(ArtistStatus.data)
    
    font_album = pygame.font.Font(AlbumStatus.font, AlbumStatus.fontsize)
    line_album = str(AlbumStatus.data)
    
    font_track = pygame.font.Font(TrackStatus.font, TrackStatus.fontsize)
    line_track = str(TrackStatus.data)
    
    font_tracknum = pygame.font.Font(TrackNumStatus.font, TrackNumStatus.fontsize)
    line_tracknum = str("Track:  " + str(TrackNumStatus.data) + "/" + str(TrackNumStatus.data))
    # To be fixed
    
    text_artist = font_artist.render(line_artist.lower(), True, ArtistStatus.colour1)
    text_album = font_album.render(line_album.lower(), True, AlbumStatus.colour1)
    text_track = font_track.render(line_track.lower(), True, TrackStatus.colour2)
    text_tracknum = font_tracknum.render(line_tracknum, True, TrackNumStatus.colour2)
    text_mpd = font_lmpd.render(line_mpd.lower(), True, MpdStatus.colour2)
    text_shuf = font_lshuf.render(line_shuf.lower(), True, ShuffleStatus.colour1)
    text_con = font_lcon.render(line_con.lower(), True, ConsumeStatus.colour1)
    text_repeat = font_repeat.render(line_repeat.lower(), True, RepeatStatus.colour1)
    
    lcd.blit(text_artist, (ArtistStatus.x_pos, ArtistStatus.y_pos))
    lcd.blit(text_album, (AlbumStatus.x_pos, AlbumStatus.y_pos))
    lcd.blit(text_track, (TrackStatus.x_pos, TrackStatus.y_pos))
    lcd.blit(text_tracknum, (TrackNumStatus.x_pos, TrackNumStatus.y_pos))
    lcd.blit(text_mpd, (MpdStatus.x_pos, MpdStatus.y_pos))
    lcd.blit(text_shuf, (ShuffleStatus.x_pos, ShuffleStatus.y_pos))
    lcd.blit(text_con, (ConsumeStatus.x_pos, ConsumeStatus.y_pos))
    lcd.blit(progress_bar, progress_bar_rect)
    lcd.blit(text_repeat, (RepeatStatus.x_pos, RepeatStatus.y_pos))
    
    needle = Needle()
    allsprites = pygame.sprite.RenderPlain(needle)
    
    allsprites.update()
    allsprites.draw(lcd)

 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Update data lines
    updatelines()
 
    # --- Limit to 10 frames per second
    clock.tick(10)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()