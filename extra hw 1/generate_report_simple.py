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
        self.set_margins(11, 12, 11)  # left, top, right margins
        
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 6, "ISYE 4031: Regression and Forecasting", 0, 1, "C")
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 5, "Homework 1 Report", 0, 1, "C")
        self.ln(2)
        
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
        
    def section_title(self, title):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(31, 78, 121)
        self.set_text_color(255, 255, 255)
        self.cell(0, 7, title, 0, 1, "L", True)
        self.set_text_color(0, 0, 0)
        self.ln(1)
        
    def subsection_title(self, title):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(0, 0, 100)
        self.cell(0, 5, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(1)
        
    def body_text(self, text):
        self.set_font("Helvetica", "", 8)
        self.multi_cell(0, 4, text)
        self.ln(0.5)

    # Keep the compact generator compatible with the section helpers below.
    def chapter_title(self, title):
        self.section_title(title)

    def chapter_body(self, text):
        self.body_text(text)


pdf = PDF()
pdf.add_page()

# PART 1
pdf.chapter_title("Part 1: Descriptive Summaries and Uncertainty")

pdf.chapter_body(
    "Unit of Analysis: Individual day\n"
    "Response: Daily maximum temperature (Fahrenheit)\n"
    "Information Cutoff: End of day 14 (14 training observations)\n"
    "Forecast Target: Daily max temperatures for days 15-20\n\n"
    "The estimand for Part 1 is the population mean daily maximum temperature. "
    "The forecast target for Part 2 is the ordered six-day sequence after the cutoff. "
    "All estimates, intervals, and forecasts must be constructed from train only.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "1a. Descriptive Plot", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "The plot shows 20 daily temperatures in order. Blue circles (days 1-14) are training data. "
    "Red squares (days 15-20) are held-out test data. The vertical line marks the training cutoff. "
    "When forecasts are issued at the end of day 14, only the 14 training values are available. "
    "The held-out points are shown for later evaluation, not for estimating the baselines or intervals.")

if os.path.exists("part1a_plot.png"):
    try:
        pdf.image("part1a_plot.png", x=35, w=140)
        pdf.ln(2)
    except:
        pass

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "1b. Descriptive Statistics (Training Data Only)", 0, 1)
pdf.set_font("Helvetica", "", 9)

stats_text = (
    "Mean: 90.6429 F\n"
    "Median: 90.5000 F\n"
    "Range: 9.0000 F\n"
    "Sample Variance: 7.9396 F-squared (denominator = n-1 = 13)\n"
    "Sample Std Dev: 2.8177 F\n"
    "Interquartile Range: 4.5000 F\n\n"
    "The mean and median are close (90.6429 F versus 90.5000 F), so the training values do not show "
    "strong skew. The standard deviation describes typical spread around the mean, while the range "
    "and IQR summarize the observed extremes and central half without using the held-out period.")
pdf.multi_cell(0, 3.5, stats_text)

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "1c. Confidence Interval for Population Mean", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "95% CI Formula: x-bar +/- t(alpha/2, n-1) * (s / sqrt(n))\n"
    "x-bar = 90.6429, s = 2.8177, n = 14\n"
    "SE = 2.8177 / sqrt(14) = 0.7531\n"
    "t(0.025, 13) = 2.1604\n"
    "Margin of error = 2.1604 * 0.7531 = 1.6269\n"
    "95% CI: [89.0160, 92.2698]\n\n"
    "Interpretation: If we repeatedly sampled 14 observations and constructed "
    "95% confidence intervals, approximately 95% would contain the true population mean. "
    "This statement describes the long-run procedure; it does not assign a 95% probability "
    "to the already-computed fixed interval.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "1d. Prediction Interval for Single Observation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "95% PI Formula: x-bar +/- t(alpha/2, n-1) * s * sqrt(1 + 1/n)\n"
    "sqrt(1 + 1/14) = 1.0351\n"
    "Margin of error = 2.1604 * 2.8177 * 1.0351 = 6.3010\n"
    "95% PI: [84.3419, 96.9438]\n\n"
    "Why Wider? PI accounts for both: (1) uncertainty about mean, and (2) natural "
    "variation of individual observations. The factor sqrt(1 + 1/n) captures this extra variability. "
    "Thus, the CI estimates where the population mean is likely to be, whereas the PI predicts where "
    "one future temperature may fall.")

