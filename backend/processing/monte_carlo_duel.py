#!/usr/bin/env python3
"""
Monte Carlo duel simulator: Batsman vs Bowler

Reads backend/data/player_features.csv (created earlier).
Simulates a short duel of B balls (default 6) for N trials (default 10000).

Outputs:
 - survival probability (batsman survives all B balls)
 - expected runs scored in duel
 - dismissal probability
 - short reasoning text

Notes / assumptions:
 - player_features.csv must have rows keyed by 'format' and 'player_name'
 - batting per-ball behavior is approximated from strike_rate, boundary_percent, etc.
 - bowler pressure is blended with bowler wicket probability to compute per-ball wicket chance
 - model is intentionally simple, tunable, and designed for MVP/hypothetical use.
"""

import argparse
import os
import sys
import math
import random
import numpy as np
import pandas as pd

BASE_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
PLAYER_FEATURES_CSV = os.path.join(BASE_DATA, "player_features.csv")

# Tunable blending weights
ALPHA_WICKET = 0.6   # weight for bowler wicket probability vs batter dismissal rate
BOWLER_PRESSURE_FACTOR = 1.0  # multiplier on wicket probability if bowler unusually high

# Minimal default distribution shape for non-boundary runs
DEFAULT_RUN_DISTRIBUTION = {0: 0.45, 1: 0.35, 2: 0.08, 3: 0.02}  # leftover mass after boundaries

