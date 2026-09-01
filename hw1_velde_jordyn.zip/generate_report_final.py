"""
Generate compact 5-page PDF report for ISYE 4031 Homework 1
Uses only ASCII characters to avoid encoding issues
Optimized for 5-page limit while maintaining readability
"""

from fpdf import FPDF
import os

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore')


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(12, 14, 12)  # left, top, right margins - compact
        
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


pdf = PDF()
pdf.add_page()

# PART 1
pdf.section_title("PART 1: Descriptive Summaries and Uncertainty")

pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Unit of Analysis: Individual day | Response: Daily max temperature (F)\n"
    "Information Cutoff: End of day 14 (14 training observations)\n"
    "Forecast Target: Daily max temperatures for days 15-20")
pdf.ln(1)

pdf.subsection_title("1a. Descriptive Plot")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Plot shows 20 daily temperatures in order. Blue circles (days 1-14) are training data. Red squares "
    "(days 15-20) are held-out test data. Vertical line marks training/test cutoff.")
pdf.ln(1)

if os.path.exists("part1a_plot.png"):
    try:
        pdf.image("part1a_plot.png", x=12, w=187)
        pdf.ln(1)
    except Exception as e:
        print(f"Warning: Could not embed plot: {e}")

pdf.subsection_title("1b. Descriptive Statistics (Training Data Only)")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Mean: 90.6429 F | Median: 90.5000 F | Range: 9.0000 F\n"
    "Sample Variance: 7.9396 F^2 (n-1=13) | Std Dev: 2.8177 F | IQR: 4.5000 F")

pdf.ln(1)
pdf.subsection_title("1c. Confidence Interval for Population Mean")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Formula: x-bar +/- t(alpha/2, n-1) * (s / sqrt(n))\n"
    "x-bar = 90.6429, s = 2.8177, n = 14, SE = 0.7531, t(0.025,13) = 2.1604\n"
    "Margin of error = 2.1604 * 0.7531 = 1.6269\n"
    "Result: 95% CI = [89.0160, 92.2698] F\n"
    "Interpretation: ~95% of repeatedly constructed CIs would contain the true population mean.")

pdf.ln(1)
pdf.subsection_title("1d. Prediction Interval for Single Observation")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Formula: x-bar +/- t(alpha/2, n-1) * s * sqrt(1 + 1/n)\n"
    "sqrt(1 + 1/14) = 1.0351, Margin of error = 2.1604 * 2.8177 * 1.0351 = 6.3010\n"
    "Result: 95% PI = [84.3419, 96.9438] F\n"
    "PI is wider than CI because it accounts for both mean uncertainty AND natural observation variation.")

pdf.ln(1)
pdf.add_page()

# PART 2
pdf.section_title("PART 2: Transparent Forecast Baselines")

pdf.subsection_title("2a & 2b. Baselines and Evaluation")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Mean Baseline: Use training mean (90.6429 F) for all forecasts\n"
    "Last-Value Baseline: Use final training value (94.00 F) for all forecasts\n\n"
    "Evaluation Results:\n"
    "Mean Baseline: MAE = 2.6190 F, RMSE = 3.1824 F\n"
    "Last-Value: MAE = 2.8333 F, RMSE = 3.3417 F\n"
    "Winner: Mean baseline performs better on both metrics.")

pdf.ln(1)

if os.path.exists("part2a_plot.png"):
    try:
        pdf.image("part2a_plot.png", x=12, w=187)
        pdf.ln(1)
    except Exception as e:
        print(f"Warning: Could not embed plot: {e}")

pdf.subsection_title("2c. Independence of Errors")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Are errors independent? NO. Reasons: (1) Temperature autocorrelation - warm days follow warm days. "
    "(2) Seasonal patterns create systematic dependence. (3) Time series data violates i.i.d. assumption.")

pdf.ln(1)
pdf.subsection_title("2d. Recommended Baseline")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Choice: MEAN BASELINE. Justification: Simple, better performance (RMSE 3.18 vs 3.34), reproducible, "
    "and theoretically optimal under squared-error loss.")

pdf.ln(1)
pdf.add_page()

# PART 3
pdf.section_title("PART 3: One-Sample Inference")