pdf.ln(2)

pdf.add_page()

# PART 2
pdf.chapter_title("Part 2: Transparent Forecast Baselines")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "2a. Baseline Forecasts", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "Mean Baseline: Using training mean (90.6429 F) for all 6 forecasts\n"
    "Forecasts for days 15-20: 90.64, 90.64, 90.64, 90.64, 90.64, 90.64\n\n"
    "Last-Value Baseline: Using final training value (94 F) for all forecasts\n"
    "Forecasts for days 15-20: 94.00, 94.00, 94.00, 94.00, 94.00, 94.00\n\n"
    "Why fixed? Both baselines use only training data (days 1-14). They produce "
    "predetermined forecasts independent of what actually occurs in the held-out period. "
    "The mean baseline represents a stable level, while the last-value baseline represents a "
    "persistence rule. Neither method is allowed to update after day 14 in this fixed evaluation.")

if os.path.exists("part2a_plot.png"):
    try:
        pdf.image("part2a_plot.png", x=35, w=140)
        pdf.ln(2)
    except:
        pass

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "2b. Forecast Evaluation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "Mean Baseline:\n"
    "  Forecast errors (forecast - actual): -5.3571, -4.3571, -2.3571, -0.3571, 0.6429, 2.6429 F\n"
    "  MAE: 2.6190 F\n"
    "  RMSE: 3.1824 F\n\n"
    "Last-Value Baseline:\n"
    "  Forecast errors (forecast - actual): -2, -1, 1, 3, 4, 6 F\n"
    "  MAE: 2.8333 F\n"
    "  RMSE: 3.3417 F\n\n"
    "Winner: Mean baseline is better on both metrics. MAE weights all absolute errors equally, "
    "whereas RMSE penalizes larger errors more heavily; the same winner under both metrics is a "
    "consistent result for this small held-out sample.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "2c. Independence of Errors", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "The 6 errors are NOT independent because: (1) Time series temperatures exhibit "
    "autocorrelation - warm days tend to follow warm days. (2) Seasonal or systematic "
    "patterns create dependence. (3) Standard i.i.d. assumption is violated in time series. "
    "Therefore, the six errors are six consecutive outcomes from one forecast origin, not six "
    "independent repetitions of the entire training-and-testing experiment. The reported MAE and "
    "RMSE are still valid descriptive scores for this holdout, but their uncertainty should not be "
    "treated as if it came from six independent replications.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "2d. Recommended Baseline", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "Choice: Mean Baseline\n\n"
    "Reasons:\n"
    "* Simplicity: Simple summary statistic from training data\n"
    "* Performance: Lower RMSE (3.1824 vs 3.3417 F)\n"
    "* Reproducibility: Perfectly reproducible, no randomness\n"
    "* Decision rule: Under squared-error loss, the population mean is the optimal constant target; "
    "the training mean is its natural sample estimate.\n\n"
    "The mean baseline is the required benchmark for a future extension. The holdout is small, so "
    "this choice should be reconsidered with additional chronological validation before deployment.")

pdf.ln(2)

pdf.add_page()

# PART 3
pdf.chapter_title("Part 3: One-Sample Inference")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "3a. Hypothesis Test", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 3.5,
    "H0: mu = 155 F (null hypothesis)\n"
    "Ha: mu != 155 F (two-tailed alternative)\n"
    "Significance level: alpha = 0.01\n\n"
    "Data: n=10, x-bar=154.2 F, sigma=1.5 F (known)\n\n"
    "Test statistic (z-test): z = (154.2 - 155) / (1.5 / sqrt(10)) = -1.6865\n\n"
    "Critical value: z(0.005) = 2.5758\n\n"
    "Decision: |z| = 1.6865 < 2.5758, so FAIL TO REJECT H0\n\n"
    "Conclusion: At alpha=0.01, insufficient evidence that mean differs from 155 F. "
    "Failing to reject is not proof that the mean equals 155 F; it means this sample does not provide "
    "enough evidence against that null at the specified significance level.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "3b. Two-Sided P-value", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "p-value = 2 * P(Z > 1.6865) = 0.0917\n\n"
    "Interpretation: The p-value 0.0917 is the probability of observing a sample mean "
    "at least as extreme as 154.2 F (in either direction) when H0 is true. It is NOT "
    "the probability that H0 is true.\n\n"
    "Since 0.0917 > 0.01, we fail to reject H0.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "3c. Type II Error Probability", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Assuming true mean is mu = 150 F\n\n"
    "Acceptance Region: [153.7782, 156.2218] F\n\n"
    "Beta = P(153.7782 <= x-bar <= 156.2218 | mu=150) ~ 0.00000\n\n"
    "Interpretation: When the true mean is 5 F away from H0, the probability of Type II "
    "error is essentially 0. The effect size is very large at this sample size.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "3d. Python Verification", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "All calculations were independently evaluated in Python with scipy.stats:\n"
    "  z_stat = -1.686548 [verified]\n"
    "  z_critical = 2.575829 [verified]\n"
    "  p_value = 0.091690 [verified]\n"
    "  beta = 0.000000 [verified]\n\n"
    "The Python values agree with the hand calculations after rounding. The z procedure is valid "
    "because the population standard deviation is given as known and the population is assumed normal.")

