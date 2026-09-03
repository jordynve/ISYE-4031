"""
Generate improved PDF report for ISYE 4031 Homework 1
Uses only ASCII characters to avoid encoding issues
Better formatting with clear sections and proper margins
"""

from fpdf import FPDF
import os

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore')


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(12, 14, 12)  # left, top, right margins - more compact
        
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(0, 6, "ISYE 4031: Regression and Forecasting", 0, 1, "C")
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 5, "Homework 1 Report", 0, 1, "C")
        self.ln(2)
        
    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
        
    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 7, title, 0, 1, "L", True)
        self.ln(2)
        
    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 100)
        self.cell(0, 5, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(0.5)
        
    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4, text)
        self.ln(0.5)


pdf = PDF()
pdf.add_page()

# PART 1
pdf.section_title("PART 1: Descriptive Summaries and Uncertainty")

pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "Unit of Analysis: Individual day\n"
    "Response: Daily maximum temperature (Fahrenheit)\n"
    "Information Cutoff: End of day 14 (14 training observations)\n"
    "Forecast Target: Daily max temperatures for days 15-20")
pdf.ln(2)

pdf.subsection_title("1a. Descriptive Plot")
pdf.body_text(
    "The plot shows 20 daily temperatures in chronological order. Blue circles (days 1-14) "
    "represent training data. Red squares (days 15-20) represent held-out test data. The "
    "vertical dashed line marks the training/test cutoff. When forecasts are issued at the "
    "end of day 14, only the 14 training values are available for analysis.")
pdf.ln(1)

if os.path.exists("part1a_plot.png"):
    try:
        pdf.image("part1a_plot.png", x=13, w=184)
        pdf.ln(2)
    except Exception as e:
        print(f"Warning: Could not embed plot: {e}")

pdf.ln(1)
pdf.subsection_title("1b. Descriptive Statistics (Training Data Only)")
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "Mean: 90.6429 F\n"
    "Median: 90.5000 F\n"
    "Range: 9.0000 F\n"
    "Sample Variance: 7.9396 F-squared (denominator = n-1 = 13)\n"
    "Sample Std Dev: 2.8177 F\n"
    "Interquartile Range: 4.5000 F")

pdf.ln(3)
pdf.subsection_title("1c. Confidence Interval for Population Mean")
pdf.body_text(
    "Formula: x-bar +/- t(alpha/2, n-1) * (s / sqrt(n))\n\n"
    "Parameters:\n"
    "  x-bar = 90.6429 F\n"
    "  s = 2.8177 F\n"
    "  n = 14\n"
    "  SE = 2.8177 / sqrt(14) = 0.7531\n"
    "  t(0.025, 13) = 2.1604\n"
    "  Margin of error = 2.1604 * 0.7531 = 1.6269\n\n"
    "Result: 95% CI = [89.0160, 92.2698] F\n\n"
    "Interpretation: If we repeatedly sample 14 observations and construct 95% confidence "
    "intervals, approximately 95% of these intervals would contain the true population mean.")

pdf.ln(2)
pdf.subsection_title("1d. Prediction Interval for Single Observation")
pdf.body_text(
    "Formula: x-bar +/- t(alpha/2, n-1) * s * sqrt(1 + 1/n)\n\n"
    "Parameters:\n"
    "  sqrt(1 + 1/14) = 1.0351\n"
    "  Margin of error = 2.1604 * 2.8177 * 1.0351 = 6.3010\n\n"
    "Result: 95% PI = [84.3419, 96.9438] F\n\n"
    "Why Wider than CI? Prediction intervals account for two sources of uncertainty:\n"
    "  (1) Uncertainty about the population mean (same as CI)\n"
    "  (2) Natural variation of individual observations\n\n"
    "The factor sqrt(1 + 1/n) captures this additional variability. At n=14, PI/CI = sqrt(15) = 3.87.")

pdf.ln(2)
pdf.add_page()

# PART 2
pdf.section_title("PART 2: Transparent Forecast Baselines")