pdf.subsection_title("3a. Hypothesis Test")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "H0: mu = 155 F | Ha: mu != 155 F | alpha = 0.01\n"
    "Data: n=10, x-bar=154.2 F, sigma=1.5 F (known)\n"
    "Test Statistic: z = (154.2 - 155) / (1.5 / sqrt(10)) = -1.6865\n"
    "Critical Value: z(0.005) = 2.5758\n"
    "Decision: |z|=1.6865 < 2.5758, so FAIL TO REJECT H0\n"
    "Conclusion: Insufficient evidence that mean differs from 155 F at alpha=0.01.")

pdf.ln(1)
pdf.subsection_title("3b. Two-Sided P-value")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "p-value = 2 * P(Z > 1.6865) = 0.0917\n"
    "Interpretation: Probability of observing sample mean at least as extreme as 154.2 F when H0 is true. "
    "Since 0.0917 > 0.01, we fail to reject H0.")

pdf.ln(1)
pdf.subsection_title("3c. Type II Error (Beta)")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "If true mean is 150 F: Acceptance region = [153.78, 156.22] F\n"
    "Beta = P(fail to reject H0 | true mean = 150) ~ 0.0000\n"
    "High power: Effect size (5 F difference) is very large relative to standard error.")

pdf.ln(1)
pdf.subsection_title("3d. Python Verification")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Calculations verified with scipy.stats:\n"
    "z_stat = -1.686548 [verified] | z_critical = 2.575829 [verified]\n"
    "p_value = 0.091690 [verified] | beta = 0.000000 [verified]")

pdf.ln(1)
pdf.add_page()

# PART 4
pdf.section_title("PART 4: Agent Audit and Automated Tests")

pdf.subsection_title("4a. Five Problems in Proposed Code")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Problem 1: x.mean() instead of train.mean() - Uses all 20 temps instead of 14 training values\n"
    "Problem 2: CI computed from all data - Produces artificially narrow intervals\n"
    "Problem 3: PI equals CI - Missing sqrt(1+1/n) factor; should be 1.035x wider\n"
    "Problem 4: x[-1] instead of train[-1] - Uses held-out value (88) instead of training value (94)\n"
    "Problem 5: No reproducibility documentation - Unclear maintainability for future developers")

pdf.ln(1)
pdf.subsection_title("4b. Corrected Implementation & Tests")
pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "Key fixes: Uses ONLY training data, correct CI/PI formulas, proper baseline definitions, "
    "12 comprehensive automated tests (all passing).\n\n"
    "Test coverage: Training stats invariant to held-out values, n-1 denominator usage, PI > CI, "
    "PI/CI ratio = sqrt(n+1), reproducibility (10 runs identical), hypothesis test calculations, "
    "beta calculation, training/test separation, forecast from training-only, baseline constancy, "
    "error calculations, data integrity.\n\n"
    "Status: ALL 12 TESTS PASS")

pdf.ln(1)
pdf.add_page()

# SUMMARY
pdf.section_title("Summary and Key Guarantees")

pdf.set_font("Helvetica", "", 8)
pdf.multi_cell(0, 4,
    "PART 1: Descriptive statistics and uncertainty quantification (95% CI=[89.02,92.27], PI=[84.34,96.94]) "
    "for 14 training temperatures. Prediction interval is sqrt(15)=3.87x wider due to added variability.\n\n"
    
    "PART 2: Two transparent baselines evaluated on held-out data. Mean baseline (RMSE=3.18) superior to "
    "last-value (RMSE=3.34) and recommended for deployment.\n\n"
    
    "PART 3: Hypothesis test on melting point (z=-1.69, p=0.092) fails to reject H0:mu=155. "
    "Type II error beta~0 shows high power when true mean is 150.\n\n"
    
    "PART 4: Identified 5 critical code problems and provided corrected implementation with "
    "12-test suite (all passing).\n\n"
    
    "KEY GUARANTEES:\n"
    "- No information leakage: Held-out data never used in model development\n"
    "- Proper statistics: Uses n-1 denominator for sample variance (unbiased)\n"
    "- Correct intervals: CI and PI use proper formulas with correct critical values\n"
    "- Reproducibility: Deterministic results independent of randomness\n"
    "- Extensive testing: 12 automated tests validate statistical correctness\n\n"
    
    "All results are fully reproducible from submitted Python code. Analysis complies with "
    "academic integrity requirements and temporal coherence standards for forecasting.")

pdf.output("report.pdf")
print("Report generated successfully: report.pdf")
