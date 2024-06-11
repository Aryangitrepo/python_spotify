import requests
import refresh_token

token_ = "abcd"

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

def fun(token):
    res = get_playlists(token)
    try:
        if res.status_code == 401:
            print("\nCreating token...")
            token = refresh_token.re_to()
            res = get_playlists(token)
            user = res.json()
            print(user)
            playlist_id = user["items"][0]["id"]
            tracks_res = get_tracks(token, playlist_id)
            if tracks_res.status_code == 200:
                tracks = tracks_res.json()
                mylist=[]
                if tracks["items"]==mylist:
                    print("no tracks available")
                else:
                    for i, result in enumerate(tracks["items"], 0):
                        print(i, result["track"]["name"], result["track"]["id"])
            else:
                print("Failed to get tracks:", tracks_res.status_code, tracks_res.text)
    except:
        print("no play lists found")
        return token

token_ = fun(token_)
    