pdf.ln(2)

pdf.add_page()

# PART 4
pdf.chapter_title("Part 4: Agent Audit and Automated Tests")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "4a. Problems in Proposed Code", 0, 1)
pdf.set_font("Helvetica", "", 9)

problems_text = (
    "Problem 1: Using x.mean() instead of train.mean()\n"
    "  Consequence: Computes the center from all 20 temperatures instead of just 14 training values. "
    "This leaks future information and changes the estimand from the legal pre-cutoff summary.\n\n"
    
    "Problem 2: Computing intervals with future data\n"
    "  Consequence: Intervals include future observations, so they cannot represent uncertainty known "
    "at the forecast origin and may give a misleading impression of precision.\n\n"
    
    "Problem 3: Prediction interval equal to confidence interval\n"
    "  Consequence: Ignores extra variability of individual observations. PI should be wider "
    "by factor sqrt(1 + 1/n), but this code makes them equal and understates predictive uncertainty.\n\n"
    
    "Problem 4: Using x[-1] instead of train[-1]\n"
    "  Consequence: Accesses the final held-out value (88) instead of last training value (94), "
    "using future information and invalidating the forecast comparison.\n\n"
    
    "Problem 5: No reproducibility guarantees\n"
    "  Consequence: The code does not state its data cutoff, denominator, assumptions, or deterministic "
    "behavior, making the result harder to audit and reproduce."
)
pdf.multi_cell(0, 3, problems_text)

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "4b. Corrected Implementation", 0, 1)
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 4,
    "Key Improvements:\n"
    "- Uses ONLY train data for all statistics\n"
    "- Correct CI formula: x-bar +/- t * (s / sqrt(n))\n"
    "- Correct PI formula: x-bar +/- t * s * sqrt(1 + 1/n)\n"
    "- Separates mean and last-value baselines clearly\n"
    "- Includes comprehensive automated tests\n\n"
    "Implementation in analysis.py and test_analysis.py. The two baselines remain separate so that "
    "a later model can be compared against transparent benchmarks without changing their definitions.")

pdf.set_font("Helvetica", "B", 9)
pdf.set_x(pdf.l_margin)
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
    "- Baseline arithmetic: Forecast lengths, constancy, errors, and data integrity\n\n"
    "Status: ALL 12 TESTS PASS. These checks target the four required properties and also verify the "
    "reported hypothesis-test and forecast calculations.")
pdf.multi_cell(0, 3, tests_text)

# Add final page
pdf.add_page()
pdf.set_font("Helvetica", "B", 11)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(31, 78, 121)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 7, "Summary", 0, 1, "L", True)
pdf.set_text_color(0, 0, 0)
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
    "Interpretive limit: The temperature holdout contains only six consecutive days, so the forecast "
    "scores support a transparent benchmark comparison rather than a broad claim about long-run "
    "performance. Likewise, the Type II error result is specific to the stated effect of 5 F, known "
    "sigma, alpha, and sample size.\n\n"
    
    "All results are reproducible from the submitted Python code. All analyses follow the "
    "requirement to use only training data for estimation, and all forecasts are based on "
    "information available at the end of day 14.")
    
pdf.multi_cell(0, 4, summary)

pdf.output("report.pdf")
print("Report generated successfully: report.pdf")
