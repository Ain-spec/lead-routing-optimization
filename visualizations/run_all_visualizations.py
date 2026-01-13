"""
Master Script to Generate All Visualizations
Runs all visualization scripts in sequence
"""

import subprocess

scripts = [
    'final_score_distribution.py',
    'opportunity_distribution.py',
    'top_bottom_pairs.py',
    'performance_heatmap.py',
    'metric_contributions.py',
    'confidence_vs_performance.py',
    'bd_summary.py',
    'classification_summary.py',
    'bd_pairing_recommendations.py',
    'routing_decision_matrix.py',
    'routing_impact_analysis.py'
]

for i, script in enumerate(scripts, 1):
    print(f"[{i}/{len(scripts)}] Running {script}...")
    subprocess.run(['python', f'visualizations/{script}'], check=True)

print(f"\nAll {len(scripts)} visualizations complete")
print(f"Saved to: visualizations/output/")