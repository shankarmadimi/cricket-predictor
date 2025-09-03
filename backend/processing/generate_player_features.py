import pandas as pd
import numpy as np
import os

# Paths
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
INPUT_FILE = os.path.join(BASE_PATH, "clean_balls.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "player_features.csv")

def generate_batting_features(df):
    """
    Generate batting features for each player by format.
    """
    print("📊 Generating batting metrics...")

    batting = df.groupby(['format', 'batter']).agg(
        balls_faced=('batter', 'count'),
        runs_scored=('runs_batter', 'sum'),
        fours=('runs_batter', lambda x: (x == 4).sum()),
        sixes=('runs_batter', lambda x: (x == 6).sum()),
        dismissals=('player_out', lambda x: (x.notna()).sum())
    ).reset_index()

    # Derived Metrics
    batting['strike_rate'] = (batting['runs_scored'] / batting['balls_faced']) * 100
    batting['boundary_percent'] = ((batting['fours'] + batting['sixes']) / batting['balls_faced']) * 100
    batting['batting_average'] = batting.apply(
        lambda row: row['runs_scored'] / row['dismissals'] if row['dismissals'] > 0 else row['runs_scored'],
        axis=1
    )
    batting['dismissal_probability'] = batting['dismissals'] / batting['balls_faced']

    return batting

def generate_bowling_features(df):
    """
    Generate bowling features for each player by format.
    """
    print("📊 Generating bowling metrics...")

    bowling = df.groupby(['format', 'bowler']).agg(
        balls_bowled=('bowler', 'count'),
        runs_conceded=('runs_total', 'sum'),
        wickets=('is_wicket', 'sum'),
        dot_balls=('runs_total', lambda x: (x == 0).sum())
    ).reset_index()

    # Derived Metrics
    bowling['overs_bowled'] = bowling['balls_bowled'] / 6
    bowling['economy_rate'] = bowling.apply(
        lambda row: row['runs_conceded'] / row['overs_bowled'] if row['overs_bowled'] > 0 else 0,
        axis=1
    )
    bowling['wicket_probability'] = bowling['wickets'] / bowling['balls_bowled']
    bowling['dot_ball_percent'] = (bowling['dot_balls'] / bowling['balls_bowled']) * 100

    return bowling

def main():
    print("🚀 Generating player features...")

    # Load cleaned data
    df = pd.read_csv(INPUT_FILE)
    print(f"🔹 Loaded {len(df)} rows from {INPUT_FILE}")

    # Ensure essential columns are present
    required_columns = ['format', 'batter', 'bowler', 'runs_batter', 'runs_total', 'is_wicket', 'player_out']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column in clean_balls.csv: {col}")

    # Generate batting and bowling metrics
    batting_df = generate_batting_features(df)
    bowling_df = generate_bowling_features(df)

    # Merge both on player and format
    features_df = pd.merge(
        batting_df,
        bowling_df,
        left_on=['format', 'batter'],
        right_on=['format', 'bowler'],
        how='outer'
    )

    # Clean column names after merge
    features_df = features_df.rename(columns={'batter': 'player_name'})
    features_df.drop(columns=['bowler'], inplace=True)

    # Fill NaNs with 0 for numerical fields
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns
    features_df[numeric_cols] = features_df[numeric_cols].fillna(0)

    # Save final CSV
    features_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Player features saved to {OUTPUT_FILE}")
    print(f"Final shape: {features_df.shape}")
    print(features_df.head(10))

if __name__ == "__main__":
    main()
