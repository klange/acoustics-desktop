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

class CurlReader:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf
def curl(url):
    t = CurlReader()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, t.body_callback)
    c.perform()
    c.close()
    return t.contents

pynotify.init("Acoustics")

last_result = -1

def art_url(artist,album,title):
    return "http://localhost:8080/amp/art.py?size=64&artist=" + urllib.quote(artist.encode("utf-8")) + "&album=" + urllib.quote(album.encode("utf-8")) + "&title=" + urllib.quote(title.encode("utf-8"))

def appendNotice(title, content):
    n = pynotify.Notification(title, content, icon_path) #"notification-audio-volume-high")
    n.set_hint_string('append','')
    n.show()

while 1:
    acoustics = simplejson.loads(curl(amp_url))

    if acoustics['now_playing']:
        if not acoustics['now_playing']['song_id'] == last_result:
            last_result = acoustics['now_playing']['song_id']
            song_title  = acoustics['now_playing']['title']
            song_artist = acoustics['now_playing']['artist']
            song_album  = acoustics['now_playing']['album']
            print "New song: %s\nby: %s\nfrom: %s" % (song_title, song_artist, song_album)
            albumart    = simplejson.loads(curl(art_url(song_artist,song_album,song_title)))
            if albumart["image"] and albumart["image"].startswith("http"):
                os.system("wget --quiet -O /tmp/_amp_icon " + albumart["image"])
                os.system("convert -quiet /tmp/_amp_icon /tmp/_amp_icon.png")
                icon_path = "file:///tmp/_amp_icon.png"
            else:
                icon_path = fallback
            print icon_path.strip()
            appendNotice(song_title,song_artist)
            appendNotice(song_title,song_album)
            appendNotice(song_title,"")

    time.sleep(5)
