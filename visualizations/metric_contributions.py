"""
Metric Contributions Visualization
Compares metric performance between high performers and at-risk pairs
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

df = pd.read_csv('analysis/performance_scores.csv')
df_analyzed = df[df['total_opps'] >= 5].copy()

top_performers = df_analyzed.nlargest(20, 'final_performance_score')
bottom_performers = df_analyzed.nsmallest(20, 'final_performance_score')

metrics = ['win_rate_weighted_score', 'early_death_weighted_score', 
           'stale_pipeline_weighted_score', 'deal_size_weighted_score']
labels = ['Win Rate', 'Early Death\n(Lower is Better)', 
          'Stale Pipeline\n(Lower is Better)', 'Deal Size']

top_avg = [top_performers[m].mean() for m in metrics]
bottom_avg = [bottom_performers[m].mean() for m in metrics]

fig, ax = plt.subplots(figsize=(15, 9), facecolor='white')
ax.set_facecolor('#FAFAFA')

x = range(len(labels))
width = 0.38

top_colors = ['#00E676', '#00C853', '#00B248', '#009E3D']
bottom_colors = ['#FF5252', '#F44336', '#E53935', '#D32F2F']

bars1 = ax.bar([i - width/2 for i in x], top_avg, width, label='Top 20 Performers', 
               color=top_colors, edgecolor='white', linewidth=2, alpha=0.9)
bars2 = ax.bar([i + width/2 for i in x], bottom_avg, width, label='Bottom 20 Performers', 
               color=bottom_colors, edgecolor='white', linewidth=2, alpha=0.9)

ax.set_xlabel('Performance Metric', fontsize=15, fontweight='600', color='#212121')
ax.set_ylabel('Average Weighted Score Contribution', fontsize=15, fontweight='600', color='#212121')
ax.set_title('Metric Contributions: High Performers vs At-Risk Pairs\nWhat Separates Winners from Losers?', 
             fontsize=18, fontweight='700', color='#212121', pad=25)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, fontweight='500')

ax.legend(fontsize=13, frameon=True, fancybox=True, 
          shadow=True, framealpha=0.95, edgecolor='#BDBDBD', loc='upper right')

ax.grid(True, alpha=0.2, axis='y', color='#9E9E9E')
ax.axhline(0, color='#212121', linewidth=1.2, zorder=3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', 
                va='bottom' if height > 0 else 'top',
                fontsize=10, fontweight='600', color='#212121')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/05_metric_contributions.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()