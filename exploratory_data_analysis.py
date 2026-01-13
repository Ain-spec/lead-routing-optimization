"""
Exploratory Data Analysis
Validates data quality and provides basic statistics
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/opportunities.csv')

# Basic info
print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Date range: {df['created_date'].min()} to {df['created_date'].max()}")

# Column info
print(df.dtypes)

# Check for nulls
null_counts = df.isnull().sum()
if null_counts.sum() == 0:
    print("No missing values found")
else:
    print("Missing values by column:")
    print(null_counts[null_counts > 0])

# BD Rep analysis
bd_counts = df['bd_rep_id'].value_counts()
print(f"Total unique BD reps: {df['bd_rep_id'].nunique()}")
print(f"Opportunities per BD (min-max): {bd_counts.min()}-{bd_counts.max()}")
print(f"Average opportunities per BD: {bd_counts.mean():.1f}")

# Sales Rep analysis
sr_counts = df['sales_rep_id'].value_counts()
print(f"Total unique Sales reps: {df['sales_rep_id'].nunique()}")
print(f"Opportunities per Sales rep (min-max): {sr_counts.min()}-{sr_counts.max()}")
print(f"Average opportunities per Sales rep: {sr_counts.mean():.1f}")

# Pairing analysis
df['pairing'] = df['bd_rep_id'] + '-' + df['sales_rep_id']
pairing_counts = df['pairing'].value_counts()
print(f"Total unique pairings: {df['pairing'].nunique()}")
print(f"Opportunities per pairing (min-max): {pairing_counts.min()}-{pairing_counts.max()}")
print(f"Average opportunities per pairing: {pairing_counts.mean():.1f}")

# Outcome distribution
outcome_dist = df['outcome'].value_counts()
for outcome, count in outcome_dist.items():
    pct = (count / len(df)) * 100
    print(f"{outcome}: {count} ({pct:.1f}%)")

# Deal value analysis
print(f"Min deal value: ${df['deal_value'].min():,.0f}")
print(f"Max deal value: ${df['deal_value'].max():,.0f}")
print(f"Average deal value: ${df['deal_value'].mean():,.0f}")
print(f"Median deal value: ${df['deal_value'].median():,.0f}")

# Stage analysis
stage_dist = df['current_stage'].value_counts()
for stage, count in stage_dist.items():
    pct = (count / len(df)) * 100
    print(f"{stage}: {count} ({pct:.1f}%)")

# Data quality checks

# Check for duplicate opportunity IDs
duplicates = df['opportunity_id'].duplicated().sum()
print(f"Duplicate opportunity IDs: {duplicates}")

# Check for invalid dates
df['created_date'] = pd.to_datetime(df['created_date'])
df['closed_date'] = pd.to_datetime(df['closed_date'])
invalid_dates = (df['closed_date'] < df['created_date']).sum()
print(f"Invalid date ranges (closed < created): {invalid_dates}")

# Check for negative deal values
negative_values = (df['deal_value'] < 0).sum()
print(f"Negative deal values: {negative_values}")

# Check days in stage
negative_days = (df['days_in_current_stage'] < 0).sum()
print(f"Negative days in stage: {negative_days}")


# Save summary statistics
summary = {
    'total_records': len(df),
    'total_bds': df['bd_rep_id'].nunique(),
    'total_sales_reps': df['sales_rep_id'].nunique(),
    'total_pairings': df['pairing'].nunique(),
    'date_range_start': df['created_date'].min(),
    'date_range_end': df['created_date'].max(),
    'avg_deal_value': df['deal_value'].mean(),
    'data_quality_issues': duplicates + invalid_dates + negative_values + negative_days
}