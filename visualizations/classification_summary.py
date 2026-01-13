"""
Classification Summary Visualization
Shows distribution of performance classifications
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
    'High Performer': '#00C853',
    'Above Average': '#2196F3',
    'Average': '#9E9E9E',
    'Below Average': '#FF9800',
    'At-Risk': '#F44336',
    'Low Confidence': '#FFEB3B',
    'Insufficient Data': '#BDBDBD'
}

df = pd.read_csv('analysis/performance_scores.csv')

classification_counts = df['performance_classification'].value_counts()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), facecolor='white')

for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAFA')

colors = [COLORS.get(cat, '#9E9E9E') for cat in classification_counts.index]

wedges, texts, autotexts = ax1.pie(classification_counts.values, 
                                     labels=classification_counts.index,
                                     autopct='%1.1f%%',
                                     colors=colors,
                                     startangle=90,
                                     textprops={'fontsize': 11, 'fontweight': '600'},
                                     wedgeprops={'edgecolor': 'white', 'linewidth': 2})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('700')

ax1.set_title('Performance Classification Distribution\n(Pie Chart)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)

bars = ax2.barh(classification_counts.index, classification_counts.values,
                color=colors, edgecolor='white', linewidth=2, alpha=0.9)

ax2.set_xlabel('Number of Pairings', fontsize=14, fontweight='600', color='#212121')
ax2.set_ylabel('Classification', fontsize=14, fontweight='600', color='#212121')
ax2.set_title('Performance Classification Distribution\n(Bar Chart)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)
ax2.grid(True, alpha=0.2, axis='x', color='#9E9E9E')

for i, (cat, count) in enumerate(classification_counts.items()):
    pct = (count / classification_counts.sum()) * 100
    ax2.text(count + 2, i, f'{count} ({pct:.1f}%)', 
            va='center', fontsize=11, fontweight='600', color='#212121')

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#BDBDBD')
ax2.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/08_classification_summary.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()