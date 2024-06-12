import requests
import refresh_token
from pytube import YouTube

token_ = "abcd"
api_key="AIzaSyD24-nGJlYZzy-hgG746XZcRVfprUdNXyk"

def get_playlists(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    return res

def get_tracks(token, playlist_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
    return res
name=[]
artists=[]
def fun(token):
    res = get_playlists(token)
    try:
        if res.status_code == 401:
            print("\nCreating token...")
            token = refresh_token.re_to()
            res = get_playlists(token)
            user = res.json()
            playlist_id = user["items"][0]["id"] #add iteration for multiple playlists
            tracks_res = get_tracks(token, playlist_id)
            if tracks_res.status_code == 200:
                tracks = tracks_res.json()
                mylist=[]
                if tracks["items"]==mylist:
                    print("no tracks available")
                else:
                    for i, result in enumerate(tracks["items"], 0):
                        print(i, result["track"]["name"])
                        name.append(result["track"]["name"])
                        artists.append(result["track"]["artists"][0]["name"])
            else:
                print("Failed to get tracks:", tracks_res.status_code, tracks_res.text)
    except:
        print("no play lists found")
        return token

token_ = fun(token_)

#yt searching
yt_url="https://www.googleapis.com/youtube/v3/search"
for names,artist in zip(name,artists):
    try:
        yt_res = requests.get(yt_url, params={"key": api_key, "q": names+" "+artist, "type": "video"})
        print(f"Status code for '{names}': {yt_res.status_code}")
        yt_js = yt_res.json()
        video_id = yt_js["items"][0]["id"]["videoId"]
        print(f"Video ID for '{names}': {video_id}")
        print("Download started.......")
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        res = yt.streams.filter(only_audio=True, abr="128kbps")
        if res:
            stream = res.first()
            stream.download(output_path="./downloads")
            print(f"Download completed for '{names}' by {artist}")
        else:
            print(f"No suitable audio stream found for '{names}'")
    except Exception as e:
        print(f"An error occurred for '{names}': {e}")
        continue