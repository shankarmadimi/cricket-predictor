import os
import json
import pandas as pd

# Define dataset folders
import os
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
FORMATS = {
    "ODI": "odis_json",
    "T20": "t20s_json",
    "TEST": "tests_json"
}

# Storage lists
matches_list = []
balls_list = []
players_set = set()

def extract_match_data(file_path, match_format):
    """Extracts match-level and ball-by-ball data from a single Cricsheet JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})
    teams = info.get("teams", [])

    # Create a unique match ID using file name
    match_id = os.path.splitext(os.path.basename(file_path))[0]

    # Match-level data
    match_record = {
        "match_id": match_id,
        "format": match_format,
        "date": info.get("dates", [None])[0],
        "venue": info.get("venue", None),
        "team1": teams[0] if len(teams) > 0 else None,
        "team2": teams[1] if len(teams) > 1 else None,
        "toss_winner": info.get("toss", {}).get("winner", None),
        "toss_decision": info.get("toss", {}).get("decision", None),
        "winner": info.get("outcome", {}).get("winner", None),
        "win_by_runs": info.get("outcome", {}).get("by", {}).get("runs", None),
        "win_by_wickets": info.get("outcome", {}).get("by", {}).get("wickets", None)
    }
    matches_list.append(match_record)

    # Extract ball-by-ball data
    innings = data.get("innings", [])
    for inning_index, inning_details in enumerate(innings, start=1):
        batting_team = inning_details.get("team", None)
        overs = inning_details.get("overs", [])

        for over in overs:
            over_number = over.get("over")
            deliveries = over.get("deliveries", [])

            for delivery in deliveries:
                batter = delivery.get("batter")
                bowler = delivery.get("bowler")
                non_striker = delivery.get("non_striker")

                # Add players to master set
                players_set.add(batter)
                players_set.add(bowler)
                players_set.add(non_striker)

                # Runs
                runs = delivery.get("runs", {})
                runs_batter = runs.get("batter", 0)
                runs_extras = runs.get("extras", 0)
                runs_total = runs.get("total", 0)

                # Wickets
                wicket_info = delivery.get("wickets", [])
                is_wicket = 1 if wicket_info else 0
                wicket_kind = None
                player_out = None
                if is_wicket:
                    wicket_kind = wicket_info[0].get("kind", None)
                    player_out = wicket_info[0].get("player_out", None)
                    players_set.add(player_out)

                balls_list.append({
                    "match_id": match_id,
                    "format": match_format,
                    "inning": inning_index,
                    "batting_team": batting_team,
                    "over": over_number,
                    "ball": delivery.get("ball", None),
                    "batter": batter,
                    "bowler": bowler,
                    "non_striker": non_striker,
                    "runs_batter": runs_batter,
                    "runs_extras": runs_extras,
                    "runs_total": runs_total,
                    "is_wicket": is_wicket,
                    "wicket_kind": wicket_kind,
                    "player_out": player_out
                })

def process_all_matches():
    """Process all formats and generate matches.csv, balls.csv, players.csv."""
    for match_format, folder in FORMATS.items():
        folder_path = os.path.join(BASE_PATH, folder)

        if not os.path.exists(folder_path):
            print(f"⚠️ Folder not found: {folder_path}")
            continue

        print(f"📂 Processing {match_format} matches...")
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                try:
                    extract_match_data(file_path, match_format)
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")

    # Convert to DataFrames
    matches_df = pd.DataFrame(matches_list)
    balls_df = pd.DataFrame(balls_list)
    players_df = pd.DataFrame(sorted(list(players_set)), columns=["player_name"])

    # Ensure BASE_PATH exists before saving CSVs
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    # Save to CSV files
    matches_df.to_csv(os.path.join(BASE_PATH, "matches.csv"), index=False)
    balls_df.to_csv(os.path.join(BASE_PATH, "balls.csv"), index=False)
    players_df.to_csv(os.path.join(BASE_PATH, "players.csv"), index=False)

    print("\n✅ Extraction Complete!")
    print(f"Matches: {len(matches_df)} rows saved to matches.csv")
    print(f"Balls: {len(balls_df)} rows saved to balls.csv")
    print(f"Players: {len(players_df)} unique players saved to players.csv")

if __name__ == "__main__":
    process_all_matches()
