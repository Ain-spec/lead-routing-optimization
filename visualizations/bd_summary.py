"""
BD Summary Visualization
Shows average performance across all pairings for each BD rep
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
df_analyzed = df[df['total_opps'] >= 3].copy()

bd_stats = df_analyzed.groupby('bd_rep_id', as_index=False).agg({
    'final_performance_score': 'mean',
    'total_opps': 'sum',
    'sales_rep_id': 'count'
})
bd_stats.columns = ['bd_rep_id', 'avg_performance', 'total_opportunities', 'num_pairings']
bd_stats = bd_stats.sort_values('avg_performance', ascending=True)

fig, ax = plt.subplots(figsize=(15, 11), facecolor='white')
ax.set_facecolor('#FAFAFA')

colors = []
for perf in bd_stats['avg_performance']:
    if perf < -20:
        colors.append('#D32F2F')
    elif perf < -10:
        colors.append('#E53935')
    elif perf < 0:
        colors.append('#FF5252')
    elif perf < 10:
        colors.append('#42A5F5')
    elif perf < 20:
        colors.append('#1E88E5')
    else:
        colors.append('#00C853')

bars = ax.barh(bd_stats['bd_rep_id'], bd_stats['avg_performance'], 
               color=colors, edgecolor='white', linewidth=2, alpha=0.9,
               height=0.7)

ax.axvline(0, color='#212121', linewidth=1.5, linestyle='-', zorder=3)
ax.set_xlabel('Average Performance Score Across All Pairings', fontsize=14, fontweight='600', color='#212121')
ax.set_ylabel('BD Rep ID', fontsize=14, fontweight='600', color='#212121')
ax.set_title('BD Rep Performance Summary\n(Average Across All Sales Rep Pairings)', 
             fontsize=18, fontweight='700', color='#212121', pad=25)
ax.grid(True, alpha=0.2, axis='x', color='#9E9E9E')

for i, (idx, row) in enumerate(bd_stats.iterrows()):
    label_text = f"{row['avg_performance']:.1f} ({int(row['num_pairings'])} pairs)"
    
    if row['avg_performance'] > 0:
        ax.text(row['avg_performance'] + 1, i, label_text, 
                va='center', ha='left', fontsize=10, fontweight='500', color='#212121')
    else:
        ax.text(row['avg_performance'] - 1, i, label_text, 
                va='center', ha='right', fontsize=10, fontweight='500', color='#212121')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

ax.tick_params(axis='y', labelsize=11, pad=5)

explanation_text = (
    "Note: Scores represent average deviation from each BD's baseline.\n"
    "Higher scores = More pairings outperform their average\n"
    "This measures pairing consistency, not absolute BD quality."
)
ax.text(0.98, 0.02, explanation_text, transform=ax.transAxes, 
        fontsize=9, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF9C4', 
                  edgecolor='#FBC02D', alpha=0.9, linewidth=2),
        fontweight='400', color='#424242', style='italic')

plt.tight_layout()
plt.savefig('visualizations/output/07_bd_summary.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()