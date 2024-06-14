import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import spotify_api.refresh_token as refresh_token
from pytube import YouTube

# Constants
SPOTIFY_API_URL = "https://api.spotify.com/v1"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_API_KEYS = [
    "AIzaSyBTnea2CG-5BMShYTQldLlbhnEW6xfNJHs",
    "AIzaSyDT0TBlMNtzv-NfkB20PfrAxQ9wz2MQmvY",
    "AIzaSyD24-nGJlYZzy-hgG746XZcRVfprUdNXyk",
    "AIzaSyAsnsXx4oeGrWQcVKusU9j8et0VKTzbpQk",
    "AIzaSyCIWRWVdn6sl46jwGCoqaHxTWXs4GGtc7Q"
]

# Function to get user's playlists from Spotify
def get_playlists(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{SPOTIFY_API_URL}/me/playlists", headers=headers)
    return res

# Function to get tracks from a specific Spotify playlist
def get_tracks(token, playlist_id):
    headers = {"Authorization": f"Bearer {token}"}
    link = f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks"
    res = requests.get(link, headers=headers)
    return res

# Main function to fetch playlist and track information
def fetch_playlist_info(token, playlist_link):
    res = get_playlists(token)
    if res.status_code == 401:
        # Refresh the token if expired
        print("\nCreating token...")
        token = refresh_token.re_to()
        res = get_playlists(token)

    if res.status_code != 200:
        print("Failed to get playlists:", res.status_code, res.text)
        return token, "", []

    id_pos = playlist_link.find("playlist") + 9
    q_pos = playlist_link.find('?')
    playlist_id = playlist_link[id_pos:q_pos if q_pos > 9 else len(playlist_link)]
    print("Playlist ID:", playlist_id)

    # Fetch tracks from the playlist
    tracks_res = get_tracks(token, playlist_id)
    if tracks_res.status_code != 200:
        print("Failed to get tracks:", tracks_res.status_code, tracks_res.text)
        return token, playlist_id, []

    tracks = tracks_res.json()
    track_names = [item["track"]["name"] for item in tracks["items"]]

    if not track_names:
        print("No tracks available")
    else:
        for i, name in enumerate(track_names):
            print(i, name)

    return token, playlist_id, track_names

# Function to search YouTube for the tracks and download videos
def search_and_download_videos(track_names, artists, playlist_id):
    for i, track_name in enumerate(track_names):
        video_id = None
        # Iterate over YouTube API keys to avoid quota issues
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
                print("YouTube API quota exceeded for key:", api_key)
                continue
        else:
            print("Failed to find a video for:", track_name)
            continue

        # Download the video from YouTube
        print("Download started for:", track_name)
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        try:
            res = yt.streams.filter(only_audio=True, abr="128kbps")
            if res:
                stream = res[0]
                output_path = f"./downloads/{refresh_token.get_playlist_name(playlist_id)}"
                stream.download(output_path=output_path)
                print(f"Downloaded {track_name} to {output_path}")
            else:
                print(f"No suitable stream found for {track_name}")
        except Exception as e:
            print(f"Failed to download {track_name}: {e}")
            # Attempt to download an alternative video if the first one fails
            video_id = yt_js["items"][1]["id"]["videoId"]
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            res = yt.streams.filter(only_audio=True, abr="128kbps")
            if res:
                stream = res[0]
                output_path = f"./downloads/{refresh_token.get_playlist_name(playlist_id)}"
                stream.download(output_path=output_path)
                print(f"Downloaded {track_name} to {output_path}")
            else:
                print(f"No suitable stream found for {track_name}")

# Main execution point
def main():
    token = "dummy_text"  # Initial dummy token

    # Create the Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for the playlist link
    playlist_link = simpledialog.askstring("Input", "Enter the playlist link:")
    if not playlist_link:
        messagebox.showerror("Error", "Playlist link is required!")
        return

    token, playlist_id, track_names = fetch_playlist_info(token, playlist_link)

    if not track_names:
        messagebox.showerror("Error", "Failed to get playlist or tracks.")
        return

    # Get artist names associated with the tracks in the playlist
    artists = refresh_token.get_artists_from_playlist(playlist_id)
    search_and_download_videos(track_names, artists, playlist_id)

    messagebox.showinfo("Info", "Download completed!")

if __name__ == "__main__":
    main()