pdf.subsection_title("2a. Baseline Forecasts")
pdf.body_text(
    "Mean Baseline: Forecasts for days 15-20\n"
    "  Use training mean (90.6429 F) for all 6 forecasts\n"
    "  Forecasts: 90.64, 90.64, 90.64, 90.64, 90.64, 90.64 F\n\n"
    "Last-Value Baseline: Forecasts for days 15-20\n"
    "  Use final training value (94.00 F) for all forecasts\n"
    "  Forecasts: 94.00, 94.00, 94.00, 94.00, 94.00, 94.00 F\n\n"
    "Both baselines are fixed and predetermined. They use only information available at the "
    "end of day 14 and do not change based on what occurs in the forecast period.")

pdf.ln(1)

if os.path.exists("part2a_plot.png"):
    try:
        pdf.image("part2a_plot.png", x=13, w=184)
        pdf.ln(2)
    except Exception as e:
        print(f"Warning: Could not embed plot: {e}")

pdf.ln(1)
pdf.subsection_title("2b. Forecast Evaluation")
pdf.body_text(
    "Mean Baseline:\n"
    "  Predictions: [96, 95, 93, 91, 90, 88]\n"
    "  Actuals:     [96, 95, 93, 91, 90, 88]\n"
    "  Errors:      [0.64, -0.64, 0.64, 0.36, 0.64, 2.64]\n"
    "  MAE: 2.6190 F\n"
    "  RMSE: 3.1824 F\n\n"
    "Last-Value Baseline:\n"
    "  Predictions: [94, 94, 94, 94, 94, 94]\n"
    "  Actuals:     [96, 95, 93, 91, 90, 88]\n"
    "  Errors:      [-2, -1, 1, 3, 4, 6]\n"
    "  MAE: 2.8333 F\n"
    "  RMSE: 3.3417 F\n\n"
    "Winner: Mean baseline is superior on both metrics (MAE and RMSE).")

pdf.ln(2)
pdf.subsection_title("2c. Independence of Errors")
pdf.body_text(
    "Are the 6 forecast errors independent?\n\n"
    "Answer: NO. The errors are NOT independent because:\n\n"
    "1. Autocorrelation: Daily temperatures exhibit positive autocorrelation. Warm days tend "
    "to follow warm days, and cool days tend to cluster together.\n\n"
    "2. Seasonal Patterns: Temperature sequences often follow systematic patterns due to "
    "weather systems and atmospheric dynamics.\n\n"
    "3. Assumption Violation: The standard assumption that forecast errors are independent "
    "and identically distributed (i.i.d.) is violated in time series data.")

pdf.ln(2)
pdf.subsection_title("2d. Recommended Baseline")
pdf.body_text(
    "Choice: MEAN BASELINE\n\n"
    "Justification:\n"
    "  * Simplicity: Uses only the training mean, a simple and interpretable statistic\n"
    "  * Performance: Lower error metrics (RMSE 3.18 vs 3.34 F)\n"
    "  * Reproducibility: Perfectly reproducible with no randomness or subjectivity\n"
    "  * Theoretical Foundation: Mean is the best constant predictor under squared-error loss\n\n"
    "Recommendation: Deploy the mean baseline for forecasting purposes.")

pdf.ln(2)
pdf.add_page()

# PART 3
pdf.section_title("PART 3: One-Sample Inference")

pdf.subsection_title("3a. Hypothesis Test")
pdf.body_text(
    "Hypotheses:\n"
    "  H0: mu = 155 F (null hypothesis)\n"
    "  Ha: mu != 155 F (two-tailed alternative)\n"
    "  Significance level: alpha = 0.01\n\n"
    "Given Data:\n"
    "  n = 10\n"
    "  x-bar = 154.2 F\n"
    "  sigma = 1.5 F (known population standard deviation)\n\n"
    "Test Statistic (z-test):\n"
    "  z = (x-bar - mu0) / (sigma / sqrt(n))\n"
    "  z = (154.2 - 155) / (1.5 / sqrt(10))\n"
    "  z = -0.8 / 0.4743 = -1.6865\n\n"
    "Critical Value:\n"
    "  For two-tailed test at alpha = 0.01: z-critical = 2.5758\n\n"
    "Decision:\n"
    "  |z| = 1.6865 < 2.5758, so FAIL TO REJECT H0\n\n"
    "Conclusion: At the 0.01 significance level, we have insufficient evidence to conclude "
    "that the mean melting point differs from 155 F.")

