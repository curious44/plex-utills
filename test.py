#!/usr/bin/env python3
import fnmatch
from collections import defaultdict
from plexapi.server import PlexServer

from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

server = config_object["PLEXSERVER"]


baseurl = (server["PLEX_URL"])
token = (server["TOKEN"])
films = (server["FILMSLIBRARY"])
plex = PlexServer(baseurl, token)
movies_section = plex.library.section('films')
movies = defaultdict(list)
added = movies_section.search(sort='titleSort')



for movie in added:
    movies[movie.title].append(movie.studio)
    #print(movies)      
    #studio = {movie.studio for movie in movies}
    #fnmatch.filter(movies, '[*]Disney[*]')
    #print(movies)
    fnmatch.filter(movies, '*Disney*')
print('%s (%s)' % (movie.title, movie.studio))

    