def load_features(csv_path=PLAYER_FEATURES_CSV):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"player_features.csv not found at {csv_path}. Run generate_player_features.py first.")
    df = pd.read_csv(csv_path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

def find_player_row(df, player_name, fmt):
    # exact match first
    row = df[(df['format'].str.upper() == fmt.upper()) & (df['player_name'].str.lower() == player_name.lower())]
    if not row.empty:
        return row.iloc[0].to_dict()
    # try case-insensitive contains
    row = df[(df['format'].str.upper() == fmt.upper()) & (df['player_name'].str.lower().str.contains(player_name.lower()))]
    if not row.empty:
        return row.iloc[0].to_dict()
    return None

def build_ball_model(batter_row, bowler_row, df_all):
    """
    Build a simple per-ball PMF and wicket probability by combining batter and bowler stats.

    Inputs: batter_row and bowler_row are dicts (or None if absent)
    Returns: dict with keys:
      - p_wicket (per-ball)
      - run_probs: dict mapping runs -> probability (excluding wicket)
      - expected_runs_per_ball
      - notes (list) for reasoning
    """

    notes = []
    # Default baseline league averages computed from df_all to normalize if available
    league_sr = None
    league_econ = None
    league_wicket_prob = None
    try:
        # compute approximate league averages excluding zeros
        tmp = df_all.copy()
        # strike_rate column may exist or not; compute if missing
        if 'strike_rate' in tmp.columns:
            league_sr = tmp['strike_rate'].replace([np.inf, -np.inf], np.nan).dropna().mean()
        if 'economy_rate' in tmp.columns:
            league_econ = tmp['economy_rate'].replace([np.inf, -np.inf], np.nan).dropna().mean()
        # wicket prob per ball average among bowlers
        if 'wicket_probability' in tmp.columns:
            league_wicket_prob = tmp['wicket_probability'].replace([np.inf, -np.inf], np.nan).dropna().mean()
    except Exception:
        league_sr = league_econ = league_wicket_prob = None

    # Batter stats fallback defaults
    batter_sr = None
    batter_boundary_pct = None
    batter_dismissal_prob = None
    if batter_row is not None:
        batter_sr = float(batter_row.get('strike_rate') or 0.0)
        batter_boundary_pct = float(batter_row.get('boundary_percent') or 0.0)
        # use dismissal_probability if present (dismissals/balls_faced)
        batter_dismissal_prob = float(batter_row.get('dismissal_probability') or 0.0)
        notes.append(f"Batter SR={batter_sr:.1f}, boundary%={batter_boundary_pct:.2f}, dismiss_prob={batter_dismissal_prob:.5f}")
    else:
        # fallback to league SR or a reasonable default
        batter_sr = league_sr if league_sr and not math.isnan(league_sr) else 60.0
        batter_boundary_pct = 6.0  # percent
        batter_dismissal_prob = 0.02
        notes.append("Batter stats missing; using league/default approximations")

    # Bowler stats fallback defaults
    bowler_wicket_prob = None
    bowler_econ = None
    if bowler_row is not None:
        bowler_wicket_prob = float(bowler_row.get('wicket_probability') or 0.0)
        bowler_econ = float(bowler_row.get('economy_rate') or 0.0)
        notes.append(f"Bowler wicket_prob={bowler_wicket_prob:.5f}, econ={bowler_econ:.2f}")
    else:
        bowler_wicket_prob = league_wicket_prob if league_wicket_prob and not math.isnan(league_wicket_prob) else 0.02
        bowler_econ = league_econ if league_econ and not math.isnan(league_econ) else 6.0
        notes.append("Bowler stats missing; using league/default approximations")

    # Combine wicket probabilities: weighted blend of bowler's wicket probability and batter's dismissal probability
    p_wicket = ALPHA_WICKET * bowler_wicket_prob + (1 - ALPHA_WICKET) * batter_dismissal_prob

    # Apply bowler pressure factor
    p_wicket *= BOWLER_PRESSURE_FACTOR

    # clip p_wicket to reasonable bounds [0.001, 0.5]
    p_wicket = max(0.0005, min(p_wicket, 0.5))

    # Expected runs per ball from batter SR
    r_b = batter_sr / 100.0  # runs per ball baseline

    # Adjust runs expectation according to bowler econ vs league
    if league_econ and league_econ > 0:
        # If bowler econ is better (lower) than league, reduce expected runs proportionally
        econ_ratio = bowler_econ / league_econ
        # compress ratio to reasonable multiplier between 0.6 and 1.4
        econ_mult = min(max(econ_ratio, 0.6), 1.4)
        r_b *= (2.0 - econ_mult) / 1.0  # if econ_mult low (<1) this increases? invert logic:
        # Better to scale inversely: lower econ -> slightly lower runs
        r_b = r_b * (1.0 / econ_mult)
    # ensure non-negative
    r_b = max(0.01, r_b)

    # boundary probabilities derived from boundary_percent
    # boundary_percent is percent of balls resulting in boundary (4 or 6) for batter
    boundary_fraction = batter_boundary_pct / 100.0
    # split between 4 and 6 heuristically: 4s are more likely than 6s; assume 4:6 = 4:1 ratio
    prob_4 = boundary_fraction * 0.8
    prob_6 = boundary_fraction * 0.2

    # Ensure boundary probabilities do not exceed plausible max
    if prob_4 + prob_6 > 0.6:
        scale = 0.6 / (prob_4 + prob_6)
        prob_4 *= scale
        prob_6 *= scale

    # Remaining expected runs to distribute to {0,1,2,3}
    runs_from_bounds = 4 * prob_4 + 6 * prob_6
    # expected runs from non-boundary outcomes
    remaining_expected = max(0.0, r_b - runs_from_bounds)

    # We'll construct a simple discrete distribution for non-boundary outcomes:
    # Use DEFAULT_RUN_DISTRIBUTION ratios scaled to sum to non_boundary_mass
    non_bound_mass = max(0.0, 1.0 - p_wicket - (prob_4 + prob_6))
    if non_bound_mass <= 0:
        # edge case: nearly certain wicket or full mass consumed by boundaries
        run_probs = {0: max(0.0, 1.0 - p_wicket - (prob_4 + prob_6))}
        if prob_4 > 0:
            run_probs[4] = prob_4
        if prob_6 > 0:
            run_probs[6] = prob_6
    else:
        # base distribution for 0/1/2/3
        base = DEFAULT_RUN_DISTRIBUTION.copy()
        # normalize default base
        total_base = sum(base.values())
        for k in base:
            base[k] = base[k] / total_base
        # convert base to probabilities summing to non_bound_mass
        run_probs = {k: base[k] * non_bound_mass for k in base}
        # add boundaries
        run_probs[4] = prob_4
        run_probs[6] = prob_6
        # small numerical cleanup
        # ensure total mass (including wicket) is 1.0 (or close)
        total_mass = p_wicket + sum(run_probs.values())
        # if <1, put leftover into 0-run
        if total_mass < 0.999999:
            leftover = 1.0 - total_mass
            run_probs[0] = run_probs.get(0, 0) + leftover

    # compute expected runs per ball from this pmf (ignoring wicket)
    expected_runs_ball = sum(r * prob for r, prob in run_probs.items())

    model = {
        'p_wicket': p_wicket,
        'run_probs': run_probs,
        'expected_runs_per_ball': expected_runs_ball,
        'notes': notes
    }
    return model

def simulate_duel(model, balls=6, trials=10000, rng_seed=None):
    """
    Run Monte Carlo trials. Each trial simulate 'balls' balls until either wicket or balls exhausted.
    Returns summary dict.
    """
    if rng_seed is not None:
        random.seed(rng_seed)
        np.random.seed(rng_seed)

    p_wicket = model['p_wicket']
    run_probs = model['run_probs']

    # build arrays for faster sampling
    outcomes = sorted(run_probs.keys())  # e.g. [0,1,2,3,4,6]
    probs = np.array([run_probs[o] for o in outcomes])
    # normalize in case small float error
    probs = probs / probs.sum()

    total_runs = np.zeros(trials, dtype=float)
    dismissed = np.zeros(trials, dtype=int)
    balls_used = np.zeros(trials, dtype=int)

    for t in range(trials):
        runs = 0.0
        out_flag = 0
        used = 0
        for b in range(balls):
            used += 1
            # first check wicket
            if random.random() < p_wicket:
                out_flag = 1
                break
            # otherwise sample runs
            r = np.random.choice(outcomes, p=probs)
            runs += r
        total_runs[t] = runs
        dismissed[t] = out_flag
        balls_used[t] = used

    surv_prob = 1.0 - dismissed.mean()
    exp_runs = total_runs.mean()
    dismissal_prob = dismissed.mean()
    # percentiles
    runs_p50 = np.percentile(total_runs, 50)
    runs_p90 = np.percentile(total_runs, 90)
    runs_p10 = np.percentile(total_runs, 10)

    return {
        'trials': trials,
        'balls': balls,
        'survival_probability': surv_prob,
        'expected_runs': float(exp_runs),
        'dismissal_probability': dismissal_prob,
        'runs_p50': float(runs_p50),
        'runs_p10': float(runs_p10),
        'runs_p90': float(runs_p90)
    }

def pretty_reason(batter_row, bowler_row, model):
    parts = []
    if batter_row is not None:
        parts.append(f"{batter_row.get('player_name')} (SR={batter_row.get('strike_rate', 'NA'):.1f}, boundary%={batter_row.get('boundary_percent', 0):.1f})")
    if bowler_row is not None:
        parts.append(f"{bowler_row.get('player_name')} (wicket_prob={bowler_row.get('wicket_probability', 0):.4f}, econ={bowler_row.get('economy_rate', 'NA')})")
    parts.append(f"Per-ball wicket chance blended = {model['p_wicket']:.3%}")
    parts.append(f"Expected runs/ball ≈ {model['expected_runs_per_ball']:.3f}")
    return " vs ".join(parts)

def main_cli():
    parser = argparse.ArgumentParser(description="Monte Carlo Batsman vs Bowler Duel Simulator")
    parser.add_argument("--batsman", required=True, help="Batsman name (partial matches allowed)")
    parser.add_argument("--bowler", required=True, help="Bowler name (partial matches allowed)")
    parser.add_argument("--format", default="ODI", help="Format: ODI/T20/TEST (default ODI)")
    parser.add_argument("--balls", type=int, default=6, help="Number of balls to simulate (default 6)")
    parser.add_argument("--trials", type=int, default=10000, help="Monte Carlo trials (default 10000)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    args = parser.parse_args()

    df = load_features()
    batter_row = find_player_row(df, args.batsman, args.format)
    bowler_row = find_player_row(df, args.bowler, args.format)

    if batter_row is None:
        print(f"⚠️ Batsman '{args.batsman}' not found for format {args.format}. Try partial name or check player_features.csv")
    if bowler_row is None:
        print(f"⚠️ Bowler '{args.bowler}' not found for format {args.format}.")

    model = build_ball_model(batter_row, bowler_row, df)
    sim = simulate_duel(model, balls=args.balls, trials=args.trials, rng_seed=args.seed)

    print("\n=== Monte Carlo Duel Results ===")
    print(f"Batsman: {args.batsman}")
    print(f"Bowler: {args.bowler}")
    print(f"Format: {args.format}")
    print(f"Balls simulated per trial: {args.balls}")
    print(f"Trials: {args.trials}")
    print()
    print(f"Survival probability (no dismissal in {args.balls} balls): {sim['survival_probability']:.3%}")
    print(f"Dismissal probability during duel: {sim['dismissal_probability']:.3%}")
    print(f"Expected runs in duel: {sim['expected_runs']:.3f}")
    print(f"Runs distribution (p10 / p50 / p90): {sim['runs_p10']:.1f} / {sim['runs_p50']:.1f} / {sim['runs_p90']:.1f}")
    print()
    print("Reasoning (approx):")
    print(pretty_reason(batter_row, bowler_row, model))
    print("\nNotes:")
    for n in model['notes']:
        print(" -", n)
    print("\nCaveats: This model approximates per-ball distributions from aggregate stats (SR, boundary%, wicket rates).")
    print("Tune ALPHA_WICKET and BOWLER_PRESSURE_FACTOR in the script for different weighting behavior.")

if __name__ == "__main__":
    main_cli()
