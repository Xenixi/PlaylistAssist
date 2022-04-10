import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import keyboard as keyboard
import os.path
import configparser


def main():
    # Setup Spotify connection
    scope = "user-read-currently-playing, user-library-read, user-library-modify, playlist-read-private, playlist-modify-private, playlist-modify-public"
    client_id = "95609027f8414070a6854d114173ddd5"
    client_secret = "dc92f50f182648a88ee87a03267ffcac"
    redirect_uri = "http://www.google.com/"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
    
    # Read user configs

    if not os.path.exists("README.md"):
        f = open("README.md", 'w')
        f.write("Welcome to PlaylistAssist. Set your hotkeys in hotkeys.config.")

    hk_cf = configparser.ConfigParser()

    if not os.path.exists("hotkeys.config"): 
        hk_cf.add_section("MAIN")
        hk_cf["MAIN"]["song-to-playlist"] = "f9"
        hk_cf["MAIN"]["song-to-liked"] = "f10"
        hk_cf["MAIN"]["remove-from-current-playlist"] = "ctrl+shift+f9"
        hk_cf["MAIN"]["remove-from-liked"] = "ctrl+shift+f10"
        with open("hotkeys.config", 'w') as f:
            hk_cf.write(f)

    hk_cf.read("hotkeys.config")

    
    # The good stuff
   
    keyboard.add_hotkey(hk_cf["MAIN"]["song-to-liked"], lambda: song_to_liked(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["song-to-playlist"],lambda: song_to_playlist(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["remove-from-liked"],lambda: song_remove_liked(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["remove-from-current-playlist"],lambda: song_remove_playlist(sp=sp))
    

    keyboard.wait()
  

def song_to_liked(sp):
    track = sp.current_user_playing_track()
    print("Adding current song to liked songs...\'" + track["item"]["name"])
    #sp.current_user_saved_tracks_add(track)
def song_to_playlist(sp):
    print("Adding current song to specified playlist...")
def song_remove_liked(sp):
    print("Removing current song from your liked songs...")
def song_remove_playlist(sp):
    print("Removing current song from your playlist...")


main()
