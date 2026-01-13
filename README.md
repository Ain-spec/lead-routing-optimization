# BD-Sales Pairing Optimization Analysis

A comprehensive data analytics project analyzing Business Development and Sales representative pairing performance to optimize lead routing and maximize conversion rates and revenue.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌐 Live Interactive Dashboards

**[👉 View Live Dashboards](https://ain-spec.github.io/lead-routing-optimization/)**

Explore the complete analysis through three interactive dashboards:
- **Dashboard 1:** Exploratory Data Analysis & Data Validation
- **Dashboard 2:** Performance Methodology & Analysis Results
- **Dashboard 3:** Business Recommendations & $600K+ ARR Impact

## 📊 Project Overview

This project analyzes 2,200+ opportunities across 18 BD reps and 23 Sales reps (413 unique pairings) to identify optimal BD-Sales team pairings and provide data-driven routing recommendations.

### Business Problem
Not all BD-Sales pairings perform equally. Random lead routing leads to:
- Suboptimal win rates
- Longer sales cycles  
- Higher early deal death rates
- Inconsistent pipeline health

### Solution
Analyze historical pairing performance to:
1. Identify high-performing BD-Sales combinations
2. Flag at-risk pairings to avoid
3. Provide actionable routing recommendations
4. Quantify expected business impact in ARR



## 🎯 Key Findings

**Expected ARR Improvement: $600K+** (annual recurring revenue lift from optimized routing)

- **18 BDs analyzed** with varying pairing performance ranges
- **Top 3 BDs** show $100K+ ARR improvement potential each
- **124-point performance swing** between best and worst routing decisions for some BDs
- **$0 implementation cost** - pure routing logic optimization


## 📁 Project Structure
sales-handoff-quality-analysis/
│
├── data/
│   └── opportunities.csv                  # Simulated opportunity data
│
├── analysis/
│   ├── pair_metrics.csv                   # BD-Sales pair metrics
│   ├── performance_scores.csv             # Performance scoring results
│   ├── bd_pairing_recommendations.csv     # Top/bottom 5 recommendations
│   └── routing_impact_analysis.csv        # ARR impact calculations
│
├── visualizations/
│   ├── output/                            # Generated PNG visualizations
│   └── *.py                               # Visualization scripts
│
├── iterations/                            # Project evolution
│   ├── v1_initial_approach.py
│   ├── v2_added_confidence.py
│   ├── v3_baseline_comparison.py
│   └── notes.txt
│
├── exploratory_data_analysis.py           # EDA and data validation
├── data_generation.py                     # Simulated data generation
├── metric_calculation.py                  # Calculate pairing metrics
├── performance_scoring.py                 # Score and classify pairings
│
├── dashboard_index.html                   # Interactive dashboard landing page
├── dashboard_1_eda.html                   # EDA dashboard
├── dashboard_2_methodology.html           # Methodology & analysis dashboard
├── dashboard_3_recommendations.html       # Business recommendations dashboard
│
├── METHODOLOGY.md                         # Detailed methodology doc
├── README.md                              # Project documentation
├── requirements.txt                       # Python dependencies
└── .gitignore                             # Git ignore file



## Technologies Used

- **Python 3.8+**: Core analysis language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Data visualization
- **seaborn**: Statistical visualizations
- **HTML/CSS**: Interactive dashboards


### Getting Started

1. Clone the repository

git clone https://github.com/yourusername/sales-handoff-quality-analysis.git
cd sales-handoff-quality-analysis


2. Install dependencies
pip install -r requirements.txt

3. Run the analysis pipeline

# Step 1: Generate simulated data
python data_generation.py

# Step 2: Exploratory data analysis
python exploratory_data_analysis.py

# Step 3: Calculate metrics
python metric_calculation.py

# Step 4: Score performance
python performance_scoring.py

# Step 5: Generate visualizations
python visualizations/run_all_visualizations.py


4. View the dashboard


## 📈 Analysis Methodology

### 1. Data Collection
- Simulated 2,200 opportunities spanning 2 years
- 18 BD reps × 23 Sales reps = 413 possible pairings
- Tracked: Win rate, early death rate, stale pipeline rate, deal size

### 2. Metric Calculation
Four key metrics calculated for each pairing:
- **Win Rate**: % of decided opportunities that closed won
- **Early Death Rate**: % of lost deals that died within 14 days
- **Stale Pipeline Rate**: % of open deals inactive for 90+ days
- **Average Deal Size**: Mean deal value

### 3. Performance Scoring
- **Baseline Comparison**: Each pair compared to that BD's average (controls for lead quality)
- **Percentage Deviation**: Relative performance vs baseline
- **Weighted Scoring**: Equal 25% weight per metric
- **Confidence Multiplier**: Based on opportunity count (threshold: 7)

### 4. Classification
Percentile-based classification:
- **High Performer**: Top 25% (75th percentile+)
- **Above Average**: 50th-75th percentile
- **Average**: 25th-50th percentile
- **Below Average**: 10th-25th percentile
- **At-Risk**: Bottom 10%

## 📊 Key Visualizations

### Dashboard 1: Exploratory Data Analysis
1. **Opportunity Distribution**: Shows confidence levels across pairings
2. **Data Quality Validation**: Confirms dataset is ready for analysis

### Dashboard 2: Methodology & Performance Analysis
3. **Performance Score Distribution**: Percentile thresholds and classification zones
4. **Top/Bottom Performers**: Best and worst BD-Sales combinations
5. **Performance Heatmap**: Complete pairing matrix
6. **Metric Contributions**: What drives high vs low performance

### Dashboard 3: Business Recommendations
7. **BD Pairing Recommendations**: Performance range for each BD
8. **Routing Decision Matrix**: Green (route) vs red (avoid) lookup table
9. **ARR Impact Analysis**: Quantified revenue improvement from optimization

---

## 💼 Business Impact

### Current State (Random Routing)
- Total ARR: ~$1.2M
- No systematic pairing optimization
- Performance left on the table

### Optimized State (Route to Top 5)
- Total ARR: ~$1.8M
- **+$600K ARR improvement**
- **50% ARR increase**



## 🎓 Skills Demonstrated

### Technical Skills
- Data analysis and manipulation (pandas, numpy)
- Statistical analysis and percentile-based classification
- Data visualization (matplotlib, seaborn)
- Python scripting and automation
- HTML/CSS dashboard creation

### Business Skills
- Problem identification and scoping
- Metric definition and KPI selection
- Data-driven recommendation development
- Stakeholder communication and storytelling
- ROI analysis and business case building

### Analytical Skills
- Baseline methodology selection
- Confidence interval application
- Performance classification systems
- Business impact quantification

## 🚧 Challenges Encountered

### 1. Baseline Selection Challenge

**Problem**: How do we fairly compare pairings when different BDs pass different quality leads?

**Initial Approach**: Compare all pairings to company-wide average
- **Issue**: Didn't account for BD lead quality differences
- Enterprise BDs naturally have lower win rates than SB BDs

**Solution**: Compare each pairing to that BD's average (BD baseline)
- Controls for inherent lead quality from each BD
- Makes comparisons fair and actionable for routing decisions

**Impact**: This was the most critical methodological decision - completely changed the analysis validity


### 2. Circular Logic in BD Summary

**Problem**: When averaging all BD pairs' performance scores, results were close to zero

**Initial Reaction**: Thought there was a bug in the calculation

**Realization**: This is mathematically correct by design!
- We compare each pair to that BD's average
- Deviations naturally balance out (some above, some below)
- This is a feature, not a bug

**Solution**: 
- Documented this clearly in methodology
- Added explanation box to visualization
- Changed interpretation: "This measures pairing consistency, not absolute BD quality"

**Lesson Learned**: What looks like an error might be correct behavior - understand your methodology deeply

### 3. Confidence Threshold Selection

**Problem**: How many opportunities needed for reliable pairing analysis?

**Trial & Error**:
- Tried threshold of 3 opps → Too noisy, unreliable results
- Tried threshold of 10 opps → Lost too many pairings, insufficient data
- Tried threshold of 5 opps → Still some instability

**Solution**: Two-tier approach
- **Minimum threshold**: 3 opportunities (43% confidence)
- **Full confidence**: 7 opportunities (75th percentile in dataset)
- Apply confidence multiplier that scales linearly

**Impact**: Balances statistical reliability with data availability


### 4. Visualization Complexity

**Problem**: Initial visualizations tried to show everything at once - too overwhelming

**Examples of cuts made**:
- Sales Rep frequency analysis → Too complex for main dashboard
- Confidence vs Performance scatter → Interesting but not essential
- Multiple classification views → Chose most intuitive representation

**Solution**: 
- Focus on storytelling: Each dashboard has a clear narrative
- Progressive disclosure: Start simple (EDA), build to complex (recommendations)
- Keep "cut" visualizations in analysis folder for reference

**Lesson Learned**: Less is more - every chart must earn its place in the story


### 5. ARR Calculation Complexity

**Problem**: How do we estimate revenue impact when not all opportunities are closed?

**Initial thought**: Only count won deals
- **Issue**: Ignores the opportunity cost of poor routing

**Solution**: Calculate potential ARR based on win rate × deal value × volume
- Current: Actual win rate × avg deal × opportunities
- Optimized: Best pairing win rate × avg deal × opportunities
- Difference = ARR improvement potential

**Assumption**: Average deal size remains constant across pairings (reasonable for this analysis)

**Impact**: Provides compelling business case in dollar terms

## 📝 Future Enhancements

- [ ] Real-time dashboard with Plotly/Dash
- [ ] Machine learning model for pairing prediction
- [ ] Time-series analysis of pairing performance trends
- [ ] A/B test framework for routing validation
- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Automated monitoring and alerting
- [ ] Sales rep specialization analysis (which BDs work best with each rep)

---

## 👤 Author

**Ain**

Data Analyst | Marketing Analyst | Revenue Operations

- Portfolio: []
- LinkedIn: [(https://www.linkedin.com/in/qurat-ul-ain-236b60133/)]
- GitHub: [@Ain-spec](https://github.com/Ain-spec)
- Email: quratulain_izhar@hotmail.com


## Additional Documentation
- **[METHODOLOGY.md](METHODOLOGY.md)**: Detailed technical methodology


## Contributing

This is a portfolio project, but feedback and suggestions are welcome! Feel free to:
1. Open an issue for discussion
2. Fork the repo and experiment
3. Share how you've adapted this methodology for your use case


## Contact

Have questions about the methodology or want to discuss similar projects?

Reach out via [LinkedIn](https://www.linkedin.com/in/qurat-ul-ain-236b60133/) or [email](quratulain_izhar@hotmial.com)


**Last Updated**: January 2026

