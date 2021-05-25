from pathlib import Path
from PIL import Image
from plexapi.server import PlexServer
import numpy as np
import requests
import shutil
import os
import re
import stat
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("config.ini")
server = config_object["PLEXSERVER"]
baseurl = (server["PLEX_URL"])
token = (server["TOKEN"])
films = (server["FILMSLIBRARY"])
ppath = (server["PLEXPATH"])
mpath = (server["MOUTEDPATH"])
plex = PlexServer(baseurl, token)
films = plex.library.section(films)
banner_4k = Image.open("4K-Template.png")
banner_hdr = Image.open("hdr-poster.png")
banner_4k_hdr = Image.open("4k-hdr-poster.png")
size = (911,1367)



def poster_4k_hdr():
    print(i.title + ' 4k HDR')
    newdir = os.path.dirname(re.sub(ppath, mpath, i.media[0].parts[0].file))+'/'
    backup = os.path.exists(newdir+'poster_bak.png') 
    if backup == False:    
        imgurl = baseurl + i.thumb + '.png'
        img = requests.get(imgurl, stream=True)
        filename = "poster.png"
        if img.status_code == 200:
            img.raw.decode_content = True
            with open(filename, 'wb') as f:
                shutil.copyfileobj(img.raw, f)
        print('Creating a backup file')
        dest = shutil.copyfile(filename, newdir+'poster_bak.png')
        os.chown(newdir+'poster_bak.png', 99, 100)
        os.chmod(newdir+'poster_bak.png', 0o0666)

        background = Image.open('poster.png')
        background = background.resize(size,Image.ANTIALIAS)
        background.paste(banner_4k_hdr, (0, 0), banner_4k_hdr)
        background.save('poster.png')
        i.uploadPoster(filepath="poster.png")
        os.remove('poster.png') 
    else:
        print('Backup File Exists, Skipping...')    

def poster_4k():
    print(i.title + " 4K Poster")
    newdir = os.path.dirname(re.sub(ppath, mpath, i.media[0].parts[0].file))+'/'
    backup = os.path.exists(newdir+'poster_bak.png') 
    
    if backup == False:
        imgurl = baseurl + i.thumb + '.png'
        img = requests.get(imgurl, stream=True)
        filename = "poster.png"
        if img.status_code == 200:
            img.raw.decode_content = True
            with open(filename, 'wb') as f:
                shutil.copyfileobj(img.raw, f)


        print('Creating a backup file')
        dest = shutil.copyfile(filename, newdir+'poster_bak.png')
        os.chown(newdir+'poster_bak.png', 99, 100)
        os.chmod(newdir+'poster_bak.png', 0o0666)

        background = Image.open('poster.png')
        background = background.resize(size,Image.ANTIALIAS)
        background.paste(banner_4k, (0, 0), banner_4k)
        background.save('poster.png')
        i.uploadPoster(filepath="poster.png")
        os.remove('poster.png') 
    else:
        print('Backup File Exists, Skipping...')

def poster_hdr():
    print(i.title + " HDR Poster")
    newdir = os.path.dirname(re.sub(ppath, mpath, i.media[0].parts[0].file))+'/'
    backup = os.path.exists(newdir+'poster_bak.png') 
    if backup == False:
        imgurl = baseurl + i.thumb + '.png'
        img = requests.get(imgurl, stream=True)
        filename = "poster.png"
        if img.status_code == 200:
            img.raw.decode_content = True
            with open(filename, 'wb') as f:
                shutil.copyfileobj(img.raw, f)

            print('Creating a backup file')
            dest = shutil.copyfile(filename, newdir+'poster_bak.png')
            os.chown(newdir+'poster_bak.png', 99, 100)
            os.chmod(newdir+'poster_bak.png', 0o0666)
        background = Image.open('poster.png')
        background = background.resize(size,Image.ANTIALIAS)
        background.paste(banner_hdr, (0, 0), banner_hdr)
        background.save('poster.png')
        i.uploadPoster(filepath="poster.png")
        os.remove('poster.png') 
    else:
        print('Backup File Exists, Skipping...')


for i in films.search(resolution="4k", hdr=True):
    poster_4k_hdr()
for i in films.search(resolution="4k", hdr=False):
    poster_4k()
for i in films.search(resolution="1080,720", hdr=True):
    poster_hdr()