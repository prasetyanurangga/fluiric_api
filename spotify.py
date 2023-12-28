from datetime import datetime, timedelta
import json
import os
import requests

class SpotifyException(Exception):
    pass

class Spotify:
    def __init__(self, sp_dc):
        self.sp_dc = sp_dc
        self.token_url = 'https://open.spotify.com/get_access_token?reason=transport&productType=web_player'
        self.lyrics_url = 'https://spclient.wg.spotify.com/color-lyrics/v2/track/'

    def get_token(self):
        if not self.sp_dc:
            raise SpotifyException('Please set SP_DC as an environmental variable.')

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
            'App-platform': 'WebPlayer',
            'content-type': 'text/html; charset=utf-8',
            'cookie': f'sp_dc={self.sp_dc};'
        }

        response = requests.get(self.token_url, headers=headers)
        token_json = response.json()

        if not token_json or token_json['isAnonymous']:
            raise SpotifyException('The SP_DC set seems to be invalid, please correct it!')

        with open('.cache', 'w') as token_file:
            json.dump(token_json, token_file)

    def check_token_expire(self):
        if os.path.exists('.cache'):
            with open('.cache', 'r') as file:
                token_data = json.load(file)
                expiration_time = datetime.utcfromtimestamp(token_data['accessTokenExpirationTimestampMs'] / 1000)
                current_time = datetime.utcnow()

            if current_time > expiration_time:
                self.get_token()
        else:
            self.get_token()

    def get_lyrics(self, track_id):
        with open('.cache', 'r') as file:
            token = json.load(file)['accessToken']

        formatted_url = f'{self.lyrics_url}{track_id}?format=json&market=from_token'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
            'App-platform': 'WebPlayer',
            'authorization': f'Bearer {token}'
        }

        response = requests.get(formatted_url, headers=headers)
        return response.json()


