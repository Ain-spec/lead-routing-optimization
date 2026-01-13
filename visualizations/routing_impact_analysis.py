"""
Routing Impact Analysis Visualization
Quantifies business impact in Annual Recurring Revenue (ARR)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('visualizations/output', exist_ok=True)

recs = pd.read_csv('analysis/bd_pairing_recommendations.csv')
performance = pd.read_csv('analysis/performance_scores.csv')
opportunities = pd.read_csv('data/opportunities.csv')

# Merge to get deal values
performance_with_deals = performance.merge(
    opportunities[['bd_rep_id', 'sales_rep_id', 'deal_value', 'outcome']],
    on=['bd_rep_id', 'sales_rep_id'],
    how='left'
)

impact_data = []

for idx, row in recs.iterrows():
    bd = row['bd_rep_id']
    
    bd_pairings = performance[performance['bd_rep_id'] == bd].copy()
    bd_pairings = bd_pairings[bd_pairings['total_opps'] >= 3]
    
    if len(bd_pairings) == 0:
        continue
    
    # Get actual opportunities for this BD
    bd_opps = opportunities[opportunities['bd_rep_id'] == bd].copy()
    
    # Current state metrics
    current_avg_score = bd_pairings['final_performance_score'].mean()
    current_win_rate = bd_pairings['win_rate_pct'].mean() / 100
    current_avg_deal = bd_opps['deal_value'].mean()
    
    # Best pairings
    best_reps = [r.strip() for r in row['best_sales_reps'].split(',')]
    best_pairings = bd_pairings[bd_pairings['sales_rep_id'].isin(best_reps)]
    best_avg_score = best_pairings['final_performance_score'].mean() if len(best_pairings) > 0 else current_avg_score
    best_win_rate = best_pairings['win_rate_pct'].mean() / 100 if len(best_pairings) > 0 else current_win_rate
    
    # Worst pairings
    worst_reps = [r.strip() for r in row['worst_sales_reps'].split(',')]
    worst_pairings = bd_pairings[bd_pairings['sales_rep_id'].isin(worst_reps)]
    worst_avg_score = worst_pairings['final_performance_score'].mean() if len(worst_pairings) > 0 else current_avg_score
    
    # Calculate ARR impact
    total_opps = bd_pairings['total_opps'].sum()
    
    # Current ARR (current win rate × avg deal × opportunities)
    current_arr = current_win_rate * current_avg_deal * total_opps
    
    # Optimized ARR (best win rate × avg deal × opportunities)
    optimized_arr = best_win_rate * current_avg_deal * total_opps
    
    # ARR improvement
    arr_improvement = optimized_arr - current_arr
    
    improvement_score = best_avg_score - current_avg_score
    total_swing = best_avg_score - worst_avg_score
    
    impact_data.append({
        'bd_rep_id': bd,
        'current_avg_score': current_avg_score,
        'optimized_score': best_avg_score,
        'worst_case_score': worst_avg_score,
        'improvement_points': improvement_score,
        'total_swing': total_swing,
        'total_opps': total_opps,
        'current_arr': current_arr,
        'optimized_arr': optimized_arr,
        'arr_improvement': arr_improvement
    })

impact_df = pd.DataFrame(impact_data)

# Create visualization
fig = plt.figure(figsize=(22, 14), facecolor='white')

ax1 = fig.add_axes([0.08, 0.55, 0.55, 0.38])
ax2 = fig.add_axes([0.08, 0.08, 0.55, 0.38])
ax_text = fig.add_axes([0.68, 0.08, 0.28, 0.85])

for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAFA')

# Chart 1: ARR Improvement by BD
impact_sorted = impact_df.sort_values('arr_improvement', ascending=True)

y_pos = range(len(impact_sorted))
colors = ['#2f855a' if x > 0 else '#9E9E9E' for x in impact_sorted['arr_improvement']]

bars1 = ax1.barh(y_pos, impact_sorted['arr_improvement'], 
                 color=colors, edgecolor='white', linewidth=1.5, alpha=0.9)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(impact_sorted['bd_rep_id'], fontsize=10, fontweight='500')
ax1.set_xlabel('ARR Improvement ($)', fontsize=14, fontweight='600', color='#212121')
ax1.set_ylabel('BD Rep', fontsize=14, fontweight='600', color='#212121')
ax1.set_title('Expected ARR Improvement by BD Rep\nOptimized Routing (Top 5) vs Current (Random/Even)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)
ax1.axvline(0, color='#212121', linewidth=1.5, alpha=0.5)
ax1.grid(True, alpha=0.2, axis='x', color='#9E9E9E')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for i, (idx, row) in enumerate(impact_sorted.iterrows()):
    ax1.text(row['arr_improvement'] + 1000, i, f"${row['arr_improvement']:,.0f}", 
            va='center', ha='left', fontsize=9, fontweight='600', color='#2f855a')

# Chart 2: Current vs Optimized ARR (Top 10)
impact_top10 = impact_df.nlargest(10, 'arr_improvement')
x = range(len(impact_top10))
width = 0.35

bars_current = ax2.bar([i - width/2 for i in x], impact_top10['current_arr'], width,
                       label='Current ARR', color='#d69e2e', 
                       edgecolor='white', linewidth=1.5, alpha=0.9)
bars_optimized = ax2.bar([i + width/2 for i in x], impact_top10['optimized_arr'], width,
                         label='Optimized ARR', color='#2f855a',
                         edgecolor='white', linewidth=1.5, alpha=0.9)

ax2.set_xlabel('BD Rep (Top 10 by ARR Improvement)', fontsize=14, fontweight='600', color='#212121')
ax2.set_ylabel('Annual Recurring Revenue ($)', fontsize=14, fontweight='600', color='#212121')
ax2.set_title('Current vs Optimized ARR (Top 10 BDs)', 
              fontsize=16, fontweight='700', color='#212121', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(impact_top10['bd_rep_id'], rotation=45, ha='right', fontsize=11, fontweight='500')
ax2.legend(fontsize=12, frameon=True, fancybox=True, shadow=True, framealpha=0.95, loc='upper right')
ax2.grid(True, alpha=0.2, axis='y', color='#9E9E9E')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, (idx, row) in enumerate(impact_top10.iterrows()):
    ax2.text(i - width/2, row['current_arr'] + 2000, 
            f"${row['current_arr']/1000:.0f}K", 
            ha='center', va='bottom', fontsize=9, fontweight='600', color='#d69e2e')
    ax2.text(i + width/2, row['optimized_arr'] + 2000, 
            f"${row['optimized_arr']/1000:.0f}K", 
            ha='center', va='bottom', fontsize=9, fontweight='600', color='#2f855a')

# Summary text
ax_text.axis('off')

total_current_arr = impact_df['current_arr'].sum()
total_optimized_arr = impact_df['optimized_arr'].sum()
total_arr_improvement = impact_df['arr_improvement'].sum()

summary_stats = f"""
BUSINESS IMPACT SUMMARY
{'='*50}

