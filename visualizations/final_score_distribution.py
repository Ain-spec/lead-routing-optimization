"""
Final Score Distribution Visualization
Displays histogram of performance scores with percentile thresholds
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

COLORS = {
    'high_performer': '#00C853',
    'above_average': '#2196F3',
    'average': '#9E9E9E',
    'below_average': '#FF9800',
    'at_risk': '#F44336',
    'background': '#FAFAFA'
}

df = pd.read_csv('analysis/performance_scores.csv')
df_analyzed = df[df['total_opps'] >= 3].copy()

fig, ax = plt.subplots(figsize=(14, 9), facecolor='white')
ax.set_facecolor(COLORS['background'])

p10 = df_analyzed['percentile_10th'].iloc[0]
p25 = df_analyzed['percentile_25th'].iloc[0]
p50 = df_analyzed['percentile_50th'].iloc[0]
p75 = df_analyzed['percentile_75th'].iloc[0]

bins = 30
n, bins_edges, patches = ax.hist(df_analyzed['final_performance_score'], bins=bins,
                                  edgecolor='white', linewidth=1.5, alpha=0.9)

for i, patch in enumerate(patches):
    bin_center = (bins_edges[i] + bins_edges[i+1]) / 2
    if bin_center >= p75:
        patch.set_facecolor(COLORS['high_performer'])
    elif bin_center >= p50:
        patch.set_facecolor(COLORS['above_average'])
    elif bin_center >= p25:
        patch.set_facecolor(COLORS['average'])
    elif bin_center >= p10:
        patch.set_facecolor(COLORS['below_average'])
    else:
        patch.set_facecolor(COLORS['at_risk'])

percentiles = [
    (p75, 'High Performer (75th)', COLORS['high_performer']),
    (p50, 'Above Average (50th)', COLORS['above_average']),
    (p25, 'Average (25th)', COLORS['average']),
    (p10, 'At-Risk (10th)', COLORS['at_risk'])
]

for value, label, color in percentiles:
    ax.axvline(value, color=color, linestyle='--', linewidth=3, alpha=0.8, label=label)

ax.set_xlabel('Performance Score', fontsize=14, fontweight='600', color='#212121')
ax.set_ylabel('Number of Pairings', fontsize=14, fontweight='600', color='#212121')
ax.set_title('Performance Score Distribution with Percentile Thresholds', 
             fontsize=18, fontweight='700', color='#212121', pad=20)

ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True, 
          framealpha=0.95, edgecolor='#BDBDBD', loc='upper right')
ax.grid(True, alpha=0.2, color='#9E9E9E')

summary_text = (f"Sample Size: {len(df_analyzed)} pairs\n"
                f"Mean: {df_analyzed['final_performance_score'].mean():.1f}\n"
                f"Median: {df_analyzed['final_performance_score'].median():.1f}")

ax.text(0.02, 0.98, summary_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                  edgecolor='#BDBDBD', alpha=0.95, linewidth=1.5),
        fontweight='500', color='#424242')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/01_final_score_distribution.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()