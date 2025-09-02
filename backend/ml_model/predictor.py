import json
import pandas as pd
import numpy as np
import sys
import os

# --- Data Loading and Preprocessing ---
def load_data(filepath):
    """
    Loads data from a single JSON file.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}", file=sys.stderr)
        return None

def load_and_preprocess_data(format_type):
    """
    Loads mock cricket data for a given format from the /data directory.
    In a real scenario, this would involve processing the full Cricsheet data.
    """
    filepath = os.path.join('..', 'data', f'{format_type}_data.json')
    raw_data = load_data(filepath)

    if not raw_data:
        # Fallback to mock data if file is not found
        if format_type == 't20':
            data = {
                'player_name': ['Virat Kohli', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne'],
                'bat_strike_rate': [135, 12, 125, 60],
                'bowl_economy': [7.5, 6.5, 8.0, 7.0]
            }
        elif format_type == 'odi':
            data = {
                'player_name': ['Virat Kohli', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne'],
                'bat_strike_rate': [93, 15, 86, 75],
                'bowl_economy': [5.8, 5.2, 5.5, 5.0]
            }
        elif format_type == 'test':
            data = {
                'player_name': ['Virat Kohli', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne'],
                'bat_strike_rate': [55, 10, 54, 45],
                'bowl_economy': [3.5, 2.8, 3.2, 3.0]
            }
        else:
            return pd.DataFrame() # Return empty if format is not recognized
        
        df = pd.DataFrame(data)
        df.set_index('player_name', inplace=True)
        return df
    
    # Placeholder for actual data processing logic
    # Here you would process the raw_data to create a structured DataFrame
    processed_data = {
        'player_name': [p['name'] for p in raw_data['players']],
        'bat_strike_rate': [p['bat_strike_rate'] for p in raw_data['players']],
        'bowl_economy': [p['bowl_economy'] for p in raw_data['players']]
    }
    df = pd.DataFrame(processed_data)
    df.set_index('player_name', inplace=True)
    return df

# --- Prediction Engine (Monte Carlo Simulation) ---
def simulate_player_vs_player(player1, player2, format_type):
    """
    Simulates a player-vs-player matchup using a simple probabilistic model.
    """
    data = load_and_preprocess_data(format_type)

    if player1 not in data.index or player2 not in data.index:
        return {"winner": "N/A", "probability": "0%", "reasoning": "Player not found in data."}

    # Simplified logic for demonstration
    if data.loc[player1, 'bat_strike_rate'] > data.loc[player2, 'bowl_economy'] * 15:
        return {"winner": player1, "probability": "75%", "reasoning": f"{player1}'s aggressive batting style gives him an edge over {player2}."}
    else:
        return {"winner": player2, "probability": "65%", "reasoning": f"{player2}'s disciplined bowling and control of the run-rate are predicted to be a challenge for {player1}."}

def simulate_team_vs_team(team1, team2, format_type):
    """
    Simulates a team-vs-team matchup based on aggregate team strengths.
    """
    data = load_and_preprocess_data(format_type)

    # Simplified logic for demonstration
    team1_strength = sum(data.loc[player, 'bat_strike_rate'] for player in team1)
    team2_strength = sum(data.loc[player, 'bowl_economy'] for player in team2)

    if team1_strength > team2_strength * 25:
        return {"winner": "Team 1", "probability": "80%", "reasoning": "Team 1's superior batting depth is expected to outperform Team 2's bowlers."}
    else:
        return {"winner": "Team 2", "probability": "70%", "reasoning": "Team 2's balanced bowling attack is likely to contain Team 1's batsmen."}

# --- Main function to handle CLI arguments ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments."}))
        sys.exit(1)

    command = sys.argv[1]
    args = json.loads(sys.argv[2])

    if command == 'simulate_player_vs_player':
        result = simulate_player_vs_player(args['player1'], args['player2'], args['format'])
        print(json.dumps(result))
    elif command == 'simulate_team_vs_team':
        result = simulate_team_vs_team(args['team1'], args['team2'], args['format'])
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Unknown command."}))
        sys.exit(1)
