#!/usr/bin/env python
"""
    Ubuntu Notification Client for Acoustics

    Produces popup notifications with libnotify to show the currently
    playing song from an Acoustics (amp) instance with album art.

    Released under the terms of the NCSA license.

    Usage:
        - Adjust `amp_url` below to match your Acoustics server.
        - Run from a desktop Ubuntu session or other libnotify-capable
          Linux desktop system.
        - Enjoy

    Prerequisites:
        - Requires `convert` because I'm lazy and it's the quickest
          way to ensure a piece of album art is a PNG.
        - You need `pynotify`, the Python libnotify module
"""
import pynotify
import simplejson, pycurl
import sys, urllib, time, os

# Reload `sys` so we can get at the default encoding and set it
# to unicode (utf-8) so that foreign song titles, etc. work.
reload(sys)
sys.setdefaultencoding("utf-8")

# The URL of the acoustics instance
amp_url    = "http://localhost/amp/json.pl"

# Time to sleep between polls
sleep_time = 5

# Fallback image is available from the directory that
# we are stored in.
fallback   = "file://%s/amp_a.png" % sys.path[0]
icon_path  = fallback

def curl(url):
    """ Retreive the contents of the requested url"""
    f = urllib.urlopen(url)
    x = f.read()
    f.close()
    return x

# Initialize the libnotify instance
pynotify.init("Acoustics")

# The contents of our last poll
last_result = -1

def art_url(artist,album,title):
    """ Get a URL to request album art from """
    # We encode everything as quoted utf-8, replace forward slashes with the appropriate
    # escaped URL character, and then squeeze it all together.
    _artist = str(urllib.quote(artist.encode("utf-8"))).replace("/","%252f")
    _album  = str(urllib.quote(album.encode("utf-8" ))).replace("/","%252f")
    _title  = str(urllib.quote(title.encode("utf-8" ))).replace("/","%252f")
    return amp_url + "?mode=art&artist=%s&album=%s&title=%s&size=64" % (_artist, _album, _title)

# Count the number of failed attempts.
attempts = 1

while 1:
    try:
        # Retreive the JSON from the API
        acoustics = simplejson.loads(curl(amp_url))
        # Check that a song is playing
        if acoustics['now_playing']:
            # If so, check if this isn't the same data as the last time we polled
            if not acoustics['now_playing']['song_id'] == last_result:
                # And if it isn't, build a notification bubble.
                last_result = acoustics['now_playing']['song_id']
                song_title  = acoustics['now_playing']['title']
                song_artist = acoustics['now_playing']['artist']
                song_album  = acoustics['now_playing']['album']
                # Print the currently playing song to stdout. Makes a nice log of what's been playing.
                print "Now Playing: %s\nby: %s\nfrom: %s\n" % (song_title, song_artist, song_album)
                # Collect the ablum art URL...
                art         = art_url(song_artist, song_album, song_title)
                albumart    = curl(art)
                if albumart:
                    # If we got album art out of that, we're going to write it out
                    f = open("/tmp/_amp_icon", "w")
                    f.write(albumart)
                    f.close()
                    # We then need to ensure it's a PNG (libnotify limitations, etc.)
                    os.system("convert /tmp/_amp_icon /tmp/_amp_icon.png")
                    # We don't really care about the old tmp file, it will get replaced
                    # the next time a new song plays anyway...
                    icon_path = "file:///tmp/_amp_icon.png"
                else:
                    # Otherwise, use the fallback (album art API command failed miserably)
                    icon_path = fallback
                # Create the notification bubble
                notify = pynotify.Notification(song_title, "<br />".join([song_artist,song_album]), icon_path)
                # And display it
                notify.show()
        else:
            # Otherwise, nothing is playing.
            if last_result != 0:
                print "Nothing playing.\n"
                last_result = 0
        # Reset the number of failed attempts.
        attempts = 1
    except:
        # An exception is probably a failed connection or something to that effect
        print "Failed to connect or retrieve stuff, attempt",attempts
        # Up the failure count
        attempts += 1
        if attempts > 10:
            # If the failure count is too high, give up and bail.
            print "Failed to get information after ten attempts. Good bye."
            sys.exit(1)
    # Wait to poll again
    time.sleep(sleep_time)
