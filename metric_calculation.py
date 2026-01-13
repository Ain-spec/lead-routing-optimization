"""
Metric Calculation
Calculates performance metrics for each BD-Sales pairing
"""

import pandas as pd
import numpy as np

print("Loading opportunities data...")
opportunities = pd.read_csv('data/opportunities.csv')

print("Calculating pairing metrics...")

# Create a complete list of all BD-Sales pairs that exist
all_pairs = opportunities.groupby(['bd_rep_id', 'sales_rep_id']).size()

# Calculate total opportunities per pair
total_opps = opportunities.groupby(['bd_rep_id', 'sales_rep_id']).size()

# Calculate counts by outcome
total_open = opportunities[opportunities['outcome'] == 'Open'].groupby(['bd_rep_id', 'sales_rep_id']).size()
total_won = opportunities[opportunities['outcome'] == 'Closed Won'].groupby(['bd_rep_id', 'sales_rep_id']).size()
total_lost = opportunities[opportunities['outcome'] == 'Closed Lost'].groupby(['bd_rep_id', 'sales_rep_id']).size()

# Reindex to ensure all pairs are included (fill missing with 0)
total_open = total_open.reindex(total_opps.index, fill_value=0)
total_won = total_won.reindex(total_opps.index, fill_value=0)
total_lost = total_lost.reindex(total_opps.index, fill_value=0)

# Calculate total decided (won + lost)
total_decided = total_won + total_lost

# Metric 1: Win Rate
win_rate_pct = (total_won / total_decided * 100).fillna(0)

# Metric 2: Early Death Rate
early_death = opportunities[
    (opportunities['outcome'] == 'Closed Lost') & 
    (opportunities['days_in_current_stage'] <= 14)
].groupby(['bd_rep_id', 'sales_rep_id']).size()

early_death = early_death.reindex(total_opps.index, fill_value=0)
early_death_rate_pct = (early_death / total_lost * 100).fillna(0)

# Metric 3: Stale Pipeline Rate
stale = opportunities[
    (opportunities['outcome'] == 'Open') & 
    (opportunities['days_in_current_stage'] > 90)
].groupby(['bd_rep_id', 'sales_rep_id']).size()

stale = stale.reindex(total_opps.index, fill_value=0)
stale_rate_pct = (stale / total_opps * 100).fillna(0)

# Metric 4: Average Deal Size
avg_deal_size = opportunities.groupby(['bd_rep_id', 'sales_rep_id'])['deal_value'].mean()
avg_deal_size = avg_deal_size.reindex(total_opps.index, fill_value=0)

# Calculate BD-level averages (for baseline comparison)
bd_won = opportunities[opportunities['outcome'] == 'Closed Won'].groupby('bd_rep_id').size()
bd_lost = opportunities[opportunities['outcome'] == 'Closed Lost'].groupby('bd_rep_id').size()
bd_decided = bd_won.add(bd_lost, fill_value=0)
bd_avg_win_rate_pct = (bd_won / bd_decided * 100).fillna(0)

bd_early_death = opportunities[
    (opportunities['outcome'] == 'Closed Lost') & 
    (opportunities['days_in_current_stage'] <= 14)
].groupby('bd_rep_id').size()
bd_total_lost = opportunities[opportunities['outcome'] == 'Closed Lost'].groupby('bd_rep_id').size()
bd_avg_early_death_rate_pct = (bd_early_death / bd_total_lost * 100).fillna(0)

bd_stale = opportunities[
    (opportunities['outcome'] == 'Open') & 
    (opportunities['days_in_current_stage'] > 90)
].groupby('bd_rep_id').size()
bd_total_opps = opportunities.groupby('bd_rep_id').size()
bd_avg_stale_rate_pct = (bd_stale / bd_total_opps * 100).fillna(0)

bd_avg_deal_size = opportunities.groupby('bd_rep_id')['deal_value'].mean()

# Create DataFrame with all metrics
metrics_df = pd.DataFrame({
    'bd_rep_id': total_opps.index.get_level_values(0),
    'sales_rep_id': total_opps.index.get_level_values(1),
    'total_opps': total_opps.values,
    'total_open': total_open.values,
    'total_closed_won': total_won.values,
    'total_closed_lost': total_lost.values,
    'total_decided': total_decided.values,
    'win_rate_pct': win_rate_pct.values,
    'early_death_rate_pct': early_death_rate_pct.values,
    'stale_rate_pct': stale_rate_pct.values,
    'avg_deal_size': avg_deal_size.values
})

# Map BD averages to each row
metrics_df['bd_avg_win_rate_pct'] = metrics_df['bd_rep_id'].map(bd_avg_win_rate_pct)
metrics_df['bd_avg_early_death_rate_pct'] = metrics_df['bd_rep_id'].map(bd_avg_early_death_rate_pct)
metrics_df['bd_avg_stale_rate_pct'] = metrics_df['bd_rep_id'].map(bd_avg_stale_rate_pct)
metrics_df['bd_avg_deal_size'] = metrics_df['bd_rep_id'].map(bd_avg_deal_size)

# Calculate percentage deviations from BD baseline
metrics_df['win_rate_deviation_pct'] = (
    (metrics_df['win_rate_pct'] - metrics_df['bd_avg_win_rate_pct']) / 
    metrics_df['bd_avg_win_rate_pct'].replace(0, 1) * 100
).fillna(0)

metrics_df['early_death_deviation_pct'] = (
    (metrics_df['early_death_rate_pct'] - metrics_df['bd_avg_early_death_rate_pct']) / 
    metrics_df['bd_avg_early_death_rate_pct'].replace(0, 1) * 100
).fillna(0)

metrics_df['stale_rate_deviation_pct'] = (
    (metrics_df['stale_rate_pct'] - metrics_df['bd_avg_stale_rate_pct']) / 
    metrics_df['bd_avg_stale_rate_pct'].replace(0, 1) * 100
).fillna(0)

metrics_df['deal_size_deviation_pct'] = (
    (metrics_df['avg_deal_size'] - metrics_df['bd_avg_deal_size']) / 
    metrics_df['bd_avg_deal_size'] * 100
).fillna(0)

# Save to CSV
metrics_df.to_csv('analysis/pair_metrics.csv', index=False)

print(f"Calculated metrics for {len(metrics_df)} pairings")
print("Saved to analysis/pair_metrics.csv")