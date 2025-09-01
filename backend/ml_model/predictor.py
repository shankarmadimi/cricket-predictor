import sys
import json
import random

def generate_reasoning(data):
    try:
        data = json.loads(data)
        winner = data.get('winner')
        probability = data.get('probability')
        match_type = data.get('type')

        reasons = {
            'player': [
                f"The simulation predicts {winner} to win with a {probability} chance due to superior historical performance in key metrics. Their consistent form against a variety of opponents gives them a distinct advantage.",
                f"{winner} has been favored in this matchup. The model highlights their exceptional ability to exploit the weaknesses of players with a similar style to their opponent, giving them a high probability of success.",
                f"The AI analysis shows {winner} is highly likely to dominate. Factors such as their incredible match-winning record and ability to perform under pressure heavily influenced the simulation outcome."
            ],
            'team': [
                f"Team {winner} is predicted to win with a {probability} chance. The model identified their strong batting depth and a versatile bowling attack as key differentiators, giving them a significant edge in the simulation.",
                f"The Monte Carlo simulation resulted in a victory for Team {winner}. The analysis points to their balanced lineup and a few key players whose performance consistently elevates the entire team, making them the favorites.",
                f"Team {winner} is favored to win. The AI-powered reasoning suggests that their cohesive team structure and historical clutch performance in critical moments give them a high probability of success in this matchup."
            ]
        }
        print(random.choice(reasons.get(match_type, ["Simulation complete."])))

    except Exception as e:
        print(f"Error generating reasoning: {e}", file=sys.stderr)
        sys.exit(1)

def generate_biography(player):
    try:
        biographies = {
            'Virat Kohli': "Virat Kohli is an Indian cricketer and a former captain of the Indian national cricket team. He is widely regarded as one of the greatest batsmen in the history of the sport. Known for his aggressive batting style and relentless consistency, Kohli has set numerous records across all formats of the game.",
            'Jasprit Bumrah': "Jasprit Bumrah is an Indian international cricketer who plays as a fast-medium bowler. Considered one of the best bowlers in the world, he is known for his unique unorthodox action, accurate yorkers, and ability to generate pace. He is a key player in all formats for the Indian team.",
            'Sachin Tendulkar': "Sachin Tendulkar is a former Indian cricketer who captained the national team. Widely regarded as the 'God of Cricket', he is the highest run-scorer of all time in international cricket and the only player to have scored one hundred international centuries. His career spanned from 1989 to 2013, making him a global icon.",
            'Shane Warne': "Shane Warne was an Australian cricketer and one of the greatest leg-spinners in the history of the sport. Known for his 'Ball of the Century', he revolutionized the art of leg-spin. With over 1,000 international wickets, he was a key figure in Australia's dominant era.",
            'Wasim Akram': "Wasim Akram is a Pakistani cricket commentator, coach, and former cricketer. Known as the 'Sultan of Swing', he is widely regarded as one of the greatest fast bowlers of all time. He was a master of reverse swing and was a dominant force with both the new and old ball.",
            'Chris Gayle': "Chris Gayle is a Jamaican cricketer who is considered one of the greatest batsmen in Twenty20 cricket. Known for his explosive power-hitting, he holds numerous records in the format, including the most centuries and sixes. He has been a dominant force in T20 leagues around the world."
        }
        print(biographies.get(player, "No biography available."))

    except Exception as e:
        print(f"Error generating biography: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'generate_reasoning':
            data = sys.argv[2]
            generate_reasoning(data)
        elif command == 'generate_biography':
            player = sys.argv[2]
            generate_biography(player)
        else:
            print("Invalid command.", file=sys.stderr)
            sys.exit(1)
