import csv
import json

# read the geocoded CSV
with open('data/stadiums_geocoded.csv', 'r') as f:
    rows = list(csv.DictReader(f))

# build the GeoJSON
features = []
for row in rows:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row['lon']), float(row['lat'])]
        },
        "properties": {
            "name": row['stadium_name'],
            "city": row['city'],
            "country": row['country'],
            "capacity": int(row['capacity']),
            "tournaments": row['tournaments'],
            "match_count": int(row['match_count']),
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# write to file
with open('data/stadiums.geojson', 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"Wrote {len(features)} features to data/stadiums.geojson")