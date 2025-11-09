import requests
import pandas as pd
import json
import time

# Load tokens
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)

# Check if token expired
if strava_tokens['expires_at'] < time.time():
    print("Token expired, refreshing...")
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': 177576,
            'client_secret': 'e1615c049012ca250f77b81d7c7736e63e7d13ee',
            'grant_type': 'refresh_token',
            'refresh_token': strava_tokens['refresh_token']
        }
    )
    new_tokens = response.json()
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_tokens, outfile)
    strava_tokens = new_tokens
    print("✅ Token refreshed successfully!")

# Use updated token
access_token = strava_tokens['access_token']

# Fetch activities
page = 1
activities = []

while True:
    print(f"Fetching page {page}...")
    url = f"https://www.strava.com/api/v3/athlete/activities?page={page}&per_page=200&access_token={access_token}"
    r = requests.get(url)
    data = r.json()
    if not data or 'message' in data:
        print("No more activities or error:", data)
        break
    activities.extend(data)
    page += 1

df = pd.json_normalize(activities)
df.to_csv('strava_activities_all_fields.csv', index=False)
print(f"Saved {len(df)} activities to CSV file.")
