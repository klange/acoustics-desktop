#!/usr/bin/env python
import pynotify
import simplejson, pycurl
import sys, urllib, time, os

amp_url = "http://localhost:8080/amp/json.pl"

# Silly hack
icon_path = "file://%s/amp_a.png" % os.getcwd()
fallback  = "file://%s/amp_a.png" % os.getcwd()

reload(sys)
sys.setdefaultencoding("utf-8")

def curl(url):
    f = urllib.urlopen(url)
    x = f.read()
    f.close()
    return x

pynotify.init("Acoustics")

last_result = -1

def art_url(artist,album,title):
    _artist = str(urllib.quote(artist.encode("utf-8"))).replace("/","%252f")
    _album  = str(urllib.quote(album.encode("utf-8" ))).replace("/","%252f")
    _title  = str(urllib.quote(title.encode("utf-8" ))).replace("/","%252f")
    return "http://localhost:8080/amp/json.pl?mode=art&artist=%s&album=%s&title=%s&size=64" % (_artist, _album, _title)

def appendNotice(title, content):
    n = pynotify.Notification(title, content, icon_path) #"notification-audio-volume-high")
    n.set_hint_string('append','')
    n.show()

attempts = 1

while 1:
    try:
        acoustics = simplejson.loads(curl(amp_url))

        if acoustics['now_playing']:
            if not acoustics['now_playing']['song_id'] == last_result:
                last_result = acoustics['now_playing']['song_id']
                song_title  = acoustics['now_playing']['title']
                song_artist = acoustics['now_playing']['artist']
                song_album  = acoustics['now_playing']['album']
                print "Now Playing: %s\nby: %s\nfrom: %s\n" % (song_title, song_artist, song_album)
                art         = art_url(song_artist, song_album, song_title)
                if art:
                    albumart    = curl(art)
                    if albumart:
                        f = open("/tmp/_amp_icon", "w")
                        f.write(albumart)
                        f.close()
                        os.system("convert /tmp/_amp_icon /tmp/_amp_icon.png")
                        icon_path = "file:///tmp/_amp_icon.png"
                    else:
                        icon_path = fallback
                else:
                    icon_path = fallback
                appendNotice(song_title,song_artist)
                appendNotice(song_title,song_album)
                appendNotice(song_title,"")
        else:
            if last_result != 0:
                print "Nothing playing.\n"
                last_result = 0
        attempts = 1
    except:
        print "Failed to connect or retrieve stuff, attempt",attempts
        attempts += 1
        if attempts > 10:
            print "Failed to get information after ten attempts. Good bye."
            sys.exit(1)
    time.sleep(5)
