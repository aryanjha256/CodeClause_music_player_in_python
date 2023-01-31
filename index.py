from utils import get_songs
import pygame
import os
import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment


pygame.init()
pygame.mixer.init()


# Create a list of songs
songs = get_songs("./audios/")

# Set the current_song to the first_song
current_song = 0

# Create the main window
root = tk.Tk()
root.geometry("800x600")
root.title("Music Player")

# Create a label to display the song title
song_title_var = tk.StringVar()
song_title_var.set("Select a song to play")
song_title_label = ttk.Label(root, textvariable=song_title_var)
song_title_label.pack()

# Create a label to display the time elapsed and remaining
time_var = tk.StringVar()
time_var.set("00:00 / 00:00")
time_label = ttk.Label(root, textvariable=time_var)
time_label.pack()

# Create a listbox to display the available songs
song_listbox = tk.Listbox(root)
song_listbox.pack()

for song in songs:
    song_listbox.insert(tk.END, os.path.basename(song))

# Create a play button
play_button = ttk.Button(
    root, text="Play", command=lambda current_song=current_song: play_song(current_song))
play_button.pack()

# Create a pause button
pause_button = ttk.Button(root, text="Pause", command=lambda: pause_song())
pause_button.pack()

# Create a stop button
stop_button = ttk.Button(root, text="Stop", command=lambda: stop_song())
stop_button.pack()

# Create a next button
next_button = ttk.Button(root, text="Next", command=lambda: next_song())
next_button.pack()

# Create a previous button
previous_button = ttk.Button(
    root, text="Previous", command=lambda: previous_song())
previous_button.pack()


def get_duration(filepath):
    audio = AudioSegment.from_file(filepath)
    return int(audio.duration_seconds)


# Function to update the time label


def update_time(total_time):
    elapsed_time = pygame.mixer.music.get_pos()/1000
    remaining_time = total_time - elapsed_time
    time_var.set(seconds_to_time(elapsed_time) +
                 " / " + seconds_to_time(remaining_time))
    if pygame.mixer.music.get_busy():
        root.after(1000, update_time, total_time)

# Function to play a song


def play_song(song_index):
    global current_song
    current_song = song_index
    pygame.mixer.music.load(songs[current_song])
    pygame.mixer.music.play()
    song_title_var.set(os.path.basename(songs[current_song]))
    total_time = get_duration(songs[current_song])
    update_time(total_time)

# Function to pause a song


def pause_song():
    pygame.mixer.music.pause()

# Function to stop a song


def stop_song():
    pygame.mixer.music.stop()
    time_var.set("00:00 / 00:00")

# Function to play the next song


def next_song():
    global current_song
    if current_song + 1 >= len(songs):
        current_song = 0
    else:
        current_song += 1
    play_song(current_song)

# Function to play the previoussong


def previous_song():
    global current_song
    if current_song - 1 < 0:
        current_song = len(songs) - 1
    else:
        current_song -= 1
    play_song(current_song)


# Function to convert seconds to time format (mm:ss)


def seconds_to_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return "{:02.0f}:{:02.0f}".format(minutes, seconds)


# Bind the double click event to the listbox
song_listbox.bind("<Double-Button-1>",
                  lambda event: play_song(song_listbox.curselection()[0]))

root.mainloop()
