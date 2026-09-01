"""
Generate simple PDF report for ISYE 4031 Homework 1
Uses only ASCII characters to avoid encoding issues
"""

from fpdf import FPDF
import os


# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore')


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "ISYE 4031: Regression and Forecasting", 0, 1, "C")
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 6, "Homework 1 Report", 0, 1, "C")
        self.ln(3)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
        
    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 7, title, 0, 1, "L", True)
        self.ln(2)
        
    def chapter_body(self, text):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4, text)
        self.ln(1)


pdf = PDF()
pdf.add_page()

# PART 1
pdf.chapter_title("Part 1: Descriptive Summaries and Uncertainty")

pdf.chapter_body(
    "Unit of Analysis: Individual day\n"
    "Response: Daily maximum temperature (Fahrenheit)\n"
    "Information Cutoff: End of day 14 (14 training observations)\n"
    "Forecast Target: Daily max temperatures for days 15-20")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "1a. Descriptive Plot", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "The plot shows 20 daily temperatures in order. Blue circles (days 1-14) are training data. "
    "Red squares (days 15-20) are held-out test data. The vertical line marks the training cutoff. "
    "When forecasts are issued at the end of day 14, only the 14 training values are available.")

if os.path.exists("part1a_plot.png"):
    try:
        pdf.image("part1a_plot.png", x=10, w=180)
        pdf.ln(2)
    except:
        pass

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "1b. Descriptive Statistics (Training Data Only)", 0, 1)
pdf.set_font("Helvetica", "", 9)

stats_text = (
    "Mean: 90.6429 F\n"
    "Median: 90.5000 F\n"
    "Range: 9.0000 F\n"
    "Sample Variance: 7.9396 F-squared (denominator = n-1 = 13)\n"
    "Sample Std Dev: 2.8177 F\n"
    "Interquartile Range: 4.5000 F")
pdf.multi_cell(0, 4, stats_text)

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "1c. Confidence Interval for Population Mean", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "95% CI Formula: x-bar +/- t(alpha/2, n-1) * (s / sqrt(n))\n"
    "x-bar = 90.6429, s = 2.8177, n = 14\n"
    "SE = 2.8177 / sqrt(14) = 0.7531\n"
    "t(0.025, 13) = 2.1604\n"
    "Margin of error = 2.1604 * 0.7531 = 1.6269\n"
    "95% CI: [89.0160, 92.2698]\n\n"
    "Interpretation: If we repeatedly sampled 14 observations and constructed "
    "95% confidence intervals, approximately 95% would contain the true population mean.")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "1d. Prediction Interval for Single Observation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "95% PI Formula: x-bar +/- t(alpha/2, n-1) * s * sqrt(1 + 1/n)\n"
    "sqrt(1 + 1/14) = 1.0351\n"
    "Margin of error = 2.1604 * 2.8177 * 1.0351 = 6.3010\n"
    "95% PI: [84.3419, 96.9438]\n\n"
    "Why Wider? PI accounts for both: (1) uncertainty about mean, and (2) natural "
    "variation of individual observations. The factor sqrt(1 + 1/n) captures this extra variability.")

pdf.ln(2)

pdf.add_page()

# PART 2
pdf.chapter_title("Part 2: Transparent Forecast Baselines")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "2a. Baseline Forecasts", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Mean Baseline: Using training mean (90.6429 F) for all 6 forecasts\n"
    "Forecasts for days 15-20: 90.64, 90.64, 90.64, 90.64, 90.64, 90.64\n\n"
    "Last-Value Baseline: Using final training value (94 F) for all forecasts\n"
    "Forecasts for days 15-20: 94.00, 94.00, 94.00, 94.00, 94.00, 94.00\n\n"
    "Why fixed? Both baselines use only training data (days 1-14). They produce "
    "predetermined forecasts independent of what actually occurs in the held-out period.")

if os.path.exists("part2a_plot.png"):
    try:
        pdf.image("part2a_plot.png", x=10, w=180)
        pdf.ln(2)
    except:
        pass

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "2b. Forecast Evaluation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Mean Baseline:\n"
    "  MAE: 2.6190 F\n"
    "  RMSE: 3.1824 F\n\n"
    "Last-Value Baseline:\n"
    "  MAE: 2.8333 F\n"
    "  RMSE: 3.3417 F\n\n"
    "Winner: Mean baseline is better on both metrics")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "2c. Independence of Errors", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "The 6 errors are NOT independent because: (1) Time series temperatures exhibit "
    "autocorrelation - warm days tend to follow warm days. (2) Seasonal or systematic "
    "patterns create dependence. (3) Standard i.i.d. assumption is violated in time series.")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "2d. Recommended Baseline", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Choice: Mean Baseline\n\n"
    "Reasons:\n"
    "* Simplicity: Simple summary statistic from training data\n"
    "* Performance: Lower RMSE (3.1824 vs 3.3417 F)\n"
    "* Reproducibility: Perfectly reproducible, no randomness\n\n"
    "The mean baseline is more appropriate for deployment.")

pdf.ln(2)

pdf.add_page()

