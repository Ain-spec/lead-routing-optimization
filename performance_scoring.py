"""
Performance Scoring
Calculates final performance scores using percentile-based classification
"""

import pandas as pd
import numpy as np

# Configuration
CONFIDENCE_THRESHOLD = 7
EQUAL_WEIGHTS = {
    'win_rate': 0.25,
    'early_death': 0.25,
    'stale_pipeline': 0.25,
    'deal_size': 0.25
}

print("Loading pair metrics...")
df = pd.read_csv('analysis/pair_metrics.csv')

print("Calculating performance scores...")

# Calculate weighted scores for each metric
df['win_rate_weighted_score'] = df['win_rate_deviation_pct'] * EQUAL_WEIGHTS['win_rate']
df['early_death_weighted_score'] = -df['early_death_deviation_pct'] * EQUAL_WEIGHTS['early_death']
df['stale_pipeline_weighted_score'] = -df['stale_rate_deviation_pct'] * EQUAL_WEIGHTS['stale_pipeline']
df['deal_size_weighted_score'] = df['deal_size_deviation_pct'] * EQUAL_WEIGHTS['deal_size']

# Calculate total weighted score
df['total_weighted_score'] = (
    df['win_rate_weighted_score'] +
    df['early_death_weighted_score'] +
    df['stale_pipeline_weighted_score'] +
    df['deal_size_weighted_score']
)

# Apply confidence multiplier
df['confidence_multiplier'] = df['total_opps'].apply(lambda x: min(x / CONFIDENCE_THRESHOLD, 1.0))
df['final_performance_score'] = df['total_weighted_score'] * df['confidence_multiplier']

print("Applying percentile-based classification...")

# Calculate percentiles for pairs with sufficient data
df_for_percentiles = df[df['total_opps'] >= 3].copy()

p10 = np.percentile(df_for_percentiles['final_performance_score'], 10)
p25 = np.percentile(df_for_percentiles['final_performance_score'], 25)
p50 = np.percentile(df_for_percentiles['final_performance_score'], 50)
p75 = np.percentile(df_for_percentiles['final_performance_score'], 75)

print(f"Percentile thresholds: 10th={p10:.2f}, 25th={p25:.2f}, 50th={p50:.2f}, 75th={p75:.2f}")

# Classify performance
def classify_performance(row):
    if row['total_opps'] < 3:
        return "Insufficient Data"
    elif row['confidence_multiplier'] < 0.43:
        return "Low Confidence"
    elif row['final_performance_score'] >= p75:
        return "High Performer"
    elif row['final_performance_score'] >= p50:
        return "Above Average"
    elif row['final_performance_score'] >= p25:
        return "Average"
    elif row['final_performance_score'] >= p10:
        return "Below Average"
    else:
        return "At-Risk"

df['performance_classification'] = df.apply(classify_performance, axis=1)

# Store percentile thresholds
df['percentile_75th'] = p75
df['percentile_50th'] = p50
df['percentile_25th'] = p25
df['percentile_10th'] = p10

# Identify strengths and concerns
df['strength_high_win_rate'] = df['win_rate_deviation_pct'] > 20
df['strength_low_early_death'] = df['early_death_deviation_pct'] < -20
df['strength_low_stale'] = df['stale_rate_deviation_pct'] < -20
df['strength_high_deal_size'] = df['deal_size_deviation_pct'] > 20

df['concern_low_win_rate'] = df['win_rate_deviation_pct'] < -20
df['concern_high_early_death'] = df['early_death_deviation_pct'] > 20
df['concern_high_stale'] = df['stale_rate_deviation_pct'] > 20
df['concern_low_deal_size'] = df['deal_size_deviation_pct'] < -20

strength_cols = [col for col in df.columns if col.startswith('strength_')]
concern_cols = [col for col in df.columns if col.startswith('concern_')]

df['total_strengths'] = df[strength_cols].sum(axis=1)
df['total_concerns'] = df[concern_cols].sum(axis=1)

print("Generating BD recommendations...")

# Generate BD-specific recommendations
recommendations = []

for bd_id in sorted(df['bd_rep_id'].unique()):
    bd_pairs = df[df['bd_rep_id'] == bd_id].copy()
    bd_pairs = bd_pairs[bd_pairs['total_opps'] >= 3]
    
    if len(bd_pairs) == 0:
        continue
    
    bd_pairs = bd_pairs.sort_values('final_performance_score', ascending=False)
    
    bd_p75 = bd_pairs['final_performance_score'].quantile(0.75)
    best_pairs = bd_pairs[bd_pairs['final_performance_score'] >= bd_p75].head(5)
    
    bd_p25 = bd_pairs['final_performance_score'].quantile(0.25)
    worst_pairs = bd_pairs[bd_pairs['final_performance_score'] <= bd_p25].tail(5)
    
    recommendations.append({
        'bd_rep_id': bd_id,
        'total_pairings': len(bd_pairs),
        'avg_performance_score': bd_pairs['final_performance_score'].mean(),
        'best_sales_reps': ', '.join(best_pairs['sales_rep_id'].tolist()),
        'worst_sales_reps': ', '.join(worst_pairs['sales_rep_id'].tolist()),
        'best_avg_score': best_pairs['final_performance_score'].mean() if len(best_pairs) > 0 else None,
        'worst_avg_score': worst_pairs['final_performance_score'].mean() if len(worst_pairs) > 0 else None,
        'num_best': len(best_pairs),
        'num_worst': len(worst_pairs)
    })

recommendations_df = pd.DataFrame(recommendations)

# Save results
print("Saving results...")
df.to_csv('analysis/performance_scores.csv', index=False)
recommendations_df.to_csv('analysis/bd_pairing_recommendations.csv', index=False)

print(df['performance_classification'].value_counts())