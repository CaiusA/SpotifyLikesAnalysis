from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Load environment variables
load_dotenv()


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=['user-library-read']))

def addTracks(lib, library):
    for track in library['items']:
        lib['Song Added At'].append(track['added_at'])
        lib['Song Name'].append(track['track']['name'])
        lib['Artist'].append(track['track']['artists'][0]['name'])
        lib['Album'].append(track['track']['album']['name'])
        lib['Album Type'].append(track['track']['album']['album_type'])
        lib['Release Date'].append(track['track']['album']['release_date'])
        lib['Explicit'].append(track['track']['explicit'])

# call api to get total songs in Liked Songs
sample = sp.current_user_saved_tracks(limit=1)
total = sample['total']

# maximum track limit
max = 50
next = 0

info = {'Song Added At': [], 'Song Name': [], 'Artist': [], 'Album': [],
        'Album Type': [], 'Release Date': [], 'Explicit': []}

# grab all liked songs
while len(info['Song Added At']) < total:
    library = sp.current_user_saved_tracks(limit=max, offset=next)
    addTracks(info, library)
    next += max

# export to csv
df = pd.DataFrame(info)
df.to_csv('spotify_liked_tracks.csv')








