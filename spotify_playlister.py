# Python Spotify Playlist List Generator
import re, os
from tkinter import *
import spotipy
import spotipy.oauth2 as oauth2
# Import Developer ID and SECRET
from local_spotify_dev_account import *

# Gather Local Path
cwd = str(os.getcwd())

# Generate Root Window
root = Tk()
root.iconbitmap(cwd+'/spotify_icon.ico')

# Function to Extract Playlist URI from URL
def gather_playlist_uri(playlist_url):
    result = re.search('playlist/(.*)\?si=', playlist_url)
    try:
        playlist_uri = result.group(1)
    except:
        playlist_uri = ''
    print("Playlist URI:",playlist_uri)
    return(playlist_uri)

# Function to Generate Spotify API Token
def generate_token():
    """ Generate the token. Please respect these credentials :) """
    credentials = oauth2.SpotifyClientCredentials(
        client_id=joestanid,
        client_secret=joestansecret)
    token = credentials.get_access_token()
    return token


# Function to Store Playlist Information in Text File
def write_tracks(text_file, tracks):
    with open(text_file, 'w') as file_out:
        # Write Text File Name
        file_out.write(text_file + '\n\n')
        # Write Playlist Header Information
        file_out.write("Title\t-\tArtist(s)\t-\tExplicit\n\n")
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    # Gather Pertinent Track Information
                    track_name = track['name']
                    track_artists = ""
                    cnt = 0
                    # Gather all Track Artists as Comma-Delimited String
                    for artist in track['artists']:
                        if cnt != 0:
                            track_artists += ', '
                        track_artists += artist['name']
                        cnt += 1
                    # Validate Track Explicit Indicator
                    track_explicit = str(track['explicit'])
                    # Write File
                    file_out.write(track_name + ' - ' + track_artists
                                   + ' - ' + track_explicit + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break

# Main Playlist Collection Function
def write_playlist(username, playlist_id):
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = results['name'] + '.txt'
    text_file = text_file.replace(' ','_').replace('\\','').replace('/','')
    text_file = text_file.replace('?','').replace(':','-').replace('|','-')
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)

# Generate Token and Authenticate Spotify API Access
token = generate_token()
spotify = spotipy.Spotify(auth=token)

# example playlist
playlist_url = 'https://open.spotify.com/playlist/7IUZbpWEJOjt4zzlBV1Lcp?si=RID45hU8TxicorsOV0p1Rw&fbclid=IwAR3kVz8TuWFBPKIq-oa9IOL33nFuiehNVmnGlw54Y0j5zry4OZppZYz89F0'
#write_playlist('NA', gather_playlist_uri(playlist_url))

# Run Tkinter GUI
root.mainloop()
