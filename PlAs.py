import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import keyboard as keyboard
import os
import os.path
import configparser
import chime as chime
import datetime
import sys
import time


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
        f.write("Welcome to PlaylistAssist by Kobe McManus (github.com/xenixi). Set your hotkeys in hotkeys.config.\n\nctrl+shift+f1 exits. | ctrl+shift+f2 exits and starts new console process | Use f7 to see if PlaylistAssist is running in background\n\nFIRST TIME USERS:\nRun setup.exe to install Python (if needed) & Python packages.\nRun normal launch first to authenticate w/ Spotify before using background launch.\n\nFunctionality:\n    song-to-liked - adds currently playing song to your liked songs\n    remove-from-liked - removes currently playing song from your liked songs\n\n    set-active-playlist - sets currently playing playlist as the active playlist for addition of songs with song-to-playlist\n    (Must be playing the playlist you want to set active at time of hotkey press)\n\n    song-to-playlist - adds currently playing song to the active playlist (set by set-active-playlist)\n    remove-from-current-playlist - removes currently playing song from currently playing playlist (not necessarily the active playlist!)")

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

    #using or operator to include multiple statements in lambda 
    keyboard.add_hotkey("ctrl+shift+f1", lambda: print("Python process terminated. You may close this window now.") or os.system('start cmd.exe /k \"echo PlaylistAssist Background Process Closed && pause && exit\"') or sys.exit())
    keyboard.add_hotkey("ctrl+shift+f2", lambda: print("Python process terminated. New process spawned in console mode.") or os.system('start cmd.exe /k \"launch.exe\"') or sys.exit())
    keyboard.add_hotkey("f7", lambda: (chime.theme('mario') or chime.info()))

    chime.theme('zelda')
    chime.info()
    print("Ready.")
    with open("PlAs.log", 'a') as log:
        log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                  + "Ready.")
    keyboard.wait()


def song_to_liked(sp):
    try:
        track = sp.current_user_playing_track()

        print("Adding current song to liked songs...\'" +
              track["item"]["name"] + "'")

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Adding current song to liked songs...\'" +
                      track["item"]["name"] + "'")

        sp.current_user_saved_tracks_add(tracks=[track['item']['id']])
        chime.theme('mario')
        chime.success()
    except Exception as e:
        print("Error occurred while processing request.")
        chime.theme('mario')
        chime.warning()
        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Error occurred while processing request. (song_to_liked)")


def song_to_playlist(sp):
    try:

        track = sp.current_user_playing_track()
        f = open("selected-playlist.store", 'r')
        playlist_id = f.readline()
        f.close()

        print("Adding current song to specified playlist...\'" +
              track["item"]["name"] + "' to playlist \'" + playlist_id + "\'")

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Adding current song to specified playlist...\'" +
                      track["item"]["name"] + "' to playlist \'" + playlist_id + "\'")

        sp.playlist_add_items(playlist_id, items=[track['item']['id']])

        chime.theme('mario')
        chime.success()
    except Exception as e:
        print("Error while adding track to playlist... Do you own the playlist?")
        chime.theme('mario')
        chime.warning()
        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Error while adding track to playlist... Do you own the playlist? (song_to_playlist)")


def song_remove_liked(sp):
    try:
        track = sp.current_user_playing_track()
        print("Removing current song from your liked songs...\'" +
              track["item"]["name"] + "'")

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Removing current song from your liked songs...\'" +
                      track["item"]["name"] + "'")

        sp.current_user_saved_tracks_delete(tracks=[track['item']['id']])
        chime.theme('zelda')
        chime.warning()
    except Exception as e:
        print("Error occurred while processing request.")
        chime.theme('mario')
        chime.warning()
        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Error occurred while processing request. (song_remove_liked)")


def song_remove_playlist(sp):
    try:
        track = sp.current_user_playing_track()
        playlist_id = track['context']['uri']

        print("Removing current song from your currently playing playlist... \'" +
            track['item']['name'] + "\' from playlist \'" + playlist_id + "\'")

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                    + "Removing current song from your currently playing playlist... \'" +
                    track['item']['name'] + "\' from playlist \'" + playlist_id + "\'")

        sp.playlist_remove_all_occurrences_of_items(
            playlist_id, items=[track['item']['id']])

        chime.theme('zelda')
        chime.warning()
    except Exception as e:
        print("Error occurred while processing request. (song_remove_playlist)")
        chime.theme('mario')
        chime.warning()
        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Error occurred while processing request.")


def set_active_playlist(sp):
    try:
        track = sp.current_user_playing_track()
        playlist = track['context']['uri']

        # should add something to verify playlists are owned by user to avoid confusion

        with open("selected-playlist.store", 'w') as f:
            f.write(playlist)
        print("Setting active playlist to \'" + playlist + "\'")

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                    + "Setting active playlist to \'" + playlist + "\'")

        chime.theme('mario')
        chime.info()
    except Exception as e:
        print("Error occurred while processing request. Make sure spotify is playing!")
        #print(e)
        chime.theme('mario')
        chime.warning()

        with open("PlAs.log", 'a') as log:
            log.write("\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " "
                      + "Error occurred while processing request. (set_active_playlist)")

main()