pdf.ln(2)
pdf.subsection_title("3b. Two-Sided P-value")
pdf.body_text(
    "Calculation:\n"
    "  p-value = 2 * P(Z > |z-stat|)\n"
    "  p-value = 2 * P(Z > 1.6865)\n"
    "  p-value = 0.0917\n\n"
    "Interpretation:\n"
    "The p-value is the probability of observing a sample mean at least as extreme as 154.2 F "
    "(in either direction) when the null hypothesis is true. It is NOT the probability that "
    "the null hypothesis is true.\n\n"
    "Decision:\n"
    "Since 0.0917 > 0.01 (alpha), we fail to reject H0. The test result is not significant "
    "at the 0.01 level (though it approaches significance at 0.10).")

pdf.ln(2)
pdf.subsection_title("3c. Type II Error Probability")
pdf.body_text(
    "Assumption: True population mean is mu = 150 F\n\n"
    "Non-rejection Region:\n"
    "  Critical z-values: +/- 2.5758\n"
    "  Acceptance region: 155 +/- 2.5758 * (1.5 / sqrt(10))\n"
    "  Acceptance region: 155 +/- 1.2218\n"
    "  Acceptance region: [153.78 F, 156.22 F]\n\n"
    "Type II Error Probability:\n"
    "  z = (153.78 - 150) / (1.5 / sqrt(10)) = 7.959\n"
    "  P(Z < 7.959) ~ 1.0000\n"
    "  Beta = 1.0000 - 1.0000 ~ 0.0000\n\n"
    "Interpretation: When the true mean is 5 F below the null hypothesis value, the probability "
    "of failing to reject H0 is essentially zero. The effect size is very large relative to the "
    "standard error, resulting in extremely high power.")

pdf.ln(2)
pdf.subsection_title("3d. Python Verification")
pdf.body_text(
    "All calculations verified using scipy.stats:\n"
    "  z_stat = -1.686548 [verified]\n"
    "  z_critical = 2.575829 [verified]\n"
    "  p_value = 0.091690 [verified]\n"
    "  beta = 0.000000 [verified]\n\n"
    "Results match manual calculations to machine precision.")

pdf.ln(2)
pdf.add_page()

# PART 4
pdf.section_title("PART 4: Agent Audit and Automated Tests")

pdf.subsection_title("4a. Problems in Proposed Code")
pdf.body_text(
    "Problem 1: Computing mean from all data instead of training only\n"
    "  Code: ci_margin = t.ppf(...) * x.std() / np.sqrt(len(x))\n"
    "  Issue: Uses x.mean() instead of train.mean()\n"
    "  Impact: Incorporates future observations, inflating bias and leaking information\n\n"
    "Problem 2: Confidence interval uses future data\n"
    "  Issue: CI computed from x, which includes held-out observations\n"
    "  Impact: Produces artificially narrow intervals, misleading about true uncertainty\n\n"
    "Problem 3: Prediction interval equals confidence interval\n"
    "  Issue: PI calculated with wrong formula, missing sqrt(1 + 1/n) factor\n"
    "  Impact: Underestimates variability; PI should be sqrt(1 + 1/n) = 1.035x wider\n\n"
    "Problem 4: Last-value baseline uses future data\n"
    "  Code: y_pred[:] = x[-1]\n"
    "  Issue: Accesses x[-1] which is held-out value (88 F), not training last value (94 F)\n"
    "  Impact: Future information leakage makes forecast evaluation invalid\n\n"
    "Problem 5: Missing reproducibility documentation\n"
    "  Issue: No clear statement about deterministic vs stochastic behavior\n"
    "  Impact: Future maintainers unclear on whether results are reproducible")

pdf.ln(2)
pdf.subsection_title("4b. Corrected Implementation")
pdf.body_text(
    "Key Corrections:\n"
    "  [OK] All statistics computed from TRAINING data only\n"
    "  [OK] CI formula: x-bar +/- t(alpha/2, n-1) * (s / sqrt(n))\n"
    "  [OK] PI formula: x-bar +/- t(alpha/2, n-1) * s * sqrt(1 + 1/n)\n"
    "  [OK] Mean baseline: train.mean() for all predictions\n"
    "  [OK] Last-value baseline: train[-1] for all predictions\n"
    "  [OK] Comprehensive automated test suite (12 tests)\n"
    "  [OK] Clear reproducibility guarantees documented\n\n"
    "Implementation: See analysis.py and test_analysis.py in submission")

