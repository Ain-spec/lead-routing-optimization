"""
Data Generation Script
Generates simulated BD-Sales opportunity data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
np.random.seed(42)
NUM_OPPORTUNITIES = 2200
NUM_BD_REPS = 18
NUM_SALES_REPS = 23
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Generate BD and Sales rep IDs
bd_reps = [f'BD_{str(i+1).zfill(3)}' for i in range(NUM_BD_REPS)]
sales_reps = [f'SR_{str(i+1).zfill(3)}' for i in range(NUM_SALES_REPS)]

# Generate opportunities
opportunities = []

for i in range(NUM_OPPORTUNITIES):
    # Random pairing
    bd_rep = np.random.choice(bd_reps)
    sales_rep = np.random.choice(sales_reps)
    
    # Create chemistry factor for pairing
    pairing_key = f"{bd_rep}_{sales_rep}"
    np.random.seed(hash(pairing_key) % 2**32)
    chemistry = np.random.normal(0, 0.3)
    
    # Generate dates
    created_date = START_DATE + timedelta(days=np.random.randint(0, (END_DATE - START_DATE).days))
    
    # Generate outcome based on chemistry
    outcome_prob = 0.25 + chemistry
    outcome_rand = np.random.random()
    
    if outcome_rand < outcome_prob:
        outcome = 'Closed Won'
        current_stage = 'Closed Won'
        days_in_stage = np.random.randint(1, 30)
    elif outcome_rand < outcome_prob + 0.30:
        outcome = 'Closed Lost'
        current_stage = 'Closed Lost'
        days_in_stage = np.random.randint(1, 30)
    else:
        outcome = 'Open'
        current_stage = np.random.choice(['Qualification', 'Proposal', 'Negotiation'])
        days_in_stage = np.random.randint(1, 120)
    
    # Generate deal value
    base_value = np.random.lognormal(10.8, 0.6)
    deal_value = max(5000, min(500000, base_value))
    
    # Calculate closed date
    if outcome in ['Closed Won', 'Closed Lost']:
        days_to_close = np.random.randint(30, 180)
        closed_date = created_date + timedelta(days=days_to_close)
    else:
        closed_date = None
    
    opportunities.append({
        'opportunity_id': f'OPP_{str(i+1).zfill(4)}',
        'bd_rep_id': bd_rep,
        'sales_rep_id': sales_rep,
        'created_date': created_date,
        'closed_date': closed_date,
        'outcome': outcome,
        'current_stage': current_stage,
        'days_in_current_stage': days_in_stage,
        'deal_value': round(deal_value, 2)
    })
    
    # Reset seed for next iteration
    np.random.seed(42 + i)

# Create DataFrame
df = pd.DataFrame(opportunities)

# Save to CSV
df.to_csv('data/opportunities.csv', index=False)

print(f"Generated {len(df)} opportunities")
print(f"BD Reps: {df['bd_rep_id'].nunique()}")
print(f"Sales Reps: {df['sales_rep_id'].nunique()}")
print(f"Unique pairings: {df.groupby(['bd_rep_id', 'sales_rep_id']).ngroups}")