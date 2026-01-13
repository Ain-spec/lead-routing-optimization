"""
Confidence vs Performance Visualization
Bubble chart showing relationship between data confidence and performance scores
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
    'at_risk': '#F44336'
}

df = pd.read_csv('analysis/performance_scores.csv')
df_viz = df[df['total_opps'] >= 3].copy()

classification_colors = {
    'High Performer': COLORS['high_performer'],
    'Above Average': COLORS['above_average'],
    'Average': COLORS['average'],
    'Below Average': COLORS['below_average'],
    'At-Risk': COLORS['at_risk']
}

fig, ax = plt.subplots(figsize=(15, 10), facecolor='white')
ax.set_facecolor('#FAFAFA')

for classification, color in classification_colors.items():
    mask = df_viz['performance_classification'] == classification
    if mask.sum() > 0:
        ax.scatter(df_viz[mask]['confidence_multiplier'], 
                  df_viz[mask]['final_performance_score'],
                  s=df_viz[mask]['total_opps'] * 45,
                  c=color, alpha=0.6, edgecolors='white', linewidth=2,
                  label=classification)

ax.axvline(0.43, color='#F44336', linestyle='--', linewidth=2, alpha=0.7,
          label='Low Confidence Cutoff (3 opps)')
ax.axvline(1.0, color='#00C853', linestyle='--', linewidth=2, alpha=0.7,
          label='Full Confidence (7+ opps)')

ax.set_xlabel('Confidence Multiplier', fontsize=14, fontweight='600', color='#212121')
ax.set_ylabel('Final Performance Score', fontsize=14, fontweight='600', color='#212121')
ax.set_title('Confidence vs Performance Analysis\n(Bubble Size = Number of Opportunities)', 
             fontsize=18, fontweight='700', color='#212121', pad=20)

legend1 = ax.legend(loc='upper left', fontsize=11, frameon=True, 
                   fancybox=True, shadow=True, framealpha=0.95, 
                   edgecolor='#BDBDBD', title='Classification')

size_legend_elements = [
    plt.scatter([], [], s=5*45, c='gray', alpha=0.6, edgecolors='white', linewidth=2),
    plt.scatter([], [], s=10*45, c='gray', alpha=0.6, edgecolors='white', linewidth=2),
    plt.scatter([], [], s=20*45, c='gray', alpha=0.6, edgecolors='white', linewidth=2)
]
legend2 = ax.legend(size_legend_elements, ['5 opps', '10 opps', '20 opps'],
                   loc='lower left', fontsize=11, frameon=True,
                   fancybox=True, shadow=True, framealpha=0.95,
                   edgecolor='#BDBDBD', title='Sample Size')

ax.add_artist(legend1)

ax.grid(True, alpha=0.2, color='#9E9E9E')
ax.axhline(0, color='#212121', linewidth=1, alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/06_confidence_vs_performance.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()