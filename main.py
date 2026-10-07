import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic


time = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = "https://appbrewery.github.io/bakeboard-hot-100/" + f"{time}/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"}
response = requests.get(url=URL, headers=headers).text

soup = BeautifulSoup(response, "html.parser")

title_song = soup.find_all(name="h3", class_="chart-entry__title")
all_titles = [title.getText() for title in title_song]

ytmusic = YTMusic("browser.json")
title = f"{time} Billboard 100"
descriptions = "The OG Playlist"

playlists = ytmusic.get_library_playlists(limit=100)
playlist_id = None

for p in playlists:
    if p["title"] == title:
        playlist_id = p["playlist_id"]
        break

if playlist_id:
    print("This playlist is already exist.")
else:
    playlist_id = ytmusic.create_playlist(title, descriptions, privacy_status="PRIVATE")
    print("Playlist created successfully.")

for song in all_titles:
    try:
        result = ytmusic.search(song ,filter="songs", limit=1)
        ytmusic.add_playlist_items(playlist_id, [result[0]["videoId"]])
        print(f"Added {song}")
    except Exception as e:
        print(f"Skipping {song} | Reason: {e}")





