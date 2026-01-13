"""
Opportunity Distribution Histogram
Shows distribution of opportunities per BD-Sales pairing
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

CONFIDENCE_THRESHOLD = 7

df = pd.read_csv('analysis/performance_scores.csv')

fig, ax = plt.subplots(figsize=(14, 9), facecolor='white')
ax.set_facecolor('#FAFAFA')

# Create histogram
n, bins, patches = ax.hist(df['total_opps'], bins=30, edgecolor='white', 
                           linewidth=1.5, alpha=0.85, color='#2196F3')

# Color bars by confidence level
for i, patch in enumerate(patches):
    bin_center = (bins[i] + bins[i+1]) / 2
    if bin_center >= CONFIDENCE_THRESHOLD:
        patch.set_facecolor('#00C853')  # Green - full confidence
    elif bin_center >= 3:
        patch.set_facecolor('#FF9800')  # Orange - partial confidence
    else:
        patch.set_facecolor('#F44336')  # Red - insufficient

# Add threshold lines
ax.axvline(CONFIDENCE_THRESHOLD, color='#00C853', linestyle='--', 
           linewidth=3, alpha=0.8, label=f'Full Confidence ({CONFIDENCE_THRESHOLD}+ opps)')
ax.axvline(3, color='#F44336', linestyle='--', 
           linewidth=3, alpha=0.8, label='Minimum Threshold (3 opps)')

ax.set_xlabel('Number of Opportunities per Pairing', fontsize=14, fontweight='600', color='#212121')
ax.set_ylabel('Number of Pairings', fontsize=14, fontweight='600', color='#212121')
ax.set_title('Distribution of Opportunities per BD-Sales Pairing\nConfidence Levels Indicated by Color', 
             fontsize=18, fontweight='700', color='#212121', pad=20)

ax.legend(fontsize=12, frameon=True, fancybox=True, shadow=True, 
          framealpha=0.95, edgecolor='#BDBDBD', loc='upper right')
ax.grid(True, alpha=0.2, color='#9E9E9E')

# Add summary statistics
above_threshold = (df['total_opps'] >= CONFIDENCE_THRESHOLD).sum()
partial = ((df['total_opps'] >= 3) & (df['total_opps'] < CONFIDENCE_THRESHOLD)).sum()
insufficient = (df['total_opps'] < 3).sum()

summary_text = (f"High Confidence: {above_threshold} pairs\n"
                f"Partial Confidence: {partial} pairs\n"
                f"Insufficient Data: {insufficient} pairs")

ax.text(0.98, 0.97, summary_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                  edgecolor='#BDBDBD', alpha=0.95, linewidth=1.5),
        fontweight='500', color='#424242')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#BDBDBD')
ax.spines['bottom'].set_color('#BDBDBD')

plt.tight_layout()
plt.savefig('visualizations/output/02_opportunity_distribution.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()