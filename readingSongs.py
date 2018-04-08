from glob import glob
import os
from mutagen.easyid3 import EasyID3
from tinytag import TinyTag
from aubio import source, tempo
from numpy import median, diff
import discogs_client





from urllib.parse import urljoin

import oauth2 as oauth

from time import sleep

from pymongo import MongoClient




def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            print("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)
                    


def getInfoAndPost(songTitle,BPM):
    consumer_key = 'kcJaFxSMvYREoRtehKXq'
    consumer_secret = 'bNkeqXXEyStspRxvxSAJQhiNishkdhPu'


    d = discogs_client.Client('ExampleApplication/0.1', user_token="ItOvpBKXmHfVtVpEJKiPUqjfFobIlnWPhuLqqXFn")

    if songTitle is not None:
        results = d.search(songTitle, type='release')
    else :
        results = None
    
    
    if results is not None and len(results) > 0:
        theBPM = BPM
        theYear = results[0].year
        theCountry = results[0].country
        
        theGenre = results[0].genres[0]
        theLabel= results[0].labels[0].name
        theArtist = results[0].artists[0].name
    
        theTitle = songTitle

        #Check for noneTypes
        if theBPM is None:
            theBPM = ""

        if theYear is None:
            theYear = ""

        if theCountry is None:
            theCountry = ""

        
        if results[0].styles is None:
            theStyle = ""
        else :
            theStyle = results[0].styles[0]

        if theGenre is None:
            theGenre = ""

        if theLabel is None:
            theLabel = ""

        if theArtist is None:
            theArtist = ""

        if theTitle is None:
            theTitle = ""



        print(int(theBPM))
        print(theYear)
        print(theCountry)
        print(theStyle)
        print(theGenre)
        print(theLabel)
        print(theArtist)
        print(theTitle)
        allSong.insert_one({'BPM': int(theBPM), 'year': theYear, 'country': theCountry , 'style': theStyle, 'genre': theGenre, 'label': theLabel, 'artist': theArtist, 'title': theTitle})




def readSongs():
    path = "/Users/aryamirshafii/Music/iTunes/iTunes Media/Music"
    for root, dirs, files in os.walk(path):
        if files is not None:
            for name in files:
                if name.endswith((".mp3")):
                    songName = (os.path.join(root, name))
                    #print(songName)
                    #mp3info = EasyID3(shpfiles)

                    #print(mp3info.title)

                    tag = TinyTag.get(songName)
                    print("")
                    print("")
                    #print(name)
                    #print('Name: %s.' % tag.title)
                    #print('Artist Name: %s.' % tag.artist)
                    #print('Artist Name: %s.' % tag.album)
                    #print(get_file_bpm(songName))
                    getInfoAndPost(tag.title, get_file_bpm(songName))
                    sleep(1) # So api does not give warning for too many http requests


# actual code run
client = MongoClient()
db = client.songDB
allSong = db.allsongs
readSongs()











    
