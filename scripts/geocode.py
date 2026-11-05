import requests
import time
import csv

def geocode(stadium_name, city_name):
    # Try stadium + city first
    for query in [f"{stadium_name}, {city_name}", city_name]:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': query, 'format': 'json'},
            headers={'User-Agent': 'WorldCupProject/1.0'}
        )
        results = response.json()
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
        time.sleep(1)
    return None, None

with open('data/stadiums_raw.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

    with open('data/stadiums_geocoded.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['stadium_id', 'stadium_name', 'city', 'country', 'capacity', 'tournaments', 'match_count', 'lat', 'lon'])
        for i, row in enumerate(rows):
            lat, lon = geocode(row['stadium_name'], row['city'])
            print(f"{i+1}/{len(rows)} - {row['stadium_name']}: {lat}, {lon}")
            writer.writerow([
                row['stadium_id'], row['stadium_name'], row['city'],
                row['country'], row['capacity'], row['tournaments'],
                row['match_count'], lat, lon,
            ])
            time.sleep(1)
    print("Done!")