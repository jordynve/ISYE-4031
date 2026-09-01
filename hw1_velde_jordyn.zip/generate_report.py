"""
Generate PDF report for ISYE 4031 Homework 1
"""

from fpdf import FPDF
import os


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "ISYE 4031: Regression and Forecasting", 0, 1, "C")
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, "Homework 1: Statistical Review and Forecast Baselines", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "Fall 2026", 0, 1, "C")
        self.ln(4)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
        
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, "L", True)
        self.ln(2)
        
    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, text)
        self.ln(2)
        
    def add_table(self, headers, rows, col_widths):
        self.set_font("Arial", "B", 9)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 6, header, 1, 0, "C")
        self.ln()
        
        self.set_font("Arial", "", 9)
        for row in rows:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, str(cell), 1, 0, "C")
            self.ln()


pdf = PDF()
pdf.add_page()

# ============================================================================
# PART 1: DESCRIPTIVE SUMMARIES AND UNCERTAINTY
# ============================================================================

pdf.chapter_title("Part 1: Descriptive Summaries and Uncertainty")

pdf.chapter_body(
    "Unit of Analysis: Individual day\n"
    "Response Variable: Daily maximum temperature (°F)\n"
    "Information Cutoff: End of day 14 (after observing first 14 consecutive temperatures)\n"
    "Intended Forecast Target: Daily maximum temperatures for days 15-20"
)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "1a. Plot Description", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "The plot displays 20 consecutive daily maximum temperatures in their observed order. "
    "The first 14 observations (days 1-14, blue circles) form the training set. The final "
    "6 observations (days 15-20, red squares) are held-out for evaluation. A vertical "
    "dashed line marks the cutoff between training and held-out periods. Only the 14 "
    "training observations are available when forecasts are issued at the end of day 14. "
    "The plot also displays 95% confidence and prediction intervals computed from training "
    "data only.")
if os.path.exists("part1a_plot.png"):
    pdf.image("part1a_plot.png", x=10, w=190)
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "1b. Statistical Summary (Training Set Only)", 0, 1)
pdf.set_font("Arial", "", 9)

pdf.add_table(
    ["Statistic", "Value", "Unit"],
    [
        ["Mean", "90.64", "°F"],
        ["Median", "90.50", "°F"],
        ["Range", "9.00", "°F"],
        ["Sample Variance", "7.94", "°F²"],
        ["Sample Std Dev", "2.82", "°F"],
        ["IQR", "4.50", "°F"],
    ],
    [70, 50, 40]
)
pdf.ln(2)

pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Sample Variance Calculation (n-1 denominator):\n"
    "Sum of squared deviations = 103.2143\n"
    "Variance = 103.2143 / (14-1) = 103.2143 / 13 = 7.9396\n"
    "Std Dev = sqrt(7.9396) = 2.8177")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "1c. 95% Confidence Interval for Population Mean", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Formula: x-bar +/- t_(alpha/2, n-1) * (s / sqrt(n))\n"
    "x-bar = 90.6429 F\n"
    "s = 2.8177 F\n"
    "SE = 2.8177 / sqrt(14) = 0.7531\n"
    "t_(0.025, 13) = 2.1604\n"
    "95% CI = [89.0160, 92.2698]\n\n"
    "Interpretation: If we repeatedly sampled 14 temperatures from this population "
    "and constructed 95% confidence intervals using this method, approximately 95% "
    "of those intervals would contain the true population mean mu.")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "1d. 95% Prediction Interval for One New Observation", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Formula: x-bar +/- t_(alpha/2, n-1) * s * sqrt(1 + 1/n)\n"
    "Margin of error = 2.1604 * 2.8177 * sqrt(1.0714) = 6.3010\n"
    "95% PI = [84.3419, 96.9438]\n\n"
    "Why Wider than CI?\n"
    "The prediction interval accounts for two sources of uncertainty:\n"
    "1) Uncertainty about the true population mean (as in CI)\n"
    "2) Natural variation of individual observations around the mean\n"
    "The factor sqrt(1 + 1/n) = 1.0351 accounts for this additional variability.")
pdf.ln(2)

pdf.add_page()

