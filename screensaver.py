PYGAME_HIDE_SUPPORT_PROMPT = '1'
import pygame
import tkinter as tk
from datetime import datetime as dt
import random
import spotipy
import spotipy.oauth2 as oauth2

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
game_clock = pygame.time.Clock()
largestBallSize = 50
ballsizeDif = 2
REALCLOCK = 0

client_id ='' #write in
client_secret = ''
redirect_uri = 'http://localhost:8080/'

Height_to_width_ratio = 1 #testing font size function

color_palette = {
    'white': (255,255,255), 
    'red': (186, 56, 33), 
    'orange' : (200, 122, 44), 
    'yellow' : (219, 182, 94),
    'green': (133, 160, 136),
    'middlegreen': (133, 160, 150),
    'middlegreen' : (105, 130, 125), 
    'darkgreen': (99, 116, 120), 
    'darkgray': (15, 28, 44), 
    'blueblack': (9, 12, 29)
}

purple_palette = {
    'warmtan': (139, 133, 137), 
    'tan': (152, 152, 152), 
    'gray': (121, 137, 150), 
    'lightpurple': (151, 154, 170), 
    'darkpurple': (76, 81,109)
}

class spotify_obj(spotipy.client.Spotify):
    def __init__(self, auth_manager):
        super().__init__(auth_manager = auth_manager)

class RealClock(pygame.sprite.Sprite):
    """shows time"""
    def  __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.font = pygame.font.Font(None, 400)
        self.font.set_italic(1)
        self.color = color_palette['blueblack']
        self.lasttime = -1  ###replaced by actual last time when run
        self.update()
        self.rect = self.image.get_rect().move(50, 650) # position on screen
    def update(self, *args, **kwargs):
        """update() if time has changed"""
        if REALCLOCK != self.lasttime:
            self.lasttime = REALCLOCK
            msg = f'{REALCLOCK}'
            self.image = self.font.render(msg, 1, self.color)

class TrackTitle(pygame.sprite.Sprite):
    '''shows title of current track'''
    def __init__(self, title):
        pygame.sprite.Sprite.__init__(self)
        fontSize = round((screen_width/len(title))*Height_to_width_ratio)
        self.font = pygame.font.Font(None, fontSize)
        self.font.set_italic(0)
        self.color = 'white'
        self.lasttitle = -1 ###replaced by actual last title when run
        self.title = title
        self.update()
        verticalP = 350-(fontSize*.66)
        self.rect = self.image.get_rect().move(20, verticalP) ##position on screen

    def update(self, *args, **kwargs):
           '''update if track has changed'''
           if  self.title != self.lasttitle:
               self.lasttitle = self.title
               msg = f'{self.title}'
               self.image = self.font.render(msg, 0, self.color)

class ArtistName(pygame.sprite.Sprite):
    '''shows name of current artist'''
    def __init__(self, artist):
        pygame.sprite.Sprite.__init__(self)
        fontSize = round((screen_width/len(artist))*Height_to_width_ratio)
        self.font = pygame.font.Font(None, fontSize)
        self.font.set_italic(0)
        self.color = 'white'
        self.lastartist= -1  ###replaced by actual last artist when run
        self.artist = artist
        self.update()
        self.rect = self.image.get_rect().move(20, 350) #position on screen

    def update(self, *args, **kwargs):
        '''update if track has changed'''
        if  self.artist != self.lastartist:
            self.lastartist = self.artist
            msg = f'{self.artist}'
            self.image = self.font.render(msg, 0, self.color)

class NowPlaying(pygame.sprite.Sprite):
    '''now playing'''
    def __init__(self, message):
        pygame.sprite.Sprite.__init__(self)
        fontSize = round((screen_width/len(message))*Height_to_width_ratio)
        self.font = pygame.font.Font(None, fontSize)
        self.font.set_italic(0)
        self.color = color_palette['green']
        self.message = message
        self.update()
        self.rect = self.image.get_rect().move(20, 10) #position on screen
    
    def update(self, *args, **kwargs):
        self.image = self.font.render(self.message, 0, self.color)

class starAnimation(pygame.sprite.Sprite):
    def __init__(self):
        self.star_field_slow = []
        self. star_field_medium = []
        #star_field_fast = []

        for slow_stars in range(50): 
            star_loc_x = random.randrange(0, screen_width)
            star_loc_y = random.randrange(0, screen_height)
            self.star_field_slow.append([star_loc_x, star_loc_y]) 
        for medium_stars in range(35):
            star_loc_x = random.randrange(0, screen_width)
            star_loc_y = random.randrange(0, screen_height)
            self.star_field_medium.append([star_loc_x, star_loc_y])

    def update(self, screen, *args, **kwargs):
        for star in self.star_field_slow:
            star[1] += .5
            if star[1] > screen_height+largestBallSize:
                star[0] = random.randrange(0, screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, color_palette['middlegreen'], star, largestBallSize) 

        for star in self.star_field_medium:
            star[1] += .7
            if star[1] > screen_height+largestBallSize:
                star[0] = random.randrange(0, screen_width) 
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, color_palette['middlegreen'], star, largestBallSize-ballsizeDif)



def make_time(time):
    '''formats time from datetime'''
    min = time.minute if time.minute >=10 else f'0{time.minute}' ##single digit minutes show as :04 instead of :4 (for ex)

    if time.hour <12:
        return(f'{time.hour}:{min}am')
    if time.hour == 12: 
        return (f'{time.hour}:{min}pm')
    else:
        hour = time.hour-12
        return(f'{hour}:{min}pm')

def open_window():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True

    stars = starAnimation()
    while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # pygame.quit ends
        for event in pygame.event.get():
            #print(event.type)
            if event.type == pygame.KEYDOWN: # running set to false if any key is pressed
                running = False
            

    # fill the screen with a color to wipe away anything from last frame
        screen.fill(color_palette['darkgreen'])

        global REALCLOCK
        time = make_time(dt.now())
        REALCLOCK = time
        all = pygame.sprite.RenderUpdates()
        all.add(NowPlaying('now playing:'))
        all.add(RealClock())
        try:
            all.add(TrackTitle(get_spotify_info()[0]))
            all.add(ArtistName(get_spotify_info()[1]))
        except:
            all.add(TrackTitle('music'))
            all.add(ArtistName('paused'))

    # RENDER YOUR GAME HERE
        stars.update(screen)
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        pygame.display.flip()

        game_clock.tick(30) #sets frames per second

    pygame.quit() # quits when running is no longer true

def get_spotify_info():
    sp = spotify_obj(auth_manager = oauth2.SpotifyOAuth(client_id = client_id,
                                                        client_secret = client_secret,
                                                        redirect_uri = redirect_uri,
                                                        scope = "user-read-currently-playing"))

    info = sp.current_user_playing_track()
    track = info['item']['name']
    artist = info['item']['artists'][0]['name']
    img = info['item']['album']['images']
    return [track, artist, img]
    

def main():
    open_window()
main()

