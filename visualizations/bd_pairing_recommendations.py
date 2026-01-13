"""
BD Pairing Recommendations Visualization
Shows performance range from worst to best pairings for each BD
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

df = pd.read_csv('analysis/bd_pairing_recommendations.csv')

df['performance_gap'] = df['best_avg_score'] - abs(df['worst_avg_score'])

df_sorted = df.sort_values('performance_gap', ascending=False)

fig = plt.figure(figsize=(22, 14), facecolor='white')
ax = fig.add_axes([0.08, 0.08, 0.62, 0.88])
ax.set_facecolor('#FAFAFA')

y_pos = range(len(df_sorted))

for i, (idx, row) in enumerate(df_sorted.iterrows()):
    worst = row['worst_avg_score']
    best = row['best_avg_score']
    gap = best - worst
    
    ax.barh(i, gap, left=worst, height=0.6,
            color='#E0E0E0', alpha=0.5, edgecolor='none')
    
    ax.barh(i, abs(worst), left=worst, height=0.6,
            color='#F44336', alpha=0.85, edgecolor='white', linewidth=1.5,
            label='Worst 5 Avg' if i == 0 else '')
    
    ax.barh(i, best, left=0, height=0.6,
            color='#00C853', alpha=0.85, edgecolor='white', linewidth=1.5,
            label='Best 5 Avg' if i == 0 else '')
    
    ax.plot(worst, i, 'o', color='#D32F2F', markersize=9, 
            markeredgecolor='white', markeredgewidth=2, zorder=5)
    ax.plot(best, i, 'o', color='#00C853', markersize=9, 
            markeredgecolor='white', markeredgewidth=2, zorder=5)
    
    ax.text(worst - 2, i, f'{worst:.0f}', 
            ha='right', va='center', fontsize=10, fontweight='600', 
            color='#D32F2F')
    
    ax.text(best + 2, i, f'{best:.0f}', 
            ha='left', va='center', fontsize=10, fontweight='600', 
            color='#00C853')
    
    range_x_position = 85
    ax.text(range_x_position, i, f'{gap:.0f}', 
            ha='center', va='center', fontsize=10, fontweight='700',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                      edgecolor='#757575', alpha=0.95, linewidth=1.5),
            color='#424242')

ax.text(85, len(df_sorted), 'Range', 
        ha='center', va='bottom', fontsize=12, fontweight='700',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD', 
                  edgecolor='#1976D2', alpha=0.95, linewidth=2),
        color='#1565C0')

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted['bd_rep_id'], fontsize=11, fontweight='500')

ax.set_xlabel('Performance Score', fontsize=15, fontweight='600', color='#212121')
ax.set_ylabel('BD Rep (By Routing Impact)', fontsize=15, fontweight='600', color='#212121')
ax.set_title('BD Pairing Performance Range: Best vs Worst Sales Rep Matches\nLarger Range = Routing Decision Has Bigger Impact', 
             fontsize=19, fontweight='700', color='#212121', pad=25)

ax.axvline(0, color='#212121', linewidth=2.5, linestyle='--', alpha=0.6, zorder=3)

ax.legend(fontsize=13, loc='lower right', frameon=True, 
          fancybox=True, shadow=True, framealpha=0.95, edgecolor='#BDBDBD')

ax.grid(True, alpha=0.25, axis='x', color='#9E9E9E', linewidth=0.8)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

ax.set_xlim(-80, 95)

explanation_ax = fig.add_axes([0.73, 0.08, 0.24, 0.88])
explanation_ax.axis('off')

explanation_title = "HOW TO READ THIS CHART"
explanation_content = [
    "",
    "VISUAL ELEMENTS:",
    "• Each row = One BD rep",
    "• Red bar (left) = Average of 5 WORST pairings",
    "• Green bar (right) = Average of 5 BEST pairings",
    "• Range (right column) = Difference between best & worst",
    "",
    "EXAMPLE: BD_009 (Top Row)",
    "• Worst pairings average: -68 points",
    "• Best pairings average: +43 points",
    "• Range: 111 points",
    "• Meaning: Routing BD_009 correctly vs incorrectly",
    "  creates a 111-point performance swing!",
    "",
    "ACTION PRIORITIES:",
    "",
    "High Priority (Range > 100):",
    "     Routing decision critical",
    "",
    "Medium Priority (Range 80-100):",
    "     Significant impact from routing",
    "",
    "Low Priority (Range < 80):",
    "     More flexible",
    "",
    "",
    "KEY INSIGHT:",
    "Larger ranges = More important to route",
    "to the RIGHT sales reps. Getting it wrong",
    "has major negative impact.",
]

explanation_ax.text(0.5, 0.98, explanation_title,
                   ha='center', va='top', fontsize=15, fontweight='700',
                   color='#1565C0', transform=explanation_ax.transAxes)

y_position = 0.94
line_spacing = 0.028

for line in explanation_content:
    if line.startswith("•"):
        explanation_ax.text(0.05, y_position, line,
                           ha='left', va='top', fontsize=10, fontweight='400',
                           color='#424242', transform=explanation_ax.transAxes)
    elif line.startswith("VISUAL") or line.startswith("EXAMPLE") or line.startswith("ACTION") or line.startswith("KEY"):
        explanation_ax.text(0.05, y_position, line,
                           ha='left', va='top', fontsize=11, fontweight='700',
                           color='#1976D2', transform=explanation_ax.transAxes)
    elif line.startswith("High Priority") or line.startswith("Medium Priority") or line.startswith("Low Priority"):
        color = '#D32F2F' if 'High' in line else '#FF9800' if 'Medium' in line else '#00C853'
        explanation_ax.text(0.05, y_position, line,
                           ha='left', va='top', fontsize=10, fontweight='700',
                           color=color, transform=explanation_ax.transAxes)
    elif line.startswith("     "):
        explanation_ax.text(0.1, y_position, line.strip(),
                           ha='left', va='top', fontsize=9, fontweight='400',
                           color='#616161', transform=explanation_ax.transAxes,
                           style='italic')
    else:
        explanation_ax.text(0.05, y_position, line,
                           ha='left', va='top', fontsize=10, fontweight='400',
                           color='#424242', transform=explanation_ax.transAxes)
    
    y_position -= line_spacing

rect = plt.Rectangle((0.01, 0.01), 0.98, 0.98, 
                     transform=explanation_ax.transAxes,
                     facecolor='#FFF9C4', edgecolor='#FBC02D', 
                     linewidth=3, alpha=0.3, zorder=-1)
explanation_ax.add_patch(rect)

plt.savefig('visualizations/output/09_bd_pairing_recommendations.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()