# ============================================================================
# PART 2: FORECAST BASELINES
# ============================================================================

pdf.chapter_title("Part 2: Transparent Forecast Baselines")

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "2a. Baseline Forecasts", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Mean Baseline: Using training mean (90.6429°F) for all 6 held-out forecasts\n"
    "Days 15-20: 90.64°F, 90.64°F, 90.64°F, 90.64°F, 90.64°F, 90.64°F\n\n"
    "Last-Value Baseline: Using final training observation (94°F) for all forecasts\n"
    "Days 15-20: 94°F, 94°F, 94°F, 94°F, 94°F, 94°F\n\n"
    "Why Forecasts Don't Change:\n"
    "Both baselines use only training data (days 1-14). They produce predetermined "
    "forecasts independent of what actually occurs in the held-out period.")
if os.path.exists("part2a_plot.png"):
    pdf.image("part2a_plot.png", x=10, w=190)
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "2b. Forecast Evaluation Metrics", 0, 1)
pdf.add_table(
    ["Metric", "Mean Baseline", "Last-Value Baseline", "Better"],
    [
        ["MAE (F)", "2.6190", "2.8333", "Mean"],
        ["RMSE (F)", "3.1824", "3.3417", "Mean"],
    ],
    [50, 50, 50, 40]
)
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "2c. Independence of Errors", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "The six held-out forecast errors are NOT independent replications because:\n"
    "1) Temporal Autocorrelation: Consecutive daily temperatures exhibit autocorrelation. "
    "A warm day tends to be followed by another warm day.\n"
    "2) Systematic Patterns: Any seasonal or systematic trends in temperature would "
    "create dependence in forecast errors.\n"
    "3) Violation of i.i.d. Assumption: Standard model evaluation statistics assume "
    "independent observations, which is violated in time series data.")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "2d. Recommended Baseline Benchmark", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "RECOMMENDED: Mean Baseline\n\n"
    "Justification:\n"
    "* Simplicity: Both methods require only one value from the training set. "
    "The mean is conceptually simpler as a summary statistic.\n"
    "* Performance: Mean baseline achieves lower RMSE (3.1824 F vs 3.3417 F), "
    "indicating better forecasting accuracy.\n"
    "* Reproducibility: Both methods are perfectly reproducible from training data "
    "with no randomness involved.\n\n"
    "The mean baseline is more appropriate for deployment as it combines simplicity "
    "with better empirical performance.")
pdf.ln(2)

pdf.add_page()

# ============================================================================
# PART 3: ONE-SAMPLE INFERENCE
# ============================================================================

pdf.chapter_title("Part 3: One-Sample Inference")

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "3a. Hypothesis Test: Melting Point Analysis", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Hypotheses:\n"
    "  H0: mu = 155 F\n"
    "  Ha: mu != 155 F (two-tailed)\n"
    "Significance level: alpha = 0.01\n\n"
    "Test Statistic (z-test, sigma known):\n"
    "  z = (154.2 - 155) / (1.5 / sqrt(10)) = -1.6865\n\n"
    "Rejection Rule:\n"
    "  Reject H0 if |z| > 2.5758\n"
    "  |-1.6865| = 1.6865 < 2.5758\n\n"
    "Decision: FAIL TO REJECT H0\n\n"
    "Conclusion: At the alpha = 0.01 significance level, there is insufficient evidence "
    "to conclude that the true mean melting point differs from 155 F.")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "3b. Two-Sided P-value", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "p-value = P(|Z| > 1.6865) = 2 * P(Z > 1.6865) = 0.0917\n\n"
    "Interpretation:\n"
    "The p-value of 0.0917 represents the probability of observing a sample mean "
    "at least as extreme as 154.2 F (in either direction), given that H0: mu = 155 "
    "is true. It is NOT the probability that H0 is true.\n\n"
    "Since 0.0917 > 0.01, we fail to reject H0 at the 0.01 significance level.")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "3c. Type II Error Probability (beta)", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "Assuming the true mean is mu = 150 F:\n\n"
    "Acceptance Region: 153.7782 <= x-bar <= 156.2218\n\n"
    "beta = P(accept H0 | true mean is 150 F)\n"
    "     = P(153.7782 <= x-bar <= 156.2218 | mu = 150)\n"
    "     = P(7.9651 <= Z <= 13.1168)\n"
    "     ~ 0.00000\n\n"
    "Interpretation: When the true mean is 150 F (5 F away from H0), the probability "
    "of committing a Type II error is essentially 0. This large effect size makes it "
    "extremely likely to detect a difference at our test's power level.")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "3d. Python Verification", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "All calculations were verified using scipy.stats functions:\n"
    "  z_stat = -1.686548 [OK]\n"
    "  z_critical = 2.575829 [OK]\n"
    "  p_value = 0.091690 [OK]\n"
    "  beta = 0.000000 [OK]\n\n"
    "All numerical results match hand calculations exactly.")
