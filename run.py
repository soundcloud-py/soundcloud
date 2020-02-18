print("[Client] Loading Soundcloud Client...")

# Soundcloud Client Python made by Artucuno (Artucuno#1898)

# Resorces Used:
# discord.py basic_voice example (For file download)
# Discord Python RPC (No Longer Maintained) (Used for Rich Presence)

import youtube_dl
import os
import sys
import pygame as pg
import rpc
try:
    client_id = '676288890331463700' #Soundcloud Client ID (Don't Change Unless you want to change the name)
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    print("RPC connection successful.")
    discordsupport = True
except:
    discordsupport = False
import time

IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
#IS_LINUX = sys.platform == "linux"

def clear_screen():
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def user_choice():
    return input("\n>>> ").strip()

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def idle():
    while True:
        start_time = time.time()
        idle = {
            "state": "Currently Idle",
            "details": "Soundcloud Client [BETA] v0.1.2",
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": "Not Playing",
                "small_image": "sc",
                "large_text": "Currently Idle",
                "large_image": "sc"
            }
        }
        rpc_obj.set_activity(idle)
        main()

def discordup(track, url, aurl):
    while True:
        start_time = time.time()
        activity = {
            "state": "Playing a Track... {}".format(aurl),
            "details": "Soundcloud Client [BETA] v0.1.2",
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "small_text": aurl,
                "small_image": "sc",
                "large_text": "Playing a Track.",
                "large_image": "sc"
            }
        }
        rpc_obj.set_activity(activity)
        while pg.mixer.music.get_busy():
            time.sleep(10)
        idle()
        main()

def from_url(url, *, loop=None, stream=False):
    volume=0.8
    scurl = "https://soundcloud.com/{}".format(url)
    data = ytdl.extract_info(scurl)
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    
    if 'entries' in data:
        data = data['entries'][0]
	
    filename = data['url'] if stream else ytdl.prepare_filename(data)
    pg.mixer.music.load(filename)
    print("Now Playing {}...".format(url))
    ##clock = pg.time.Clock()
    ##print("Elapsed time{}".time)
    pg.mixer.music.play()
    start_time = time.time()
    if discordsupport == True:
        discordup(filename, scurl, url)
        print("[Discord] Set Rich Presence!")
    else:
        print("[Discord] Discord not Found!")
    while pg.mixer.music.get_busy():
        clock.tick(30)
    main()
try:
	def main():
    		clear_screen()
    		urll = input('Enter a soundcloud track (EG: artucuno/wave) >>> ')
    		from_url(urll)
except KeyboardInterrupt:
	print("\n\nSoundcloud has exited.")
	sys.exit(0)

try:
    main()
except KeyboardInterrupt:
    print("\n\nSoundcloud has exited.")
    sys.exit(0)
