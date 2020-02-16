version = "0.2.1"

# Discord RPC doesn't work for this version at the moment!

from tkinter import *
import tkinter as tk
import youtube_dl
import os
import sys
import pygame as pg
from PIL import Image
import requests
from io import BytesIO
try:
    import rpc
    client_id = '676288890331463700' #Soundcloud Client ID (Don't Change Unless you want to change the name)
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    print("RPC connection successful.")
    discordsupport = True
except:
    discordsupport = False
import time

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'mp3',
    'outtmpl': '%(extractor)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch',
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

def offlineplayy(file, *, loop=None, stream=False):
    volume=0.8
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    pg.mixer.music.load("soundcloud-" + file + ".mp3")
    print("Now Playing {}...".format(file))
    pg.mixer.music.play()

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
    pg.mixer.music.play()
    start_time = time.time()
    #if discordsupport == True:
    #    discordup(filename, scurl, url)
    #    print("[Discord] Set Rich Presence!")
    #else:
    #    print("[Discord] Discord not Found!")
    #while pg.mixer.music.get_busy():
    #    clock.tick(30)

def search(query, *, loop=None, stream=False):
    volume=0.8
    data = ytdl.extract_info(query)
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
    print("Now Playing {}...".format(data['title']))
    nowplaying = Tk()
    nowplaying.title('{} - Soundcloud Client v{}'.format(data['title'], version))
    np = Label(nowplaying, text="Now Playing: {} by {}".format(data['title'], data['uploader']))
    np.pack()
    #canvas = Canvas(nowplaying, width = 512, height = 512)      
    #canvas.pack()  
    #canvas.create_image(20,20, anchor=NW, image=Image.open(requests.get(data['thumbnail'], stream=True).raw))
    pg.mixer.music.play()
    start_time = time.time()

master = Tk()
master.title('Soundcloud Client v{}'.format(version))
txr = Label(master, text="Soundcloud Client Made by Artucuno#1898")
txr.pack()
e = Entry(master)
e.pack()

e.focus_set()

def srch():
    search(e.get())

def offlineplay():
    offlineplayy(e.get())

def callback():
    from_url(e.get())

def stop():
    pg.mixer.music.stop()

def pause():
    pg.mixer.music.pause()

def resume():
    pg.mixer.music.unpause()

def loop():
    try:
        pg.mixer.music.play(-1)
    except:
        print("Make sure you press play first!")

src = Button(master, text="Search", width=10, command=srch)
src.pack()
b = Button(master, text="Play", width=10, command=callback)
b.pack()
off = Button(master, text="Offline Play", width=10, command=offlineplay)
off.pack()
stop = Button(master, text="Stop", width=10, command=stop)
stop.pack()
pause = Button(master, text="Pause", width=10, command=pause)
pause.pack()
resu = Button(master, text="Resume", width=10, command=resume)
resu.pack()

lop = Button(master, text="Loop", width=10, command=loop)
lop.pack()

e.pack()
canvas = Canvas(master, width = 512, height = 512)      
canvas.pack()      
img = PhotoImage(file="data/assets/sc.png")      
canvas.create_image(20,20, anchor=NW, image=img) 

text = e.get()
mainloop()

text = content.get()
content.set(text)
