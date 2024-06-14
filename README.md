# Spotify to YouTube Audio Downloader

This script fetches tracks from your Spotify playlists, searches for the corresponding YouTube videos, and downloads the audio from these videos.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- `requests` library installed
- `pytube` library installed
- `pillow` library installed
- `tkinter` library installed
- A valid Spotify OAuth token
- A valid YouTube Data API key

You can install the required libraries using pip:

`---bash
~# pip install requests pytube pillow tkinter`

Try using your own API key and spotify IDs as it will lessen the load on our current API keys
The links are provided below containing the information on how to create your own API keys and spotify `CLIENT-ID` and `CLIENT-SECRET`

# Spotify to YouTube Audio Downloader

To use the downloader, run the `main.py` file.

## About the Code

- **Spotify API**: Used to retrieve the playlist data. You need to log in to the Spotify Developer Dashboard to get the necessary access codes.
- **YouTube API**: Used to search for the songs. Be aware of the free tier document as it has a daily limit on requests.
- **pytube**: Used for downloading the audio from YouTube videos.
- **tkinter**: Used for building the graphical user interface (GUI). It's the standard Python interface to the Tk GUI toolkit.
- **Pillow**: Used for handling images. It's a powerful Python library for image processing tasks.

> **Note:** Ensure that you have the required API keys and tokens before running the script.


## Links of Documentations

- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Pytube Documentation](https://pytube.io/en/latest/)
- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)

### Hope this helps!

