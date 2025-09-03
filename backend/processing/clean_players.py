import pandas as pd
import re
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
BALLS_FILE = os.path.join(BASE_PATH, "balls.csv")
PLAYERS_FILE = os.path.join(BASE_PATH, "players.csv")

OUTPUT_MAPPING_FILE = os.path.join(BASE_PATH, "player_mapping.csv")
OUTPUT_CLEAN_BALLS_FILE = os.path.join(BASE_PATH, "clean_balls.csv")

# Helper function to clean player names
def clean_name(name):
    if pd.isna(name):
        return name

    # Remove (c), (wk), etc.
    name = re.sub(r"\(.*?\)", "", name)

    # Remove extra spaces
    name = name.strip()

    # Replace multiple spaces with single
    name = re.sub(r"\s+", " ", name)

    return name

def generate_player_mapping():
    """Creates a mapping of raw_name -> clean_name"""
    players_df = pd.read_csv(PLAYERS_FILE)

    print(f"🔹 Original players loaded: {len(players_df)}")

    players_df['clean_name'] = players_df['player_name'].apply(clean_name)

    # Remove duplicates
    players_df = players_df.drop_duplicates(subset=['clean_name'])

    # Save the mapping
    players_df[['player_name', 'clean_name']].to_csv(OUTPUT_MAPPING_FILE, index=False)
    print(f"✅ Player mapping saved to {OUTPUT_MAPPING_FILE}")

    return players_df

def clean_balls_data(mapping_df):
    """Replaces raw names in balls.csv with clean names."""
    print("📂 Loading balls.csv for cleaning...")
    balls_df = pd.read_csv(BALLS_FILE)

    # Create a mapping dictionary
    name_map = dict(zip(mapping_df['player_name'], mapping_df['clean_name']))

    print("🔹 Replacing names in batter, bowler, and player_out columns...")

    for col in ['batter', 'bowler', 'non_striker', 'player_out']:
        balls_df[col] = balls_df[col].map(name_map).fillna(balls_df[col])

    # Save cleaned balls file
    balls_df.to_csv(OUTPUT_CLEAN_BALLS_FILE, index=False)
    print(f"✅ Cleaned balls.csv saved to {OUTPUT_CLEAN_BALLS_FILE}")
    print(f"Final rows: {len(balls_df)}")

def main():
    print("🚀 Starting player cleaning process...")

    # Step 1: Generate player mapping
    mapping_df = generate_player_mapping()

    # Step 2: Clean balls.csv using mapping
    clean_balls_data(mapping_df)

    print("🎉 Cleaning process complete!")

if __name__ == "__main__":
    main()
