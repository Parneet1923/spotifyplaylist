import spotipy
from spotipy import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import os
from pprint import pprint


YOUR_ID = os.environ.get('YOUR_ID')
YOUR_KEY = os.environ.get('YOUR_SECRET')
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url = "https://www.billboard.com/charts/hot-100/"
link = url + date

response = requests.get(url=link)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
list = soup.find_all(name="h3", id="title-of-a-story", class_="lrv-u-font-size-16")
song_names = [song.getText().strip("\n\t") for song in list[:100]]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=YOUR_ID,
                                               client_secret=YOUR_KEY,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()['id']
uri = []
for song in song_names:
    try:
        result = sp.search(q=song, type="track", limit=1)
        uri.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{song} does not exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} 100 songs",
                                   description=f"Top 100 songs on {date}", public=False)

playlist_id = playlist['id']

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=uri)
print(f"Check your spotify. Top 100 Songs of the {date} has been added in a playlist. ")
