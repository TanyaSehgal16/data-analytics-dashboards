import requests
import pandas as pd

#Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        })
    auth_data = auth_response.json()
    return auth_data['access_token']

#Function to search for a Track and get its ID
def search_track(Track, Artist, token):
    query = f"{Track} Artist:{Artist}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
        })
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None

#Function to get Track details
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
        })
    json_data = response.json()
    image_url = json_data['album']['images'][0]['url']
    return image_url

#Your Spotify API Credentials
client_id = '1234'
client_secret = '1234'

#Get Access Token
access_token = get_spotify_token(client_id, client_secret)

#Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
df_spotify = pd.read_csv('Most_Streamed_Spotify_Songs_2024.csv', encoding='ISO-8859-1')

#Loop through each row to get Track details and add to DataFrame
for i, row in df_spotify.iterrows():
    track_id = search_track(row['Track'], row['Artist'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        df_spotify.at[i, 'image_url'] = image_url
        
#Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
df_spotify.to_csv('Most_Streamed_Spotify_Songs_2024_updated_file.csv', index=False)
print("Done! Saved as Most_Streamed_Spotify_Songs_2024_updated_file.csv")
