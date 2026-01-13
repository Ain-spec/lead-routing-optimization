"""
Performance Heatmap Visualization
BD-Sales matrix showing all pairing performance scores
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("white")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

df = pd.read_csv('analysis/performance_scores.csv')
df_analyzed = df[df['total_opps'] >= 3].copy()

pivot_table = df_analyzed.pivot(index='bd_rep_id', 
                                  columns='sales_rep_id', 
                                  values='final_performance_score')

fig, ax = plt.subplots(figsize=(20, 12), facecolor='white')

sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Performance Score', 'shrink': 0.8},
            linewidths=1.5, linecolor='white', ax=ax,
            vmin=-100, vmax=100,
            annot_kws={'fontsize': 9, 'fontweight': '500'})

ax.set_xlabel('Sales Rep ID', fontsize=15, fontweight='600', color='#212121', labelpad=10)
ax.set_ylabel('BD Rep ID', fontsize=15, fontweight='600', color='#212121', labelpad=10)
ax.set_title('BD-Sales Pairing Performance Heatmap\n(Pairs with 3+ Opportunities)', 
             fontsize=19, fontweight='700', color='#212121', pad=25)

plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontweight='500', fontsize=11)
plt.setp(ax.get_yticklabels(), rotation=0, fontweight='500', fontsize=11)

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12, labelcolor='#212121')
cbar.set_label('Performance Score', fontsize=14, fontweight='600', color='#212121')

plt.tight_layout()
plt.savefig('visualizations/output/04_performance_heatmap.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()