import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from spotify import fetch_playlist_info
import spotify_api.refresh_token as refresh_token
from PIL import Image, ImageTk
import threading
import requests
from pytube import YouTube


# Constants
YOUTUBE_API_KEYS = [
    "AIzaSyBTnea2CG-5BMShYTQldLlbhnEW6xfNJHs",
    "AIzaSyDT0TBlMNtzv-NfkB20PfrAxQ9wz2MQmvY",
    "AIzaSyD24-nGJlYZzy-hgG746XZcRVfprUdNXyk",
    "AIzaSyAsnsXx4oeGrWQcVKusU9j8et0VKTzbpQk",
    "AIzaSyCIWRWVdn6sl46jwGCoqaHxTWXs4GGtc7Q"
]
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

class SpotifyDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spotify Playlist Downloader")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        # Load and set the background image
        self.bg_image = Image.open("background.jpg")  # Ensure you have a background.jpg in your directory
        self.bg_image = self.bg_image.resize((600, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Title Label
        self.title_label = tk.Label(self, text="Spotify Playlist Downloader", font=("Helvetica", 20, "bold"), bg="#000000", fg="#ffffff")
        self.title_label.pack(pady=20)

        # Playlist Link Label
        self.playlist_link_label = tk.Label(self, text="Enter Spotify Playlist Link:", font=("Helvetica", 14), bg="#000000", fg="#ffffff")
        self.playlist_link_label.pack(pady=10)

        # Playlist Link Entry
        self.playlist_link_entry = tk.Entry(self, width=50, font=("Helvetica", 12), bg="#ffffff", fg="#000000")
        self.playlist_link_entry.pack(pady=5)

        # Download Button
        self.download_button = tk.Button(self, text="Download Playlist", font=("Helvetica", 14, "bold"), bg="#1DB954", fg="#ffffff", command=self.start_download)
        self.download_button.pack(pady=20)

        # Status Text
        self.status_text = ScrolledText(self, width=70, height=10, font=("Helvetica", 10), bg="#000000", fg="#ffffff", state=tk.DISABLED)
        self.status_text.pack(pady=10)

    def start_download(self):
        # Disable button and entry during download
        self.download_button.config(state=tk.DISABLED)
        self.playlist_link_entry.config(state=tk.DISABLED)

        # Start download in a separate thread to prevent UI freeze
        threading.Thread(target=self.download_playlist).start()

    def download_playlist(self):
        playlist_link = self.playlist_link_entry.get()
        if not playlist_link:
            messagebox.showerror("Error", "Playlist link is required!")
            self.reset_ui()
            return

        token = "dummy_text"  # Initial dummy token
        token, playlist_id, track_names = fetch_playlist_info(token, playlist_link)

        if not track_names:
            messagebox.showerror("Error", "Failed to get playlist or tracks.")
            self.reset_ui()
            return

        # Get artist names associated with the tracks in the playlist
        artists = refresh_token.get_artists_from_playlist(playlist_id)

        # Custom search and download function to update status text
        for i, track_name in enumerate(track_names):
            self.update_status(f"Searching YouTube for: {track_name}")
            video_id = None
            for api_key in YOUTUBE_API_KEYS:
                yt_res = requests.get(YOUTUBE_SEARCH_URL, params={
                    "key": api_key,
                    "q": f"{track_name} {artists[i]} song",
                    "type": "video"
                })
                if yt_res.status_code == 200:
                    yt_js = yt_res.json()
                    if yt_js["items"]:
                        video_id = yt_js["items"][0]["id"]["videoId"]
                        break
                else:
                    self.update_status(f"YouTube API quota exceeded for key: {api_key}")
                    continue
            else:
                self.update_status(f"Failed to find a video for: {track_name}")
                continue

            # Download the video from YouTube
            self.update_status(f"Download started for: {track_name}")
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            try:
                res = yt.streams.filter(only_audio=True, abr="128kbps")
                if res:
                    stream = res[0]
                    output_path = f"./downloads/{refresh_token.get_playlist_name(playlist_id)}"
                    stream.download(output_path=output_path)
                    self.update_status(f"Downloaded {track_name} to {output_path}")
                else:
                    self.update_status(f"No suitable stream found for {track_name}")
            except Exception as e:
                self.update_status(f"Failed to download {track_name}: {e}")
                # Attempt to download an alternative video if the first one fails
                video_id = yt_js["items"][1]["id"]["videoId"]
                yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
                res = yt.streams.filter(only_audio=True, abr="128kbps")
                if res:
                    stream = res[0]
                    output_path = f"./downloads/{refresh_token.get_playlist_name(playlist_id)}"
                    stream.download(output_path=output_path)
                    self.update_status(f"Downloaded {track_name} to {output_path}")
                else:
                    self.update_status(f"No suitable stream found for {track_name}")

        self.update_status("Download completed!")
        self.reset_ui()

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def reset_ui(self):
        # Enable button and entry after download
        self.download_button.config(state=tk.NORMAL)
        self.playlist_link_entry.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = SpotifyDownloaderApp()
    app.mainloop()
