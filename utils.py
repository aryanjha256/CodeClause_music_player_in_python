import os


def get_songs(directory):
    songs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Only added mp3 and flac files but can be extended to other formats
            if file.endswith('.mp3') or file.endswith('.flac'):
                songs.append(os.path.join(root, file))
    return songs