CURRENT STATE (Random/Even Routing):
  • Total ARR: ${total_current_arr:,.0f}
  • Total Opportunities: {impact_df['total_opps'].sum():,.0f}

OPTIMIZED STATE (Route to Top 5):
  • Total ARR: ${total_optimized_arr:,.0f}
  • Expected ARR Lift: ${total_arr_improvement:,.0f}

PERFORMANCE GAIN:
  • Absolute: ${total_arr_improvement:,.0f}
  • Relative: {(total_arr_improvement / total_current_arr) * 100:.1f}%

TOP 3 BDs (Highest ARR Impact):
"""

top_3_impact = impact_df.nlargest(3, 'arr_improvement')
for idx, row in top_3_impact.iterrows():
    summary_stats += f"\n  {row['bd_rep_id']}: ${row['arr_improvement']:,.0f}"

summary_stats += f"""


IMPLEMENTATION PRIORITY:

High Impact (>${total_arr_improvement/len(impact_df)*1.5:,.0f}):
  {len(impact_df[impact_df['arr_improvement'] > total_arr_improvement/len(impact_df)*1.5])} BDs

Medium Impact (${total_arr_improvement/len(impact_df)*0.5:,.0f}-${total_arr_improvement/len(impact_df)*1.5:,.0f}):
  {len(impact_df[(impact_df['arr_improvement'] >= total_arr_improvement/len(impact_df)*0.5) & (impact_df['arr_improvement'] <= total_arr_improvement/len(impact_df)*1.5)])} BDs


KEY INSIGHTS:

ARR Calculation Method:
  • Current: Win Rate × Avg Deal × Opps
  • Optimized: Best Win Rate × Deal × Opps
  • Improvement = Difference

What ${total_arr_improvement:,.0f} Means:
  • Additional revenue from same leads
  • No additional marketing spend
  • Pure routing optimization

How to Achieve This:
  1. Route each BD's leads to their 
     top 5 compatible sales reps
  2. Avoid routing to bottom 5 reps
  3. Focus on high-impact BDs first


BUSINESS VALUE:

Implementation cost: $0
(Pure routing logic changes)

Expected annual benefit: 
${total_arr_improvement:,.0f}

ROI: Infinite ♾️
"""

ax_text.text(0.05, 0.98, summary_stats, transform=ax_text.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=1.2', facecolor='#E6FFFA', 
                   edgecolor='#2f855a', alpha=0.95, linewidth=2.5),
         color='#212121', linespacing=1.6)

plt.savefig('visualizations/output/12_routing_impact_analysis.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

impact_df.to_csv('analysis/routing_impact_analysis.csv', index=False)