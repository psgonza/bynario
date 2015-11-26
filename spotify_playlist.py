#/usr/bin/env python
# Getting track details from a list of Spotify URLs via spotify API
# Input file containing the list of URLs mandatory
# Date: 26 Nov 2015

import json, urllib2, sys
from time import sleep

#Checking input file
if len(sys.argv) != 2:
    print("Error: Input file mandatory")
    sys.exit(0)
else:
    input_file = sys.argv[1]

#Spotify track API
api_url = "https://api.spotify.com/v1/tracks/"

#track dictionary
mytracks = []

#Open input file
try:
    fd = open(input_file,"r")
except Exception as e:
    print("Error opening %s" % input_file)
    print(e)
    sys.exit(0)

#getting track details from uri
def get_track_data(url):

    request = urllib2.Request(api_url + url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    request.add_header('Content-Type','application/json')

    try:
        response = urllib2.urlopen(request)
    except Exception as e:
        print("\nError connecting to spotify API looking details for uri %s" % url)
        return False

    try:
        data = json.load(response)
    except Exception as e:
        print("\nError handling json object looking details for uri %s" % url)
        return False

    try:
        mytracks.append({'album':str(data['album']['name']),'artist':str(data['artists'][0]['name']),'track':str(data['name'])})
        sys.stdout.write(".")
        sys.stdout.flush()
    except Exception as e:
        print("Error getting details for uri %s" % url)
        return False

########
# MAIN #
########

sys.stdout.write("Iterating through tracks in " + input_file)
sys.stdout.flush()

#Calling to get_track_data for each uri in the input file
for track in fd:
    get_track_data(track.split(":")[2])
    #I don't need to DDoS spotify servers :)
    sleep(2)
print("done!")

#Printing the header when the dict has been populated
print("\nArtist - Album - Track")
print("----------------------")

#Printing the results. By default, ordered by 'artist', but it can be ordered by 'album' or 'track'
for track in sorted(mytracks,key=lambda k: k['artist']):
    print("%s - %s - %s" % (track['artist'],track['album'],track['track']))

#close input file
fd.close()
