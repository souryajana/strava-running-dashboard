# running_summary.py
from load_strava import runs
import pandas as pd

# --- Summary Metrics ---

# Total distance (km)
total_distance = runs['distance_km'].sum().round(2)

# Total runs
total_runs = len(runs)

# Average pace (min/km)
average_pace = (runs['pace_min_per_km'].mean()).round(2)

# Average moving time (minutes)
average_moving_time = (runs['moving_time_min'].mean()).round(1)

# Longest run
longest_run = runs['distance_km'].max().round(2)

# Print summary
print("Running Summary")
print(f"Total Runs: {total_runs}")
print(f"Total Distance: {total_distance} km")
print(f"Average Pace: {average_pace} min/km")
print(f"Average Moving Time: {average_moving_time} min")
print(f"Longest Run: {longest_run} km")

# Ensure start_date_local is datetime
runs['start_date_local'] = pd.to_datetime(runs['start_date_local'])

# Extract year and ISO week
runs['year'] = runs['start_date_local'].dt.isocalendar().year
runs['week'] = runs['start_date_local'].dt.isocalendar().week

# Group by year and week
weekly_summary = runs.groupby(['year', 'week']).agg(
    distance_km=('distance_km', 'sum'),
    num_runs=('name', 'count')
).reset_index()

# Sort and add running_week counter
weekly_summary = weekly_summary.sort_values(['year', 'week']).reset_index(drop=True)
weekly_summary['running_week'] = range(1, len(weekly_summary) + 1)

print(weekly_summary)
