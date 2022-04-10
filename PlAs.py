import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import keyboard as keyboard
import os.path
import configparser
import chime as chime


def main():
    # Setup Spotify connection
    scope = "user-read-currently-playing, user-library-read, user-library-modify, playlist-read-private, playlist-modify-private, playlist-modify-public"
    client_id = "95609027f8414070a6854d114173ddd5"
    client_secret = "dc92f50f182648a88ee87a03267ffcac"
    redirect_uri = "http://www.google.com/"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

    # Read user configs

    if not os.path.exists("README.md"):
        f = open("README.md", 'w')
        f.write("Welcome to PlaylistAssist. Set your hotkeys in hotkeys.config.")

    hk_cf = configparser.ConfigParser()

    if not os.path.exists("hotkeys.config"):
        hk_cf.add_section("MAIN")
        hk_cf["MAIN"]["song-to-playlist"] = "f10"
        hk_cf["MAIN"]["song-to-liked"] = "f9"
        hk_cf["MAIN"]["remove-from-current-playlist"] = "ctrl+shift+f10"
        hk_cf["MAIN"]["remove-from-liked"] = "ctrl+shift+f9"
        hk_cf["MAIN"]["set-active-playlist"] = "alt+f7"
        with open("hotkeys.config", 'w') as f:
            hk_cf.write(f)

    hk_cf.read("hotkeys.config")

    # The good stuff

    keyboard.add_hotkey(hk_cf["MAIN"]["song-to-liked"],
                        lambda: song_to_liked(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["song-to-playlist"],
                        lambda: song_to_playlist(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["remove-from-liked"],
                        lambda: song_remove_liked(sp=sp))
    keyboard.add_hotkey(
        hk_cf["MAIN"]["remove-from-current-playlist"], lambda: song_remove_playlist(sp=sp))
    keyboard.add_hotkey(hk_cf["MAIN"]["set-active-playlist"],
                        lambda: set_active_playlist(sp=sp))

    chime.theme('zelda')
    chime.info()
    print("Ready.")
    keyboard.wait()


def song_to_liked(sp):
    try:
        track = sp.current_user_playing_track()
        print("Adding current song to liked songs...\'" +
              track["item"]["name"] + "'")
        sp.current_user_saved_tracks_add(tracks=[track['item']['id']])
        chime.theme('mario')
        chime.success()
    except Exception as e:
        print("Error occurred while processing request.")


def song_to_playlist(sp):
    try:

        track = sp.current_user_playing_track()
        f = open("selected-playlist.store", 'r')
        playlist_id = f.readline()
        f.close()
        print("Adding current song to specified playlist...\'" +
              track["item"]["name"] + "' to playlist \'" + playlist_id + "\'")

        sp.playlist_add_items(playlist_id, items=[track['item']['id']])

        chime.theme('mario')
        chime.success()
    except Exception as e:
        print("Error while adding track to playlist... Do you own the playlist?")


def song_remove_liked(sp):
    try:
        track = sp.current_user_playing_track()
        print("Removing current song from your liked songs...\'" +
              track["item"]["name"] + "'")
        sp.current_user_saved_tracks_delete(tracks=[track['item']['id']])
        chime.theme('zelda')
        chime.warning()
    except Exception as e:
        print("Error occurred while processing request.")


def song_remove_playlist(sp):

    track = sp.current_user_playing_track()
    playlist_id = track['context']['uri']

    print("Removing current song from your currently playing playlist... \'" +
          track['item']['name'] + "\' from playlist \'" + playlist_id + "\'")

    sp.playlist_remove_all_occurrences_of_items(
        playlist_id, items=[track['item']['id']])

    chime.theme('zelda')
    chime.warning()


def set_active_playlist(sp):
    track = sp.current_user_playing_track()
    playlist = track['context']['uri']

    # should add something to verify playlists are owned by user to avoid confusion

    with open("selected-playlist.store", 'w') as f:
        f.write(playlist)
    print("Setting active playlist to \'" + playlist + "\'")

    chime.theme('mario')
    chime.info()


main()
