import requests

# Constants
TOKEN_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = '0fd112519e78427298e734ebc971c0cf'
CLIENT_SECRET = 'bb3aaa058b074840bf971b4d7813d386'
REFRESH_TOKEN = 'AQBw55muI4lxIVrNU_DEVJhtZ_bh3MnGqbj9bNEIxQXE33EtT2aR4uq2VwSy_eS4uam_E8Q7pIto7kMKGNa4hMnn6ydYrgggQgygWvCVtLaq4tdmKL6XBF1OmYx-h1yX_Ac'

# Data for token request
data = {
    'grant_type': 'refresh_token',
    'refresh_token': REFRESH_TOKEN,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
def re_to():
    try:
        # Request new access token
        response = requests.post(TOKEN_URL, data=data, headers=headers)

        # Debugging: print the raw response content
        print(f'Response status code: {response.status_code}')

        # Handle the response
        if response.status_code == 200:
            try:
                tokens = response.json()
                new_access_token = tokens['access_token']
                new_refresh_token = tokens.get('refresh_token')  # Update if a new one is provided
                print(f'New access token: {new_access_token}')
                if new_refresh_token:
                    print(f'New refresh token: {new_refresh_token}')
                return new_access_token
            except requests.exceptions.JSONDecodeError:
                print('Response content is not valid JSON')
        else:
            print(f'Failed to refresh token: {response.status_code}')
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
