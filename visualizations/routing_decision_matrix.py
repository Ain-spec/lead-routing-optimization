"""
Routing Decision Matrix Visualization
Lookup table showing which sales reps to route to for each BD
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("white")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

recs = pd.read_csv('analysis/bd_pairing_recommendations.csv')

all_sales_reps = set()
for bd_reps in recs['best_sales_reps']:
    all_sales_reps.update([r.strip() for r in bd_reps.split(',')])
for bd_reps in recs['worst_sales_reps']:
    all_sales_reps.update([r.strip() for r in bd_reps.split(',')])

all_sales_reps = sorted(list(all_sales_reps))
all_bds = sorted(recs['bd_rep_id'].tolist())

matrix = pd.DataFrame(0, index=all_bds, columns=all_sales_reps)

for idx, row in recs.iterrows():
    bd = row['bd_rep_id']
    
    best_reps = [r.strip() for r in row['best_sales_reps'].split(',')]
    for rep in best_reps:
        if rep in matrix.columns:
            matrix.loc[bd, rep] = 1
    
    worst_reps = [r.strip() for r in row['worst_sales_reps'].split(',')]
    for rep in worst_reps:
        if rep in matrix.columns:
            matrix.loc[bd, rep] = -1

fig, ax = plt.subplots(figsize=(22, 12), facecolor='white')

colors = ['#F44336', '#E0E0E0', '#00C853']
cmap = sns.color_palette(colors, as_cmap=True)

sns.heatmap(matrix, annot=True, fmt='d', cmap=cmap, center=0,
            cbar_kws={'label': 'Routing Decision', 
                      'ticks': [-1, 0, 1],
                      'shrink': 0.6,
                      'pad': 0.02},
            linewidths=2, linecolor='white',
            vmin=-1, vmax=1, ax=ax,
            annot_kws={'fontsize': 10, 'fontweight': '600'})

cbar = ax.collections[0].colorbar
cbar.set_ticklabels(['AVOID', 'Neutral', 'ROUTE'])
cbar.ax.tick_params(labelsize=12, labelcolor='#212121')
cbar.set_label('Routing Decision', fontsize=14, fontweight='600', color='#212121')

ax.set_xlabel('Sales Rep ID', fontsize=15, fontweight='600', color='#212121', labelpad=10)
ax.set_ylabel('BD Rep ID', fontsize=15, fontweight='600', color='#212121', labelpad=10)
ax.set_title('Lead Routing Decision Matrix\nGreen = Route Here | Red = Avoid | Gray = Not in Top/Bottom 5', 
             fontsize=19, fontweight='700', color='#212121', pad=25)

plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontweight='500', fontsize=11)
plt.setp(ax.get_yticklabels(), rotation=0, fontweight='500', fontsize=11)

explanation = (
    "HOW TO USE THIS MATRIX:\n"
    "\n"
    "1. Find the BD rep in the left column\n"
    "\n"
    "2. Look across their row\n"
    "\n"
    "3. Route leads to GREEN cells\n"
    "    (top 5 performers)\n"
    "\n"
    "4. Avoid routing to RED cells\n"
    "    (bottom 5 performers)\n"
    "\n"
    "5. Gray cells = neutral\n"
    "    (not in top/bottom 5)"
)

ax.text(1.15, 0.35, explanation, transform=ax.transAxes,
        fontsize=11, verticalalignment='center',
        bbox=dict(boxstyle='round,pad=1.0', facecolor='#FFF9C4', 
                  edgecolor='#FBC02D', alpha=0.95, linewidth=2),
        fontweight='400', color='#424242', linespacing=1.8)

plt.tight_layout()
plt.savefig('visualizations/output/11_routing_decision_matrix.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()