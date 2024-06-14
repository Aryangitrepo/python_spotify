import requests
import spotify_api.refresh_token as refresh_token
from pytube import YouTube

# Edit the URLs if you run into version errors and add your own api keys.
SPOTIFY_API_URL = "https://api.spotify.com/v1"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_API_KEYS = [
    "add yt keys here"
]

def get_playlists(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{SPOTIFY_API_URL}/me/playlists", headers=headers)
    return res


def get_tracks(token, playlist_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks", headers=headers)
    return res


# Main function to fetch playlist and track information. This was built to fix the random connectionbreak error.
def fetch_playlist_info(token):
    res = get_playlists(token)
    if res.status_code == 401:
        print("\nCreating token...")
        token = refresh_token.re_to()
        res = get_playlists(token)

    if res.status_code != 200:
        print("Failed to get playlists:", res.status_code, res.text)
        return token, "", []

    playlist_link = input("Enter the playlist link:")
    id_pos = playlist_link.find("playlist") + 9
    q_pos = playlist_link.find('?')
    playlist_id = playlist_link[id_pos:q_pos if q_pos > 9 else len(playlist_link)]
    print("Playlist ID:", playlist_id)

    tracks_res = get_tracks(token, playlist_id)
    if tracks_res.status_code != 200:
        print("Failed to get tracks:", tracks_res.status_code, tracks_res.text)
        return token, playlist_id, []

    tracks = tracks_res.json()
    track_names = [item["track"]["name"] for item in tracks["items"]]
    artists= [item["track"]["artists"][0]["name"] for item in tracks["items"]]

    if not track_names:
        print("No tracks available")
    else:
        for i, name in enumerate(track_names):
            print(i, name)

    return token, playlist_id, track_names,artists


# Function to search YouTube and download videos. edit at your own risk.
def search_and_download_videos(track_names, artists):
    for i, track_name in enumerate(track_names):
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

        # Downloading part - may or maynot throw age restricted error. May come off as an issue in the future.
        print("Download started for:", track_name +f" by {artists[i]}")
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        try:
            res = yt.streams.filter(only_audio=True, abr="128kbps")
            if res:
                stream = res[0]
               # output_path = f"./downloads/{refresh_token.get_playlist_name(playlist_id)}" this aint working 
                stream.download("./downloads")
                print(f"Downloaded {track_name}  to downloads")
            else:
                print(f"No suitable stream found for {track_name}")
        except Exception as e:
            print(f"Failed to download {track_name}: {e}")


# Main execution
def main():
    token = "dummy_text"
    token, playlist_id, track_names,artists = fetch_playlist_info(token)
    print(f"the playlist id : {playlist_id}")
    if not track_names:
        print("Failed to get playlist or tracks.")
        return
    # what was here ??
    search_and_download_videos(track_names,artists)

if __name__ == "__main__":
    main()
