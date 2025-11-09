import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from load_strava import runs
from running_summary import weekly_summary

st.set_page_config(page_title="My Running Dashboard", layout="wide")
st.title("🏃‍♂️ Running Dashboard")

# -------------------------------
# Weekly Distance Plot
# -------------------------------
st.subheader("Weekly Distance (km)")
fig1, ax1 = plt.subplots()
ax1.plot(
    weekly_summary['running_week'], 
    weekly_summary['distance_km'], 
    marker='o', 
    linestyle='-', 
    color='blue'
)
ax1.set_xlabel("Running Week")
ax1.set_ylabel("Distance (km)")
st.pyplot(fig1)

# -------------------------------
# Number of Runs per Week
# -------------------------------
st.subheader("Number of Runs per Week")
fig2, ax2 = plt.subplots()
ax2.bar(
    weekly_summary['running_week'], 
    weekly_summary['num_runs'], 
    color='orange'
)
ax2.set_xlabel("Running Week")
ax2.set_ylabel("Number of Runs")
st.pyplot(fig2)

# -------------------------------
# -------------------------------
# Monthly Distance vs Average Pace (Filtered)
# -------------------------------
st.subheader("Monthly Distance vs Average Pace (Filtered)")

# Convert to datetime
runs['start_date_local'] = pd.to_datetime(runs['start_date_local'])

# Create a 'year_month' column
runs['year_month'] = runs['start_date_local'].dt.to_period('M').astype(str)

# Compute monthly totals and average pace
monthly_summary = runs.groupby('year_month', as_index=False).agg({
    'distance_km': 'sum',
    'moving_time_min': 'sum'
})

# Calculate monthly average pace (min/km)
monthly_summary['avg_pace'] = monthly_summary['moving_time_min'] / monthly_summary['distance_km']

# Filter out unrealistic paces (<5 or >8 min/km)
monthly_filtered = monthly_summary[
    (monthly_summary['avg_pace'] >= 5) & (monthly_summary['avg_pace'] <= 8)
].copy()

# Plot distance and pace
fig, ax1 = plt.subplots(figsize=(12, 4))

# Distance (left y-axis)
ax1.bar(monthly_filtered['year_month'], monthly_filtered['distance_km'], color='skyblue', label='Distance (km)')
ax1.set_xlabel("Year-Month")
ax1.set_ylabel("Distance (km)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
plt.xticks(rotation=45)

# Pace (right y-axis)
ax2 = ax1.twinx()
ax2.plot(monthly_filtered['year_month'], monthly_filtered['avg_pace'], color='purple', marker='o', label='Average Pace (min/km)')
ax2.set_ylabel("Average Pace (min/km)", color='purple')
ax2.tick_params(axis='y', labelcolor='purple')
ax2.invert_yaxis()  # lower pace = faster

fig.tight_layout()
st.pyplot(fig)

# -------------------------------
# Longest Runs
# -------------------------------
st.subheader("Top 10 Longest Runs")

# Sort by distance and take top 10
top_runs = runs.sort_values(by='distance_km', ascending=False).head(10)

# Convert start_date_local to datetime and keep only date
top_runs['run_date'] = pd.to_datetime(top_runs['start_date_local']).dt.date

# Convert moving_time_min to hh:mm:ss
def format_time(minutes):
    h = int(minutes // 60)
    m = int(minutes % 60)
    s = int(round((minutes - int(minutes)) * 60))
    return f"{h:02d}:{m:02d}:{s:02d}"

top_runs['moving_time_hms'] = top_runs['moving_time_min'].apply(format_time)

# Reset index to remove old index
top_runs_display = top_runs[['run_date', 'name', 'distance_km', 'pace_min_per_km', 'moving_time_hms']].reset_index(drop=True)

# Display table without index
st.table(top_runs_display)

# -------------------------------
# -------------------------------
# Fastest Run Progress by Distance (Trendline)
# -------------------------------
st.subheader("Fastest Run Progress: 5K, 10K, 21K")

# Target distances with tolerance
targets = {
    "5K": (4.5, 5.5),
    "10K": (9.5, 10.5),
    "21K": (20.5, 21.5)
}

# Prepare dataframe for plotting
fastest_runs_list = []

# Ensure date column is datetime
runs['start_date_local'] = pd.to_datetime(runs['start_date_local'])
runs['year'] = runs['start_date_local'].dt.year

for label, (min_d, max_d) in targets.items():
    subset = runs[(runs['distance_km'] >= min_d) & (runs['distance_km'] <= max_d)].copy()
    fastest_per_year = subset.sort_values('pace_min_per_km').groupby('year').head(1)
    fastest_per_year['distance_label'] = label
    fastest_runs_list.append(fastest_per_year)

fastest_runs = pd.concat(fastest_runs_list)
fastest_runs = fastest_runs.sort_values('start_date_local')

# Format moving time
fastest_runs['time_hms'] = fastest_runs['moving_time_min'].apply(format_time)

# Plot combined trendlines
fig, ax = plt.subplots(figsize=(12, 5))
colors = {"5K": "green", "10K": "blue", "21K": "red"}

for dist_label, color in colors.items():
    subset = fastest_runs[fastest_runs['distance_label'] == dist_label]
    ax.plot(
        subset['start_date_local'], 
        subset['pace_min_per_km'], 
        marker='o', linestyle='-', 
        color=color, label=dist_label
    )

ax.set_xlabel("Date")
ax.set_ylabel("Pace (min/km)")
ax.set_title("Fastest Run Progress by Distance")
ax.invert_yaxis()  # lower pace = faster
ax.legend(title="Distance")
plt.xticks(rotation=45)
fig.tight_layout()
st.pyplot(fig)

# Optional: show table for reference
st.write("Fastest Runs by Distance Each Year")
st.table(
    fastest_runs[['year', 'distance_label', 'start_date_local', 'name', 'distance_km', 'time_hms', 'pace_str']].reset_index(drop=True)
)




# -------------------------------
# Summary Stats
# -------------------------------
st.subheader("Running Summary")
st.write(f"**Total Runs:** {len(runs)}")
st.write(f"**Total Distance:** {runs['distance_km'].sum():.2f} km")
st.write(f"**Average Pace:** {runs['pace_min_per_km'].mean():.2f} min/km")
st.write(f"**Average Moving Time:** {runs['moving_time_min'].mean():.1f} min")
st.write(f"**Longest Run:** {runs['distance_km'].max():.2f} km")
