#!/usr/bin/env python
import pynotify
import simplejson, pycurl
import sys, urllib, time

amp_url = "http://localhost:8080/amp/json.pl"

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

while 1:
    json_output = curl(amp_url)
    acoustics = simplejson.loads(json_output)

    if acoustics['now_playing']:
        if not acoustics['now_playing']['song_id'] == last_result:
            last_result = acoustics['now_playing']['song_id']
            song_title  = acoustics['now_playing']['title']
            song_artist = acoustics['now_playing']['artist']
            song_album  = acoustics['now_playing']['album']
            print "New song: %s\nby: %s\nfrom: %s" % (song_title, song_artist, song_album)
            n = pynotify.Notification(song_title, song_artist + " <br />" + song_album, "notification-audio-volume-high")
            n.show()

    time.sleep(5)
