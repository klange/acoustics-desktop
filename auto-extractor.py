#!/usr/bin/env python
import simplejson, pycurl
import sys, urllib, time, os, getopt

from extract_art import extractArt

# Reload `sys` so we can get at the default encoding and set it
# to unicode (utf-8) so that foreign song titles, etc. work.
reload(sys)
sys.setdefaultencoding("utf-8")

# The URL of the acoustics instance
amp_url    = "https://www-s.acm.uiuc.edu/acoustics/json.pl"
room       = ""
no_loop    = False

# Argument parsing
try:
    opts, args = getopt.getopt(sys.argv[1:], "s:r:n", ["server=", "room=", "no-loop"])
except getopt.GetoptError, err:
    print str(err)
    sys.exit(1)
for o, a in opts:
    if o in ("-s", "--server"):
        amp_url = a + "/json.pl"
    if o in ("-r", "--room"):
        room = a
    if o in ("-n", "--no-loop"):
        no_loop = True

def getPath(additional):
    if len(room) > 0:
        return amp_url + "?player_id=" + room + ";" + additional
    else:
        return amp_url + "?" + additional

# Time to sleep between polls
sleep_time = 5

def curl(url):
    """ Retreive the contents of the requested url"""
    f = urllib.urlopen(url)
    x = f.read()
    f.close()
    return x

# The contents of our last poll
last_result = -1

# Count the number of failed attempts.
attempts = 1

while 1:
    try:
        # Retreive the JSON from the API
        acoustics = simplejson.loads(curl(getPath("")))
        # Check that a song is playing
        if acoustics['now_playing']:
            # If so, check if this isn't the same data as the last time we polled
            if not acoustics['now_playing']['song_id'] == last_result:
                # And if it isn't, build a notification bubble.
                extractArt(acoustics['now_playing']['path'])
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
    if no_loop:
        sys.exit(0)
    # Wait to poll again
    time.sleep(sleep_time)
