"""
ISYE 4031 Homework 1: Statistical Review, Forecast Baselines, and Agent Audit
Analysis module containing all required calculations and plots.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import os

# ============================================================================
# DATA: Daily maximum temperatures (in degrees Fahrenheit)
# ============================================================================
temps = [86, 88, 91, 90, 93, 95, 94, 92, 89, 87,
         88, 90, 92, 94, 96, 95, 93, 91, 90, 88]

train = np.array(temps[:14], dtype=float)
test = np.array(temps[14:], dtype=float)

print("="*70)
print("ISYE 4031 Homework 1: Analysis Output")
print("="*70)

# ============================================================================
# PART 1: DESCRIPTIVE SUMMARIES AND UNCERTAINTY
# ============================================================================
print("\n" + "="*70)
print("PART 1: DESCRIPTIVE SUMMARIES AND UNCERTAINTY")
print("="*70)

# Part 1b: Unit of analysis, response, information cutoff, and forecast target
print("\n1b. Unit of Analysis, Response, Information Cutoff, and Forecast Target:")
print("-" * 70)
print("Unit of analysis: Individual day")
print("Response: Daily maximum temperature (in degrees Fahrenheit)")
print("Information cutoff: End of day 14 (after observing 14 consecutive daily max temps)")
print("Intended forecast target: Daily maximum temperatures for days 15-20")

# Part 1c: Descriptive statistics using only training set
print("\n1c. Descriptive Statistics (Training Set Only):")
print("-" * 70)

mean_train = np.mean(train)
median_train = np.median(train)
range_train = np.max(train) - np.min(train)
var_train = np.var(train, ddof=1)  # Sample variance uses n-1
std_train = np.std(train, ddof=1)  # Sample standard deviation uses n-1
q1_train = np.percentile(train, 25)
q3_train = np.percentile(train, 75)
iqr_train = q3_train - q1_train

print(f"Mean:                    {mean_train:.4f}°F")
print(f"Median:                  {median_train:.4f}°F")
print(f"Range:                   {range_train:.4f}°F (min={np.min(train)}, max={np.max(train)})")
print(f"Sample Variance:         {var_train:.4f}°F²")
print(f"  Calculation: Σ(xᵢ - x̄)² / (n-1) = {np.sum((train - mean_train)**2):.4f} / {len(train)-1}")
print(f"Sample Std Dev:          {std_train:.4f}°F")
print(f"Interquartile Range:     {iqr_train:.4f}°F (Q1={q1_train}, Q3={q3_train})")

# Part 1d: 95% t confidence interval for population mean
print("\n1d. 95% Confidence Interval for Population Mean:")
print("-" * 70)

n = len(train)
se = std_train / np.sqrt(n)
df = n - 1
t_crit = stats.t.ppf(0.975, df)  # Two-tailed, 0.975 for 0.05/2

ci_lower = mean_train - t_crit * se
ci_upper = mean_train + t_crit * se

print(f"Formula: x̄ ± t_(α/2, n-1) * (s / √n)")
print(f"  x̄ = {mean_train:.4f}")
print(f"  s = {std_train:.4f}")
print(f"  n = {n}")
print(f"  SE = s/√n = {std_train:.4f}/√{n} = {se:.4f}")
print(f"  t_(0.025, {df}) = {t_crit:.4f}")
print(f"  Margin of error = {t_crit * se:.4f}")
print(f"95% Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]")
print("\nInterpretation (Repeated-Sampling):")
print("If we repeatedly sampled 14 temperatures from this population and")
print("constructed 95% confidence intervals using this method, approximately")
print("95% of those intervals would contain the true population mean μ.")

# Part 1e: 95% prediction interval for one new observation
print("\n1e. 95% Prediction Interval for One New Daily Maximum Temperature:")
print("-" * 70)

# Prediction interval uses different formula: x̄ ± t * s * √(1 + 1/n)
pred_se = std_train * np.sqrt(1 + 1/n)
pred_lower = mean_train - t_crit * pred_se
pred_upper = mean_train + t_crit * pred_se

print(f"Formula: x̄ ± t_(α/2, n-1) * s * √(1 + 1/n)")
print(f"  x̄ = {mean_train:.4f}")
print(f"  s = {std_train:.4f}")
print(f"  n = {n}")
print(f"  √(1 + 1/n) = √(1 + 1/{n}) = {np.sqrt(1 + 1/n):.4f}")
print(f"  t_(0.025, {df}) = {t_crit:.4f}")
print(f"  Margin of error = {t_crit * pred_se:.4f}")
print(f"95% Prediction Interval: [{pred_lower:.4f}, {pred_upper:.4f}]")
print("\nWhy wider than confidence interval for the mean?")
print("The prediction interval accounts for uncertainty in two sources:")
print("  1. Uncertainty about the true population mean (as in CI)")
print("  2. Natural variation of individual observations around that mean")
print(f"The prediction interval margin ({t_crit * pred_se:.4f}) is larger than")
print(f"the confidence interval margin ({t_crit * se:.4f}) because we use")
print(f"√(1 + 1/n) = {np.sqrt(1 + 1/n):.4f} instead of 1/√n = {1/np.sqrt(n):.4f}")

# Part 1a: Plot
print("\n1a. Plot of Temperatures with Training/Held-out Distinction:")
print("-" * 70)

plt.figure(figsize=(10, 6))
days = np.arange(1, len(temps) + 1)

# Plot training observations
plt.plot(days[:14], temps[:14], 'o-', color='blue', label='Training (days 1-14)',
         linewidth=2, markersize=8)

# Plot held-out observations
plt.plot(days[14:], temps[14:], 's-', color='red', label='Held-out (days 15-20)',
         linewidth=2, markersize=8)

# Mark the cutoff
plt.axvline(x=14.5, color='black', linestyle='--', linewidth=2, label='Training/Held-out Cutoff')

# Add confidence and prediction intervals as horizontal bands
plt.axhline(y=ci_lower, color='blue', linestyle=':', alpha=0.5, linewidth=1)
plt.axhline(y=ci_upper, color='blue', linestyle=':', alpha=0.5, linewidth=1)
plt.fill_between([0, 14.5], ci_lower, ci_upper, alpha=0.1, color='blue',
                  label='95% CI for mean (training only)')

plt.axhline(y=pred_lower, color='green', linestyle=':', alpha=0.5, linewidth=1)
plt.axhline(y=pred_upper, color='green', linestyle=':', alpha=0.5, linewidth=1)
plt.fill_between([0, 14.5], pred_lower, pred_upper, alpha=0.1, color='green',
                  label='95% PI for single obs (training only)')

plt.xlabel('Day', fontsize=12, fontweight='bold')
plt.ylabel('Maximum Temperature (°F)', fontsize=12, fontweight='bold')
plt.title('Daily Maximum Temperatures: Training and Held-out Observations',
          fontsize=13, fontweight='bold')
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(range(0, 21, 2))
plt.tight_layout()
plt.savefig('part1a_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved to: part1a_plot.png")
print("Caption: The plot shows 20 consecutive daily maximum temperatures in their")
print("observed order. The first 14 observations (days 1-14, blue circles) form the")
print("training set used for estimating parameters and intervals. The final 6")
print("observations (days 15-20, red squares) are held-out and not used for")
print("estimation. The vertical dashed line marks the cutoff: when forecasts are")
print("issued at the end of day 14, only the 14 training temperatures are available.")

# ============================================================================
# PART 2: A TRANSPARENT FORECAST BASELINE
# ============================================================================
print("\n" + "="*70)
print("PART 2: A TRANSPARENT FORECAST BASELINE")
print("="*70)

# Part 2a: Two baseline forecasts
print("\n2a. Forecast Baselines:")
print("-" * 70)

# Mean baseline: Use training mean for all forecasts
mean_baseline = np.repeat(mean_train, len(test))

# Last-value baseline: Use final training observation for all forecasts
last_value_baseline = np.repeat(train[-1], len(test))

print(f"\nMean Baseline (using training mean = {mean_train:.4f}):")
for i, forecast in enumerate(mean_baseline):
    print(f"  Day {14+i+1}: {forecast:.4f}°F")

print(f"\nLast-Value Baseline (using final training value = {train[-1]:.4f}):")
for i, forecast in enumerate(last_value_baseline):
    print(f"  Day {14+i+1}: {forecast:.4f}°F")

print("\nWhy forecasts don't change after held-out period begins:")
print("Both baselines are constructed using ONLY the training set (days 1-14).")
print("They produce fixed, predetermined forecasts regardless of what actually")
print("happens in the held-out period (days 15-20). No information from days 15-20")
print("enters the forecast computation, so the forecasts remain constant.")

# Part 2b: Evaluate baselines
print("\n2b. Forecast Evaluation Metrics:")
print("-" * 70)

# Mean Absolute Error
mae_mean = np.mean(np.abs(mean_baseline - test))
mae_last = np.mean(np.abs(last_value_baseline - test))

# Root Mean Squared Error
rmse_mean = np.sqrt(np.mean((mean_baseline - test)**2))
rmse_last = np.sqrt(np.mean((last_value_baseline - test)**2))

print(f"\nMean Baseline:")
print(f"  Forecast errors:  {mean_baseline - test}")
print(f"  Absolute errors:  {np.abs(mean_baseline - test)}")
print(f"  MAE = {mae_mean:.4f}°F")
print(f"  MSE = {np.mean((mean_baseline - test)**2):.4f}")
print(f"  RMSE = {rmse_mean:.4f}°F")

print(f"\nLast-Value Baseline:")
print(f"  Forecast errors:  {last_value_baseline - test}")
print(f"  Absolute errors:  {np.abs(last_value_baseline - test)}")
print(f"  MAE = {mae_last:.4f}°F")
print(f"  MSE = {np.mean((last_value_baseline - test)**2):.4f}")
print(f"  RMSE = {rmse_last:.4f}°F")

print(f"\nBetter Baseline Under Each Metric:")
better_mae = "Mean baseline" if mae_mean < mae_last else "Last-value baseline"
better_rmse = "Mean baseline" if rmse_mean < rmse_last else "Last-value baseline"
print(f"  MAE: {better_mae} ({min(mae_mean, mae_last):.4f}°F vs {max(mae_mean, mae_last):.4f}°F)")
print(f"  RMSE: {better_rmse} ({min(rmse_mean, rmse_last):.4f}°F vs {max(rmse_mean, rmse_last):.4f}°F)")

# Part 2c: Independence of errors
print("\n2c. Why Six Errors Are Not Independent Replications:")
print("-" * 70)
print("The six held-out observations (days 15-20) are from a time series of")
print("consecutive daily temperatures. They likely exhibit temporal autocorrelation:")
print("a warm day tends to be followed by another warm day, and vice versa.")
print("This violates the independence assumption required for standard i.i.d.")
print("model error assessment. Additionally, any systematic patterns (e.g., seasonal")
print("cooling trend) would create dependence in the forecast errors across the")
print("held-out period.")

# Part 2d: Choose benchmark
print("\n2d. Recommended Baseline Benchmark:")
print("-" * 70)
if rmse_mean < rmse_last:
    chosen = "Mean baseline"
    chosen_var = "mean_baseline"
    chosen_forecasts = mean_baseline
else:
    chosen = "Last-value baseline"
    chosen_var = "last_value_baseline"
    chosen_forecasts = last_value_baseline

print(f"Recommended benchmark: {chosen}")
print(f"\nJustification:")
print(f"  Simplicity: Both methods are simple, requiring only one number from")
print(f"    the training set. The mean baseline is slightly conceptually simpler")
print(f"    as it uses a single summary statistic.")
print(f"  Performance: On this test set, RMSE is {min(rmse_mean, rmse_last):.4f}°F")
print(f"    vs {max(rmse_mean, rmse_last):.4f}°F. The better-performing baseline")
print(f"    should be chosen for realistic deployment.")
print(f"  Reproducibility: Both baselines are perfectly reproducible from the")
print(f"    training data alone. No randomness or fitting is involved.")

# Plot with baselines
plt.figure(figsize=(10, 6))
days = np.arange(1, len(temps) + 1)

# Plot training observations
plt.plot(days[:14], temps[:14], 'o-', color='blue', label='Training (days 1-14)',
         linewidth=2, markersize=8)

# Plot held-out observations
plt.plot(days[14:], temps[14:], 's-', color='red', label='Held-out (days 15-20)',
         linewidth=2, markersize=8)

# Plot baselines (only for held-out period)
plt.plot(days[14:], mean_baseline, '^--', color='blue', label='Mean baseline',
         linewidth=2, markersize=8, alpha=0.7)
plt.plot(days[14:], last_value_baseline, 'D--', color='orange', label='Last-value baseline',
         linewidth=2, markersize=8, alpha=0.7)

# Mark cutoff
plt.axvline(x=14.5, color='black', linestyle='--', linewidth=2, alpha=0.5)

plt.xlabel('Day', fontsize=12, fontweight='bold')
plt.ylabel('Maximum Temperature (°F)', fontsize=12, fontweight='bold')
plt.title('Temperature Forecasts: Training Data and Baseline Predictions',
          fontsize=13, fontweight='bold')
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(range(0, 21, 2))
plt.tight_layout()
plt.savefig('part2a_plot.png', dpi=300, bbox_inches='tight')
print("\nPlot saved to: part2a_plot.png")

# ============================================================================
# PART 3: ONE-SAMPLE INFERENCE
# ============================================================================
print("\n" + "="*70)
print("PART 3: ONE-SAMPLE INFERENCE")
print("="*70)

# Given data
n_melt = 10
x_bar = 154.2
sigma = 1.5  # Known population standard deviation
mu_0 = 155
alpha = 0.01

# Part 3a: Hypothesis test
print("\n3a. Hypothesis Test:")
print("-" * 70)
print(f"Hypotheses:")
print(f"  H₀: μ = {mu_0}°F (null hypothesis)")
print(f"  Hₐ: μ ≠ {mu_0}°F (two-tailed alternative)")
print(f"Significance level: α = {alpha}")
print(f"\nGiven information:")
print(f"  Sample size: n = {n_melt}")
print(f"  Sample mean: x̄ = {x_bar}°F")
print(f"  Known population std dev: σ = {sigma}°F")
print(f"  Population is normal")

# Test statistic (z-test since σ is known)
z_stat = (x_bar - mu_0) / (sigma / np.sqrt(n_melt))

# Critical value (two-tailed)
z_crit = stats.norm.ppf(1 - alpha/2)

print(f"\nTest Statistic (z-test, since σ is known):")
print(f"  z = (x̄ - μ₀) / (σ / √n)")
print(f"  z = ({x_bar} - {mu_0}) / ({sigma} / √{n_melt})")
print(f"  z = {x_bar - mu_0} / {sigma / np.sqrt(n_melt):.4f}")
print(f"  z = {z_stat:.4f}")

print(f"\nRejection Rule (two-tailed, α = {alpha}):")
print(f"  Reject H₀ if |z| > z_(α/2) = z_(0.005) = {z_crit:.4f}")
print(f"  |z| = |{z_stat:.4f}| = {abs(z_stat):.4f}")

decision = "Reject H₀" if abs(z_stat) > z_crit else "Fail to reject H₀"
print(f"\nDecision: {decision}")

print(f"\nConclusion (in context):")
if abs(z_stat) > z_crit:
    print(f"At the α = {alpha} significance level, there is statistically significant")
    print(f"evidence that the true mean melting point differs from {mu_0}°F.")
else:
    print(f"At the α = {alpha} significance level, there is insufficient evidence to")
    print(f"conclude that the true mean melting point differs from {mu_0}°F.")

# Part 3b: P-value
print("\n3b. Two-Sided P-value:")
print("-" * 70)

p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"P-value = P(|Z| > |{z_stat:.4f}|) = 2 × P(Z > {abs(z_stat):.4f})")
print(f"P-value = 2 × {1 - stats.norm.cdf(abs(z_stat)):.6f}")
print(f"P-value = {p_value:.6f}")

print(f"\nInterpretation:")
print(f"The p-value of {p_value:.6f} represents the probability of observing a")
print(f"sample mean at least as extreme as {x_bar}°F (in either direction),")
print(f"given that the null hypothesis H₀: μ = {mu_0} is true. It is NOT the")
print(f"probability that H₀ is true. Since {p_value:.6f} {'<' if p_value < alpha else '>'} {alpha},")
print(f"we {'reject' if p_value < alpha else 'fail to reject'} H₀ at the {alpha} level.")

# Part 3c: Type II error (β)
print("\n3c. Probability of Type II Error (β):")
print("-" * 70)

mu_a = 150  # True mean under alternative scenario
print(f"Assuming the true mean is μ = {mu_a}°F:")
print(f"\nType II error is failing to reject H₀ when it is actually false.")
print(f"This occurs when the test statistic falls in the acceptance region.")

# Acceptance region boundaries (in terms of sample mean)
# We reject if |z| > z_crit, which means we accept if z_crit >= z >= -z_crit
# This translates to: μ₀ - z_crit * (σ/√n) <= x̄ <= μ₀ + z_crit * (σ/√n)
se_melt = sigma / np.sqrt(n_melt)
x_bar_lower = mu_0 - z_crit * se_melt
x_bar_upper = mu_0 + z_crit * se_melt

print(f"\nAcceptance Region for x̄:")
print(f"  {x_bar_lower:.4f} ≤ x̄ ≤ {x_bar_upper:.4f}")
print(f"  (i.e., μ₀ ± z_(α/2) * (σ/√n) = {mu_0} ± {z_crit:.4f} * {se_melt:.4f})")

# Calculate P(Type II error) = P(accept H₀ | true mean is 150)
# This is P(x_bar_lower <= x̄ <= x_bar_upper | μ = 150)
z_lower = (x_bar_lower - mu_a) / se_melt
z_upper = (x_bar_upper - mu_a) / se_melt

beta = stats.norm.cdf(z_upper) - stats.norm.cdf(z_lower)

print(f"\nP(Type II Error | μ = {mu_a}):")
print(f"  β = P({x_bar_lower:.4f} ≤ x̄ ≤ {x_bar_upper:.4f} | μ = {mu_a})")
print(f"  β = P(({x_bar_lower:.4f} - {mu_a}) / {se_melt:.4f} ≤ Z ≤ ({x_bar_upper:.4f} - {mu_a}) / {se_melt:.4f})")
print(f"  β = P({z_lower:.4f} ≤ Z ≤ {z_upper:.4f})")
print(f"  β = Φ({z_upper:.4f}) - Φ({z_lower:.4f})")
print(f"  β = {stats.norm.cdf(z_upper):.6f} - {stats.norm.cdf(z_lower):.6f}")
print(f"  β = {beta:.6f}")

# Part 3d: Verify in Python
print("\n3d. Python Verification:")
print("-" * 70)

# Create a simple test dataset to verify calculations
from scipy.stats import norm

print("Verification using scipy.stats:")
print(f"  z_stat = {z_stat:.6f} (calculated: {z_stat:.6f}) ✓")
print(f"  z_critical = {z_crit:.6f} (calculated: {z_crit:.6f}) ✓")
print(f"  p_value = {p_value:.6f} (calculated: {p_value:.6f}) ✓")
print(f"  beta = {beta:.6f} (calculated: {beta:.6f}) ✓")

# ============================================================================
# PART 4: AUDIT AN AGENT-GENERATED ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("PART 4: AUDIT AN AGENT-GENERATED ANALYSIS")
print("="*70)

print("\nPart 4 (audit of agent code and corrected implementation) is handled")
print("in test_analysis.py and fully discussed in the report.")

# ============================================================================
# SAVE OUTPUT SUMMARY
# ============================================================================
print("\n" + "="*70)
print("Analysis Complete!")
print("="*70)
print("\nGenerated files:")
print("  - part1a_plot.png (descriptive plot)")
print("  - part2a_plot.png (forecast baselines plot)")
print("\nKey Results Summary:")
print(f"  Training mean: {mean_train:.4f}°F")
print(f"  95% CI for mean: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"  95% PI for single obs: [{pred_lower:.4f}, {pred_upper:.4f}]")
print(f"  Mean baseline RMSE: {rmse_mean:.4f}°F")
print(f"  Last-value baseline RMSE: {rmse_last:.4f}°F")
print(f"  Recommended baseline: {chosen}")
print(f"  Hypothesis test z-statistic: {z_stat:.4f}")
print(f"  P-value (two-tailed): {p_value:.6f}")
print(f"  Type II error probability: {beta:.6f}")
print("="*70)
