import csv
import requests
import os 
import time

stadiums_resp = requests.get('https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/stadiums.csv')
matches_resp = requests.get('https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/matches.csv')

# parse stadiums into a dictionary keyed by stadium_id
stadiums = {}
reader = csv.DictReader(stadiums_resp.text.splitlines())
for row in reader:
    # store each stadium in the dict
    stadiums[row['stadium_id']] = {
        'stadium_name': row['stadium_name'],                                         
        'city_name': row['city_name'],                                               
        'country_name': row['country_name'],                                         
        'capacity': row['stadium_capacity'],                                         
    }
    pass

# collect matches per stadium
# stadium_id -> list of match dicts
stadium_matches = {}
reader = csv.DictReader(matches_resp.text.splitlines())
for row in reader:
    # append match info to that stadium's list
    sid = row['stadium_id']
    if sid not in stadium_matches:
        stadium_matches[sid] = []
    stadium_matches[sid].append({
        'tournament': row['tournament_name'],
        'date': row['match_date'],
        'stage': row['stage_name'],
        'home': row['home_team_name'],
        'away': row['away_team_name'],
        'score': row['score'],
        'gender': 'men' if "Men's" in row['tournament_name'] else 'women'
    })
    pass

# combine and print
for stadium_id, matches in stadium_matches.items():
    info = stadiums[stadium_id]
    print(f"\n{info['stadium_name']} ({info['city_name']}) {info['capacity']} — {len(matches)} matches")
    for m in matches[:3]:  # print first 3 as a preview
        # print match details
        print(f"  {m['tournament']} | {m['stage']} | {m['home']} vs {m['away']} {m['score']}")
        pass

os.makedirs('data', exist_ok=True)

with open('data/stadiums_raw.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['stadium_id', 'stadium_name', 'city', 'country', 'capacity','tournaments', 'match_count'])

    for stadium_id, matches in stadium_matches.items():
        info = stadiums[stadium_id]
        tournaments = sorted(set(m['tournament'] for m in matches))
        writer.writerow([
            stadium_id,
            info['stadium_name'],
            info['city_name'],
            info['country_name'],
            info['capacity'],
            '; '.join(tournaments),
            len(matches),
        ])

print(f"Saved {len(stadium_matches)} stadiums to data/stadiums_raw.csv")