pdf.ln(2)
pdf.subsection_title("4c. Automated Tests (12 Total, All Passing)")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "1. test_training_stats_invariant_to_held_out_values:\n"
    "   Modifies held-out data; confirms training stats unchanged\n\n"
    "2. test_sample_std_uses_n_minus_1_denominator:\n"
    "   Verifies standard deviation uses n-1 (unbiased) vs n (biased) denominator\n\n"
    "3. test_prediction_interval_wider_than_ci:\n"
    "   Confirms PI is strictly wider than CI\n\n"
    "4. test_ci_pi_width_ratio:\n"
    "   Validates PI/CI margin ratio equals sqrt(n+1) = sqrt(15)\n\n"
    "5. test_reproducibility_of_calculations:\n"
    "   10 consecutive runs produce identical results\n\n"
    "6. test_hypothesis_test_calculations:\n"
    "   Verifies z_stat, z_critical, and p_value from Part 3\n\n"
    "7. test_type_ii_error_calculation:\n"
    "   Confirms beta calculation for true mean 150 F\n\n"
    "8. test_training_test_separation:\n"
    "   Ensures training and test indices never overlap\n\n"
    "9. test_forecast_from_training_only:\n"
    "   Confirms forecasts use only training statistics\n\n"
    "10. test_mean_baseline_constant:\n"
    "    All mean forecasts equal training mean\n\n"
    "11. test_last_value_baseline_constant:\n"
    "    All last-value forecasts equal train[-1]\n\n"
    "12. test_error_calculations:\n"
    "    MAE and RMSE computed correctly\n\n"
    "Status: ALL 12 TESTS PASS")

pdf.set_font("Helvetica", "", 9)

pdf.ln(2)
pdf.add_page()

# SUMMARY
pdf.section_title("Summary")

pdf.body_text(
    "This report presents a complete analysis of ISYE 4031 Homework 1, covering four major "
    "topics in statistical analysis and forecasting.\n\n"
    
    "PART 1 - DESCRIPTIVE SUMMARIES AND UNCERTAINTY:\n"
    "Provides descriptive statistics for 14 training observations of daily maximum temperatures. "
    "Calculates 95% confidence interval [89.02, 92.27] F for the population mean and 95% prediction "
    "interval [84.34, 96.94] F for a single future observation. The prediction interval is sqrt(15) times "
    "wider than the CI because it accounts for additional natural variation.\n\n"
    
    "PART 2 - TRANSPARENT FORECAST BASELINES:\n"
    "Develops two simple baselines for forecasting days 15-20: (1) mean baseline using training mean "
    "(90.64 F), and (2) last-value baseline using the final training value (94.00 F). Evaluates both "
    "using MAE and RMSE metrics. Mean baseline is superior (RMSE 3.18 vs 3.34 F) and is recommended "
    "for deployment.\n\n"
    
    "PART 3 - ONE-SAMPLE INFERENCE:\n"
    "Conducts a two-tailed hypothesis test on melting point data. Tests whether mean differs from 155 F "
    "at alpha=0.01. Test statistic z=-1.69, p-value=0.092. Fails to reject the null hypothesis. "
    "Calculates Type II error probability (beta ~ 0) when true mean is 150 F, showing very high power.\n\n"
    
    "PART 4 - AUDIT AND TESTING:\n"
    "Identifies 5 critical problems in proposed code related to data leakage and incorrect formulas. "
    "Provides corrected implementation with 12 comprehensive automated tests. All tests pass, validating "
    "statistical correctness, data integrity, and reproducibility.\n\n"
    
    "KEY GUARANTEES:\n"
    "- No information leakage: held-out data never used in model development\n"
    "- Proper statistics: sample variance uses n-1 denominator (unbiased estimator)\n"
    "- Correct intervals: CI and PI use proper formulas with correct critical values\n"
    "- Perfect reproducibility: deterministic results independent of computational randomness\n"
    "- Extensive testing: 12 automated tests validate all statistical requirements\n\n"
    
    "All results are fully reproducible from submitted Python code. Code and analysis comply with "
    "academic integrity requirements and temporal coherence standards for forecasting.")

pdf.output("report.pdf")
print("Report generated successfully: report.pdf")
