import subprocess

subprocess.run(["python", "fetch_activity.py"])
subprocess.run(["python", "load_strava.py"])
subprocess.run(["python", "running_summary.py"])
subprocess.run(["streamlit", "run", "running_dashboard.py"])