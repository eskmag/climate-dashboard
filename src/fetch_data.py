import requests
import pandas as pd

# Bergen coordinates
latitude = 60.3913
longitude = 5.3221

# Define date range
start_date = "2014-01-01"
end_date = "2024-12-31"

# Build URL
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=Europe%2FOslo"
)

# Fetch data
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['daily'])
df['time'] = pd.to_datetime(df['time'])

# Calculate average temperature
df['temperature_avg'] = (df['temperature_2m_max'] + df['temperature_2m_min']) / 2

# Preview
print(df.head())

# Save to CSV
df.to_csv("bergen_climate_data.csv", index=False)
