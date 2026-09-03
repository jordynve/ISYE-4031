# ISYE 4031 Homework 1 - Analysis and Results

## Overview

This directory contains a complete analysis of ISYE 4031 Homework 1: Statistical Review, Forecast Baselines, and Agent Audit.

The analysis covers:
- **Part 1**: Descriptive statistics and uncertainty quantification using 14 training observations of daily maximum temperatures
- **Part 2**: Development and evaluation of two transparent forecast baselines
- **Part 3**: One-sample hypothesis testing on melting point data
- **Part 4**: Audit of proposed statistical code and corrected implementation with automated tests

## Files

- `analysis.py` - Main analysis script containing all calculations and plots
- `test_analysis.py` - Automated test suite (12 tests, all passing)
- `AI_USAGE.md` - AI assistance audit trail
- `README.md` - This file
- `part1a_plot.png` - Plot of temperatures with training/held-out distinction
- `part2a_plot.png` - Plot of forecast baselines

## Required Environment

**Python**: 3.12.11  
**Virtual Environment**: .venv (configured as venv)

### Required Packages

```
numpy==2.2.6
pandas==2.2.3
scipy==1.15.3
statsmodels==0.14.4
scikit-learn==1.6.1
matplotlib==3.10.3
seaborn==0.13.2
jupyterlab==4.4.3
ipykernel==6.29.5
openpyxl==3.1.5
pytest==8.4.1
```

## Quick Start - Reproducing All Results

### 1. Run the Analysis

```bash
python analysis.py
```

This generates:
- Comprehensive text output with all numerical results
- `part1a_plot.png` - Temperature plot with confidence/prediction intervals
- `part2a_plot.png` - Baseline forecast comparison plot
- All intermediate calculations and interpretations

**Expected Output**: 
- Training statistics summary
- 95% confidence interval for population mean: [89.0160, 92.2698]
- 95% prediction interval for new observation: [84.3419, 96.9438]
- Forecast evaluation metrics for both baselines
- Hypothesis test results with p-value = 0.0917
- Type II error probability

### 2. Run All Tests

```bash
pytest -q
```

**Expected Output**:
```
............                                                             [100%]
12 passed in 0.95s
```

Verify that all 12 tests pass:
- test_training_stats_invariant_to_held_out_values
- test_held_out_not_in_training_calculation
- test_sample_std_uses_n_minus_1_denominator
- test_denominator_impact_on_variance
- test_prediction_interval_wider_than_ci
- test_ci_pi_width_ratio
- test_reproducibility_of_calculations
- test_reproducibility_of_bootstrap_independent_stats
- test_hypothesis_test_calculations
- test_type_ii_error_calculation
- test_data_length_and_split
- test_baseline_forecast_lengths

## Key Results Summary

### Part 1: Descriptive Statistics
- Training Mean: 90.6429°F
- Training Std Dev (n-1): 2.8177°F
- 95% CI for mean: [89.0160, 92.2698]
- 95% PI for single obs: [84.3419, 96.9438]

### Part 2: Forecast Baselines
- Mean Baseline RMSE: 3.1824°F (better)
- Last-Value Baseline RMSE: 3.3417°F
- Recommended: Mean baseline

### Part 3: Hypothesis Test
- H₀: μ = 155°F vs Hₐ: μ ≠ 155°F
- Test Statistic: z = -1.6865
- P-value: 0.0917 (fail to reject H₀ at α=0.01)
- Type II Error (μ=150): β ≈ 0.00000

### Part 4: Code Audit
- Identified 5 distinct problems in proposed code
- All corrected in analysis.py
- 12 automated tests verify correct implementation

## Data Integrity Guarantees

All calculations respect the temporal information cutoff:
- Training period: Days 1-14 (14 observations)
- Held-out period: Days 15-20 (6 observations)
- No held-out values used in any training calculations
- No held-out values used in baseline construction
- No held-out values used in confidence/prediction interval estimation

This is verified by:
- `test_training_stats_invariant_to_held_out_values`: ✓ PASS
- `test_held_out_not_in_training_calculation`: ✓ PASS

## Reproducibility

All results are perfectly reproducible:
- Verified by `test_reproducibility_of_calculations`: 10 consecutive runs produce identical results
- Verified by `test_reproducibility_of_bootstrap_independent_stats`: 5 runs produce identical results
- No randomness involved in any calculation
- All analyses use deterministic mathematical formulas

Run any of the above commands multiple times - all outputs will be identical.

## Detailed Analysis Sections

For detailed explanations and interpretations, see the console output from
`analysis.py` and the implementation details in `test_analysis.py`.

## Validation Checklist

Before submission, verify:

- [x] analysis.py produces all numerical results
- [x] pytest -q passes all 12 tests
- [x] No held-out observations used in training
- [x] Sample std dev uses n-1 denominator
- [x] Prediction interval is wider than confidence interval
- [x] Repeated runs produce identical results
- [x] AI_USAGE.md documents assistance received
- [x] README.md provides exact reproduction commands

## Author Notes

The analysis is complete and ready for submission. All requirements from the assignment specification are satisfied:

1. ✓ Descriptive summaries and uncertainty (Part 1, 25 points)
2. ✓ Forecast baselines and evaluation (Part 2, 22 points)
3. ✓ One-sample inference (Part 3, 24 points)
4. ✓ Agent audit and automated tests (Part 4, 24 points)
5. ✓ AI Usage Statement (5 points)

Total: 100 points