# PART 3
pdf.chapter_title("Part 3: One-Sample Inference")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "3a. Hypothesis Test", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "H0: mu = 155 F (null hypothesis)\n"
    "Ha: mu != 155 F (two-tailed alternative)\n"
    "Significance level: alpha = 0.01\n\n"
    "Data: n=10, x-bar=154.2 F, sigma=1.5 F (known)\n\n"
    "Test statistic (z-test): z = (154.2 - 155) / (1.5 / sqrt(10)) = -1.6865\n\n"
    "Critical value: z(0.005) = 2.5758\n\n"
    "Decision: |z| = 1.6865 < 2.5758, so FAIL TO REJECT H0\n\n"
    "Conclusion: At alpha=0.01, insufficient evidence that mean differs from 155 F")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "3b. Two-Sided P-value", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "p-value = 2 * P(Z > 1.6865) = 0.0917\n\n"
    "Interpretation: The p-value 0.0917 is the probability of observing a sample mean "
    "at least as extreme as 154.2 F (in either direction) when H0 is true. It is NOT "
    "the probability that H0 is true.\n\n"
    "Since 0.0917 > 0.01, we fail to reject H0.")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "3c. Type II Error Probability", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Assuming true mean is mu = 150 F\n\n"
    "Acceptance Region: 153.78 to 156.22\n\n"
    "Beta = P(fail to reject H0 | true mean is 150) ~ 0.00000\n\n"
    "Interpretation: When the true mean is 5 F away from H0, the probability of Type II "
    "error is essentially 0. The effect size is very large at this sample size.")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "3d. Python Verification", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "All calculations verified with scipy.stats:\n"
    "  z_stat = -1.686548 [verified]\n"
    "  z_critical = 2.575829 [verified]\n"
    "  p_value = 0.091690 [verified]\n"
    "  beta = 0.000000 [verified]")

pdf.ln(2)

pdf.add_page()

# PART 4
pdf.chapter_title("Part 4: Agent Audit and Automated Tests")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "4a. Problems in Proposed Code", 0, 1)
pdf.set_font("Helvetica", "", 9)

problems_text = (
    "Problem 1: Using x.mean() instead of train.mean()\n"
    "  Consequence: Computes mean from all 20 temperatures instead of just 14 training values. "
    "Uses future information, violating temporal integrity.\n\n"
    
    "Problem 2: Computing intervals with future data\n"
    "  Consequence: Intervals include future observations, producing artificially narrow "
    "uncertainty estimates.\n\n"
    
    "Problem 3: Prediction interval equal to confidence interval\n"
    "  Consequence: Ignores extra variability of individual observations. PI should be wider "
    "by factor of sqrt(1 + 1/n), but this code makes them equal.\n\n"
    
    "Problem 4: Using x[-1] instead of train[-1]\n"
    "  Consequence: Accesses the final held-out value (88) instead of last training value (94), "
    "using future information for forecasts.\n\n"
    
    "Problem 5: No reproducibility guarantees\n"
    "  Consequence: Insufficient documentation of reproducibility despite no randomness. "
    "Future maintainability issues."
)
pdf.multi_cell(0, 3, problems_text)

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "4b. Corrected Implementation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Key Improvements:\n"
    "- Uses ONLY train data for all statistics\n"
    "- Correct CI formula: x-bar +/- t * (s / sqrt(n))\n"
    "- Correct PI formula: x-bar +/- t * s * sqrt(1 + 1/n)\n"
    "- Separates mean and last-value baselines clearly\n"
    "- Includes comprehensive automated tests\n\n"
    "Implementation in analysis.py and test_analysis.py")

pdf.set_font("Helvetica", "B", 9)
pdf.cell(0, 5, "4c. Automated Tests", 0, 1)
pdf.set_font("Helvetica", "", 9)

tests_text = (
    "- Held-out values invariant: Changing test data does not affect training stats\n"
    "- Sample variance denominator: Verifies n-1 denominator used (not n)\n"
    "- PI wider than CI: Confirms prediction interval is larger\n"
    "- CI/PI width ratio: Verifies PI = sqrt(n+1) * CI factor\n"
    "- Reproducibility: 10 runs produce identical results\n"
    "- Hypothesis test: Verifies Part 3 calculations\n"
    "- Type II error: Confirms beta calculation\n"
    "- Data integrity: Training and test sets properly separated\n\n"
    "Status: ALL 12 TESTS PASS")
pdf.multi_cell(0, 3, tests_text)

# Add final page
pdf.add_page()
pdf.set_font("Helvetica", "B", 11)
pdf.cell(0, 6, "Summary", 0, 1, "L")
pdf.set_font("Helvetica", "", 9)

summary = (
    "This report presents a complete analysis of ISYE 4031 Homework 1.\n\n"
    
    "Part 1 provides descriptive statistics and confidence/prediction intervals "
    "based on 14 training observations of daily maximum temperatures.\n\n"
    
    "Part 2 develops two transparent forecast baselines: (1) mean baseline using "
    "the training mean, and (2) last-value baseline using the final training value. "
    "The mean baseline performs better and is recommended.\n\n"
    
    "Part 3 conducts a one-sample hypothesis test on melting point data, testing whether "
    "the mean differs from 155 F at alpha=0.01. The test fails to reject the null hypothesis "
    "with p-value=0.0917.\n\n"
    
    "Part 4 audits proposed code and identifies 5 major statistical problems related to data "
    "leakage and incorrect interval formulas. A corrected implementation with 12 passing "
    "automated tests is provided.\n\n"
    
    "All results are reproducible from the submitted Python code. All analyses follow the "
    "requirement to use only training data for estimation, and all forecasts are based on "
    "information available at the end of day 14.")
    
pdf.multi_cell(0, 4, summary)

pdf.output("report.pdf")
print("Report generated successfully: report.pdf")
