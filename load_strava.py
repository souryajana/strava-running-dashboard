import pandas as pd
import numpy as np
import math

# Load your Strava CSV
df = pd.read_csv('strava_activities_all_fields.csv')

# Filter only running activities
runs = df[df['type'] == 'Run'].copy()

# Convert distances (m → km) and moving time (s → min)
runs['distance_km'] = runs['distance'] / 1000
runs['moving_time_min'] = runs['moving_time'] / 60

# Calculate pace (min/km)
runs['pace_min_per_km'] = runs['moving_time_min'] / runs['distance_km']

# --- Safe format functions ---
def format_time(minutes):
    if pd.isna(minutes) or minutes == 0:
        return ""
    h = int(minutes // 60)
    m = int(minutes % 60)
    s = int(round((minutes * 60) % 60))
    return f"{h}:{m:02d}:{s:02d}"

def format_pace(pace_min_per_km):
    if pace_min_per_km is None or pd.isna(pace_min_per_km) or pace_min_per_km == 0:
        return ""
    total_seconds = pace_min_per_km * 60
    if math.isnan(total_seconds):
        return ""
    m = int(total_seconds // 60)
    s = int(round(total_seconds % 60))
    return f"{m}:{s:02d}/km"

# Create formatted columns
runs['distance_km_str'] = runs['distance_km'].round(2)
runs['moving_time_str'] = runs['moving_time_min'].apply(format_time)
runs['pace_str'] = runs['pace_min_per_km'].apply(format_pace)

# Sort by most recent date (optional)
if 'start_date_local' in runs.columns:
    runs = runs.sort_values(by='start_date_local', ascending=False)

# Display summary table
print(runs[['name', 'distance_km_str', 'moving_time_str', 'pace_str']].head())
