# Python Spotify Playlist List Generator
import re, os
from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import spotipy
import spotipy.oauth2 as oauth2
from tabulate import tabulate
# Import Developer ID and SECRET
from local_spotify_dev_account import *

# Gather Local Path
cwd = str(os.getcwd())

# Function to Perform Folder Browsing Operation
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    if filename != '':
        folder_path.set(filename)

# Function to Extract Playlist URI from URL
def gather_playlist_uri(playlist_url):
    result = re.search('playlist/(.*)\?si=', playlist_url)
    try:
        playlist_uri = result.group(1)
    except:
        playlist_uri = ''
    return(playlist_uri)

# Function to Generate Spotify API Token
def generate_token():
    """ Generate the token. Please respect these credentials :) """
    credentials = oauth2.SpotifyClientCredentials(
        client_id=joestanid,
        client_secret=joestansecret)
    token = credentials.get_access_token()
    return token

# Initialize Token and Spotify
token = generate_token()
spotify = spotipy.Spotify(auth=token)

# Function to Store Playlist Information in Text File
def write_tracks(text_file, tracks):
    text_file = os.path.join(folder_path.get(), text_file) # Use Full File Path
    with open(text_file, 'w', encoding="utf-8") as file_out:
        # Write Text File Name
        file_out.write(text_file + '\n\n')
        # Write Playlist Header Information
        headers = ["Title","Artist(s)","Explicit"]
        tracklist = []
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
                    track_explicit = 'Yes' if track['explicit'] else '--'
                    # Append Track Information to List
                    tracklist.append([track_name, track_artists, track_explicit])
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break
        file_out.write(tabulate(tracklist, headers, tablefmt="simple"))

# Main Playlist Collection Function
def write_playlist(playlist_id):
    global spotify
    username = 'NA' # Username Doesn't Matter
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = results['name'] + '.txt'
    text_file = text_file.replace(' ','_').replace('\\','').replace('/','')
    text_file = text_file.replace('?','').replace(':','-').replace('|','-')
    labelvar.set(u'Wrote {0} tracks to {1}'.format(
                 results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)



# Generate Playlist File
def generate():
    # Generate Token and Authenticate Spotify API Access
    global token, spotify
    token = generate_token()
    spotify = spotipy.Spotify(auth=token)
    # Gather User-Specified URL
    url = urlvar.get()
    if url == '':
        labelvar.set('Invalid URL')
        return
    uri = gather_playlist_uri( url )
    # Write Playlist Information
    write_playlist( uri )

# Generate Root Window
root = Tk()
root.geometry("800x350") # Force Size
root.resizable(0,0) # Deny Resizing
root.iconbitmap(cwd+'/spotify_icon.ico')
root.title("Spotify Playlister")
root.configure(background='black')
# Generate String Vars
labelvar = StringVar()
urlvar = StringVar()
folder_path = StringVar()
# Configure Frames
top = Frame(root,height=20,bd=0,bg='black')
top.pack(side=TOP)
body = Frame(root,bg='black')
body.pack(side=TOP)
urlent = Frame(body,height=20,bd=10,bg='black',width=500)
urlent.pack(side=BOTTOM)
stor = Frame(body,height=20,bd=10,bg='black',width=500)
stor.pack(side=BOTTOM)
# Configure Items
calibri16 = Font(family='Calibri', size=16)
calibri12 = Font(family='Calibri', size=12)
calibri10 = Font(family='Calibri', size=10)
labelvar.set('Welcome to the Spotify Playlister')
folder_path.set(cwd+'\\Playlists')
lab = Label(body, textvariable=labelvar, fg='white', bg='black')
lab.configure(font=calibri16)
lab.pack()
dirlab = Label(stor,text='\nPlaylist Storage Directory:',font=calibri12,fg='white',bg='black')
dirlab.pack(side=TOP)
direntry = Entry(stor, width=350,bg='gray20',textvariable=folder_path,bd=0,fg='white',
                 selectbackground='black',selectforeground='white',highlightcolor=
                 'gray65',insertbackground='white',font=calibri12)
dirbut = Button(stor,text="Browse",bg="#1DB954",fg='white',command=browse_button,
                height=1,bd=0,activebackground='gray65',activeforeground='black',
                font=calibri10,highlightcolor='gray20',pady=0)
dirbut.pack(side=RIGHT)
direntry.pack()
urllab = Label(urlent,text='\nPlaylist URL:',font=calibri12,fg='white',bg='black')
urllab.pack(side=TOP)
urlentry = Entry(urlent, width=350,bg='gray20',textvariable=urlvar,bd=0,fg='white',
                 selectbackground='black',selectforeground='white',highlightcolor=
                 'gray65',insertbackground='white',font=calibri12)
urlentry.pack()
runbut = Button(urlent,text="Generate",bg="#1DB954",fg='white',command=generate,
                height=1,bd=0,activebackground='gray65',activeforeground='black',
                font=calibri16,highlightcolor='gray20',pady=0)
runbut.pack(side=BOTTOM)
foo = Label(urlent,text='\n\nGenerate Playlist:',font=calibri12,fg='white',bg='black')
foo.pack(side=BOTTOM)

# Run Tkinter GUI
root.mainloop()
