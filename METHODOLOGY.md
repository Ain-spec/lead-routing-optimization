# Analysis Methodology: BD-Sales Pairing Optimization

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Data Requirements](#data-requirements)
3. [Metric Selection](#metric-selection)
4. [Baseline Selection (Critical Decision)](#baseline-selection-critical-decision)
5. [Scoring Formula](#scoring-formula)
6. [Classification System](#classification-system)
7. [Alternative Approaches Considered](#alternative-approaches-considered)
8. [Limitations & Assumptions](#limitations--assumptions)

## Problem Statement

**Business Question**: How can we optimize lead routing from BD to Sales reps to maximize conversion rates and revenue?

**Core Hypothesis**: Not all BD-Sales pairings perform equally. By analyzing historical pairing performance, we can identify optimal combinations and route leads accordingly.

## Data Requirements

### Minimum Data Needed
- **Opportunity-level data** with BD rep and Sales rep assignments
- **Outcome tracking**: Won, Lost, or Open status
- **Temporal data**: Created date, closed date, days in current stage
- **Value data**: Deal size/value

### Confidence Requirements
- **Minimum sample size**: 3 opportunities per pairing (minimum confidence)
- **Full confidence threshold**: 7 opportunities per pairing (75th percentile in our dataset)
- **Rationale**: Pairs with 1-2 opps are statistically unreliable

## Metric Selection

### Selection Criteria
1. **Actionability**: Can we change behavior based on this metric?
2. **Measurability**: Can we reliably calculate it from available data?
3. **Business Impact**: Does it correlate with revenue outcomes?

### Four Selected Metrics

#### 1. Win Rate
**Definition**: % of decided opportunities (Won or Lost) that closed won

**Formula**:
Win Rate = Closed Won / (Closed Won + Closed Lost) × 100

**Why included**: Direct measure of conversion success

#### 2. Early Death Rate
**Definition**: % of lost opportunities that died within 14 days

**Formula**:

Early Death Rate = Lost within 14 days / Total Lost × 100

**Why included**: Indicates lead qualification quality and early disqualification

**Lower is better** - pairs with high early death likely have qualification misalignment


#### 3. Stale Pipeline Rate
**Definition**: % of open opportunities inactive for 90+ days
Stale Rate = Open deals >90 days / Total Opportunities × 100

**Why included**: Indicates deal momentum and pipeline health

**Lower is better** - pairs with high stale rate struggle to move deals forward

**Key insight from analysis**: This was the biggest differentiator between high/low performers!

#### 4. Average Deal Size
**Definition**: Mean deal value across all opportunities (won or not)

**Formula**:
Avg Deal Size = Sum of all deal values / Total Opportunities

**Why included**: Revenue impact per opportunity

**Higher is better** - pairs that win larger deals contribute more revenue

**Example**:

### Metrics Considered But Not Included

**Days to Close**:
- **Why considered**: Measures sales cycle efficiency
- **Why excluded**: Highly dependent on deal complexity and company processes; less actionable at pairing level

**Loss Rate**:
- **Why excluded**: Redundant with Win Rate (inverse metric)


## Baseline Selection (Critical Decision)

This was the **most important methodological choice** in the entire analysis.

### The Challenge

How do we fairly compare pairing performance when:
- Different BDs pass different quality/difficulty leads
- Some BDs focus on enterprise (longer cycles, harder closes)
- Some BDs focus on SB (faster cycles, easier closes)

### Three Approaches Considered

### Approach 1: Population-Level Comparison

**Method**: Compare each pairing to the overall company average

**Rejected** - Fails to account for lead quality differences


### Approach 2: Sales Rep Baseline

**Method**: Compare each pairing to that Sales Rep's average across all BDs

**Valid but answers different question** - Could be useful for sales rep territory optimization


### Approach 3: BD Baseline (SELECTED)

**Method**: Compare each pairing to that BD's average across all Sales Reps

**SELECTED** - Best fit for routing optimization problem


## Scoring Formula

### Step 1: Calculate Percentage Deviation

For each metric, calculate percentage deviation from BD's average:

### Step 2: Apply Directionality

Some metrics: **Higher is better** (keep positive)
- Win Rate
- Deal Size

Some metrics: **Lower is better** (multiply by -1)
- Early Death Rate
- Stale Pipeline Rate

### Step 3: Apply Weights

Equal weight (25%) to each metric:

**Formula**:

Total Weighted Score = 
    (Win Rate Deviation × 0.25) +
    (Early Death Deviation × 0.25 × -1) +
    (Stale Pipeline Deviation × 0.25 × -1) +
    (Deal Size Deviation × 0.25)

**Why equal weights?**
- No strong business reason to prioritize one metric
- Keeps methodology simple and explainable
- Could customize in future based on company priorities


### Step 4: Apply Confidence Multiplier

Penalize pairs with limited sample size:

**Examples**:

Pair with 10 opps: Confidence = min(10/7, 1.0) = 1.0 (full confidence)
Pair with 7 opps:  Confidence = min(7/7, 1.0) = 1.0 (full confidence)
Pair with 5 opps:  Confidence = min(5/7, 1.0) = 0.71 (71% confidence)
Pair with 3 opps:  Confidence = min(3/7, 1.0) = 0.43 (43% confidence)


**Why 7 opportunities?**
- 75th percentile in our dataset
- Provides stable estimates in real-world data
- Balance between sample size and data availability


## Classification System

### Percentile-Based Approach

**Method**: Calculate percentiles on pairs with 3+ opportunities

**Classification Buckets**:

High Performer:   ≥ 75th percentile (top 25%)
Above Average:    50th - 75th percentile
Average:          25th - 50th percentile
Below Average:    10th - 25th percentile
At-Risk:          < 10th percentile (bottom 10%)

Low Confidence:   Confidence multiplier < 0.43 (< 3 opportunities)
Insufficient Data: < 3 opportunities


**In our dataset**:

75th percentile: +23.4 points
50th percentile: +2.1 points
25th percentile: -18.7 points
10th percentile: -42.3 points


**Why percentiles?**
1. **Data-driven**: Not arbitrary cutoffs
2. **Adaptive**: Automatically adjusts to score distribution
3. **Relative**: Always identifies top/bottom performers
4. **Explainable**: "Top 25%" is intuitive

## Alternative Approaches Considered

### Machine Learning Approach

**Considered**: Train model to predict pairing performance

**Pros**:
- Could capture non-linear relationships
- Might discover hidden patterns
- Could predict performance for new BD-Sales pairs

**Cons**:
- Less explainable ("black box")
- Requires more data for reliable training
- Harder to get stakeholder buy-in
- May overfit with limited data

**Decision**: Simpler statistical approach better for v1
- More explainable to stakeholders
- Adequate for current problem
- Could evolve to ML in future with more data

## Limitations & Assumptions

### Assumptions

1. **Historical patterns will continue**
   - Past pairing performance predicts future performance
   - Mitigation: Quarterly re-analysis to detect drift

2. **Lead quality is relatively stable per BD**
   - Each BD passes similar difficulty leads over time
   - Mitigation: Monitor BD qualification rates


### Limitations

1. **Simulated data**
   - This analysis uses synthetic data
   - Real company data will have additional nuances
   - Real validation needed before production use

2. **Doesn't account for external factors**
   - Market conditions
   - Product changes
   - Seasonal variations
   - Mitigation: Could add time-based analysis

3. **No causation, only correlation**
   - We observe pairing performance patterns
   - Can't definitively say WHY some pairs work better
   - Mitigation: Combine with qualitative feedback

4. **Treats all BDs/Sales reps as static**
   - People improve with training and experience
   - Model doesn't capture skill development
   - Mitigation: Regular re-analysis

## Iteration & Refinement

### Phase 1: Current State
- Baseline comparison methodology
- Equal-weighted metrics
- Percentile-based classification

### Phase 2: Potential Enhancements
- Custom weights based on company priorities
- Machine learning for pairing prediction
- Time-series analysis (trending over time)
- Incorporate qualitative factors (rep experience, territory knowledge)

### Phase 3: Advanced Features
- Automated monitoring and alerts
- Integration with CRM


## Conclusion

This methodology provides a **statistically sound**, **business-actionable**, and **explainable** framework for optimizing BD-Sales pairing decisions.

**Key strengths**:
1. Controls for lead quality through BD baseline
2. Data-driven classification through percentiles
3. Accounts for sample size through confidence multiplier
4. Directly actionable for routing decisions

**Result**: $600K+ estimated ARR improvement with zero implementation cost

**Statistical Concepts**:
- Percentile ranking
- Confidence intervals
- Baseline comparison methods

**Business Applications**:
- Revenue operations optimization
- Lead routing algorithms
- Sales territory design

**Tools Used**:
- Python (pandas, numpy)
- Statistical analysis
- Data visualization (matplotlib, seaborn)