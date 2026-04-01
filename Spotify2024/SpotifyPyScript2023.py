import pandas as pd
import requests
import time

# ----------------------------------------
# 1. ENTER YOUR SPOTIFY API CREDENTIALS
# ----------------------------------------
CLIENT_ID = "1234"
CLIENT_SECRET = "1234"

# ----------------------------------------
# 2. AUTHENTICATE WITH SPOTIFY API
# ----------------------------------------
auth_url = "https://accounts.spotify.com/api/token"
auth_response = requests.post(
    auth_url,
    data={"grant_type": "client_credentials"},
    auth=(CLIENT_ID, CLIENT_SECRET)
)

access_token = auth_response.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# ----------------------------------------
# 3. LOAD YOUR DATASET
# ----------------------------------------
df = pd.read_csv("spotify-2023.csv", encoding="latin1")

# Create new column
df["Cover_URL"] = None

# ----------------------------------------
# 4. FUNCTION TO SEARCH TRACK AND FETCH COVER URL
# ----------------------------------------
def get_cover_url(track, artist):
    query = f"track:{track} artist:{artist}"
    url = "https://api.spotify.com/v1/search"
    
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        print(f"Error {r.status_code} for {track} – retrying...")
        return None

    data = r.json()
    items = data.get("tracks", {}).get("items", [])

    if not items:
        print(f"No match: {track} by {artist}")
        return None

    # First image (largest) is usually [0]
    return items[0]["album"]["images"][0]["url"]

# ----------------------------------------
# 5. LOOP THROUGH ROWS AND FETCH URLS
# ----------------------------------------
for idx, row in df.iterrows():
    track = row["track_name"]
    artist = row["artist(s)_name"]

    print(f"Fetching cover URL for: {track} — {artist}")

    cover_url = get_cover_url(track, artist)
    df.at[idx, "Cover_URL"] = cover_url

    time.sleep(0.15)   # prevents rate-limit issues

# ----------------------------------------
# 6. SAVE OUTPUT
# ----------------------------------------
df.to_csv("Spotify_Songs_With_Cover_URLs.csv", index=False)
print("Done! Saved as Spotify_Songs_With_Cover_URLs.csv")
