"""
Top and Bottom Performing Pairs Visualization
Displays best and worst BD-Sales pairings side by side
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

COLORS = {
    'high_performer': '#00C853',
    'at_risk': '#F44336'
}

df = pd.read_csv('analysis/performance_scores.csv')
df_analyzed = df[df['total_opps'] >= 3].copy()

top_10 = df_analyzed.nlargest(10, 'final_performance_score').copy()
bottom_10 = df_analyzed.nsmallest(10, 'final_performance_score').copy()

top_10['pair_name'] = top_10['bd_rep_id'] + ' → ' + top_10['sales_rep_id']
bottom_10['pair_name'] = bottom_10['bd_rep_id'] + ' → ' + bottom_10['sales_rep_id']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11), facecolor='white')

for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAFA')

y_pos = np.arange(len(top_10))
colors_gradient = plt.cm.Greens(np.linspace(0.5, 0.9, len(top_10)))

bars1 = ax1.barh(y_pos, top_10['final_performance_score'], 
                 color=colors_gradient, edgecolor='white', linewidth=2, alpha=0.9,
                 height=0.7)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(top_10['pair_name'], fontsize=12, fontweight='500')
ax1.set_xlabel('Performance Score', fontsize=14, fontweight='600', color='#212121')
ax1.set_title('Top 10 High-Performing Pairs', 
              fontsize=18, fontweight='700', color=COLORS['high_performer'], pad=20)
ax1.grid(True, alpha=0.2, axis='x', color='#9E9E9E')
ax1.invert_yaxis()

for i, (idx, row) in enumerate(top_10.iterrows()):
    ax1.text(row['final_performance_score'] + 3, i, f"{row['final_performance_score']:.1f}", 
             va='center', fontsize=11, fontweight='600', color='#212121')

y_pos = np.arange(len(bottom_10))
colors_gradient = plt.cm.Reds(np.linspace(0.5, 0.9, len(bottom_10)))

bars2 = ax2.barh(y_pos, bottom_10['final_performance_score'], 
                 color=colors_gradient, edgecolor='white', linewidth=2, alpha=0.9,
                 height=0.7)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(bottom_10['pair_name'], fontsize=12, fontweight='500')
ax2.set_xlabel('Performance Score', fontsize=14, fontweight='600', color='#212121')
ax2.set_title('Bottom 10 At-Risk Pairs', 
              fontsize=18, fontweight='700', color=COLORS['at_risk'], pad=20)
ax2.grid(True, alpha=0.2, axis='x', color='#9E9E9E')
ax2.invert_yaxis()

for i, (idx, row) in enumerate(bottom_10.iterrows()):
    ax2.text(row['final_performance_score'] - 4, i, f"{row['final_performance_score']:.1f}", 
             va='center', ha='right', fontsize=11, fontweight='600', color='#212121')

for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDBDBD')
    ax.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/03_top_bottom_pairs.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()