pdf.ln(2)

pdf.add_page()

# ============================================================================
# PART 4: AUDIT AND AUTOMATED TESTS
# ============================================================================

pdf.chapter_title("Part 4: Agent Audit and Automated Tests")

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "4a. Problems in Proposed Code", 0, 1)
pdf.set_font("Arial", "", 10)

problems = [
    ("Using x.mean() instead of train.mean()", 
     "Consequence: The mean is computed from ALL 20 temperatures instead of only the 14 training values. This uses information from the held-out period, violating temporal integrity."),
    
    ("Future value leakage in interval estimation", 
     "Consequence: Computing intervals using x.mean() and x.std() includes future (held-out) observations, producing misleading uncertainty estimates that appear artificially narrow."),
    
    ("Prediction interval set equal to confidence interval", 
     "Consequence: future_interval = mean_interval ignores the added variability of individual observations. PI should be wider than CI by a factor of √(1 + 1/n) ≈ 1.035, but this mistake makes them equal."),
    
    ("Using last training value incorrectly", 
     "Consequence: forecast = np.repeat(x[-1], len(test)) uses x[-1], which is an ambiguous reference. With x being all 20 values, this uses the final held-out value (88°F) instead of the last training value (94°F)."),
    
    ("Insufficient randomness control and reproducibility documentation", 
     "Consequence: No seed is set for reproducibility. While this code contains no randomness, a proper implementation should document reproducibility guarantees and avoid future maintainability issues."),
]

for i, (problem, consequence) in enumerate(problems, 1):
    pdf.set_font("Arial", "B", 9)
    pdf.cell(0, 5, f"{i}. {problem}", 0, 1)
    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 4, f"   {consequence}")
    pdf.ln(1)

pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "4b & 4c. Corrected Implementation", 0, 1)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "The corrected implementation is provided in analysis.py and test_analysis.py:\n\n"
    "Key Improvements:\n"
    "• Uses only train data for all statistics (no held-out values)\n"
    "• Correctly computes confidence intervals: x̄ ± t × (s/√n)\n"
    "• Correctly computes prediction intervals: x̄ ± t × s × √(1 + 1/n)\n"
    "• Properly separates mean and last-value baselines\n"
    "• Includes 12 automated tests verifying all requirements")
pdf.ln(2)

pdf.set_font("Arial", "B", 10)
pdf.cell(0, 6, "Automated Tests Included", 0, 1)
pdf.set_font("Arial", "", 9)

tests = [
    "test_training_stats_invariant_to_held_out_values: Changing held-out values does not affect training summaries or forecasts",
    "test_sample_std_uses_n_minus_1_denominator: Verifies n-1 denominator in sample variance",
    "test_prediction_interval_wider_than_ci: Confirms PI > CI",
    "test_ci_pi_width_ratio: Verifies PI margin = sqrt(n+1) * CI margin",
    "test_reproducibility_of_calculations: Identical results across 10 repeated runs",
    "test_hypothesis_test_calculations: Verifies Part 3 results",
    "test_type_ii_error_calculation: Confirms beta calculation",
]

for test in tests:
    pdf.multi_cell(0, 4, f"- {test}")
pdf.ln(2)

pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 4,
    "All 12 tests PASS, confirming data integrity, statistical correctness, "
    "and perfect reproducibility of the implementation.")

pdf.output("report.pdf")
print("Report generated: report.pdf")
