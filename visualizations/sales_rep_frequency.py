import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

# Load data
df = pd.read_csv('analysis/bd_pairing_recommendations.csv')

# Count appearances in best_sales_reps
all_best = []
for reps in df['best_sales_reps']:
    all_best.extend([r.strip() for r in reps.split(',')])

best_counter = Counter(all_best)

# Count appearances in worst_sales_reps
all_worst = []
for reps in df['worst_sales_reps']:
    all_worst.extend([r.strip() for r in reps.split(',')])

worst_counter = Counter(all_worst)

# Get all unique sales reps
all_reps = sorted(set(all_best + all_worst))

# Create DataFrame
rep_data = []
for rep in all_reps:
    rep_data.append({
        'sales_rep_id': rep,
        'top_5_count': best_counter.get(rep, 0),
        'bottom_5_count': worst_counter.get(rep, 0),
        'net_score': best_counter.get(rep, 0) - worst_counter.get(rep, 0)
    })

rep_df = pd.DataFrame(rep_data)
rep_df = rep_df.sort_values('net_score', ascending=True)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12), facecolor='white')

for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAFA')

# ===== LEFT CHART: Frequency in Top 5 vs Bottom 5 =====
y_pos = np.arange(len(rep_df))
bar_height = 0.4

bars_top = ax1.barh(y_pos + bar_height/2, rep_df['top_5_count'], 
                    bar_height, label='Appears in Top 5',
                    color='#00C853', edgecolor='white', linewidth=1.5, alpha=0.9)

bars_bottom = ax1.barh(y_pos - bar_height/2, -rep_df['bottom_5_count'], 
                       bar_height, label='Appears in Bottom 5',
                       color='#F44336', edgecolor='white', linewidth=1.5, alpha=0.9)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(rep_df['sales_rep_id'], fontsize=10, fontweight='500')
ax1.set_xlabel('Number of BDs', fontsize=13, fontweight='600', color='#212121')
ax1.set_ylabel('Sales Rep ID', fontsize=13, fontweight='600', color='#212121')
ax1.set_title('Sales Rep Appearance Frequency\n(Positive = Top 5, Negative = Bottom 5)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)

ax1.axvline(0, color='#212121', linewidth=1.5, linestyle='-', alpha=0.5)
ax1.legend(fontsize=11, loc='upper right', frameon=True, 
           fancybox=True, shadow=True, framealpha=0.95, edgecolor='#BDBDBD')
ax1.grid(True, alpha=0.2, axis='x', color='#9E9E9E')

# Add value labels
for i, (idx, row) in enumerate(rep_df.iterrows()):
    # Top 5 count
    if row['top_5_count'] > 0:
        ax1.text(row['top_5_count'] + 0.3, i + bar_height/2, 
                f"{int(row['top_5_count'])}", 
                va='center', ha='left', fontsize=9, fontweight='600', color='#00C853')
    
    # Bottom 5 count
    if row['bottom_5_count'] > 0:
        ax1.text(-row['bottom_5_count'] - 0.3, i - bar_height/2, 
                f"{int(row['bottom_5_count'])}", 
                va='center', ha='right', fontsize=9, fontweight='600', color='#F44336')

# ===== RIGHT CHART: Net Score (Universal Closers vs Struggles) =====
rep_df_sorted = rep_df.sort_values('net_score', ascending=True)
y_pos2 = np.arange(len(rep_df_sorted))

# Color based on net score
colors = ['#00C853' if x > 0 else '#F44336' if x < 0 else '#9E9E9E' 
          for x in rep_df_sorted['net_score']]

bars_net = ax2.barh(y_pos2, rep_df_sorted['net_score'], 
                    color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)

ax2.set_yticks(y_pos2)
ax2.set_yticklabels(rep_df_sorted['sales_rep_id'], fontsize=10, fontweight='500')
ax2.set_xlabel('Net Score (Top 5 - Bottom 5)', fontsize=13, fontweight='600', color='#212121')
ax2.set_title('Sales Rep Classification\n(Universal Closers vs Universal Struggles)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)

ax2.axvline(0, color='#212121', linewidth=1.5, linestyle='-', alpha=0.5)
ax2.grid(True, alpha=0.2, axis='x', color='#9E9E9E')

# Add value labels
for i, (idx, row) in enumerate(rep_df_sorted.iterrows()):
    label_x = row['net_score'] + (0.3 if row['net_score'] > 0 else -0.3)
    label_ha = 'left' if row['net_score'] > 0 else 'right'
    
    ax2.text(label_x, i, f"{int(row['net_score'])}", 
            va='center', ha=label_ha, fontsize=9, fontweight='600',
            color='#212121')

# Add category labels
ax2.text(0.95, 0.97, 'Universal\nClosers\n→', transform=ax2.transAxes,
         fontsize=12, fontweight='700', ha='right', va='top',
         color='#00C853',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor='#00C853', linewidth=2, alpha=0.9))

ax2.text(0.05, 0.03, '← Universal\nStruggles', transform=ax2.transAxes,
         fontsize=12, fontweight='700', ha='left', va='bottom',
         color='#F44336',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor='#F44336', linewidth=2, alpha=0.9))

# Clean spines
for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDBDBD')
    ax.spines['bottom'].set_color('#BDBDBD')

# Add explanation box
explanation_text = (
    "Universal Closers (Net > 0): Work well with many BDs → Route premium leads\n"
    "Universal Struggles (Net < 0): Struggle with many BDs → Selective routing only\n"
    "Specialists (High Top & Bottom): Excel with specific BDs, struggle with others"
)
ax2.text(0.02, 0.98, explanation_text, transform=ax2.transAxes, 
        fontsize=9, verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF9C4', 
                  edgecolor='#FBC02D', alpha=0.9, linewidth=2),
        fontweight='400', color='#424242')

plt.tight_layout()
plt.savefig('visualizations/output/10_sales_rep_frequency.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Created: 10_sales_rep_frequency.png")
plt.close()