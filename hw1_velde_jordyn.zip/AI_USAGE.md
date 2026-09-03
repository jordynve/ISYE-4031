# AI Usage Statement - ISYE 4031 Homework 1

## Tool and Model Used

**Tool**: GitHub Copilot (VS Code extension)  
**Model**: Claude Haiku  
**Agent Type**: General coding assistant for problem-solving and implementation

## Representative Prompts

### Prompt Template 1: Computational Implementation
"Generate Python code to [specific statistical calculation], ensuring it uses only training data (no held-out values). Include [specific feature like confidence intervals, validation]. Show detailed calculations with intermediate steps."

### Prompt Template 2: Audit and Debugging
"Review this proposed statistical code and identify at least 5 distinct problems. For each, explain the consequence rather than just naming the faulty line. Then provide correct implementation."

### Prompt Template 3: Testing and Validation
"Write automated tests to verify: [list of statistical properties]. Each test should confirm [specific aspect] and the test should be independent and reproducible."

## Tasks Delegated to Agent

1. **Implementation of Part 1 Analysis**: Generated code for descriptive statistics (mean, median, variance with n-1 denominator, confidence intervals, prediction intervals) with proper documentation of formulas and assumptions.

2. **Part 2 Baseline Forecasts**: Implemented two transparent forecast baselines with proper separation between training and test periods, ensuring no data leakage.

3. **Part 3 Hypothesis Testing**: Coded one-sample hypothesis test, p-value calculation, and Type II error probability with verification against manual calculations.

4. **Code Audit Implementation**: Generated the analysis.py module that correctly implements all Part 1 and Part 2 calculations, avoiding the identified statistical errors.

5. **Automated Test Suite**: Created comprehensive test_analysis.py with 12 tests covering data integrity, statistical correctness, and reproducibility requirements specified in Part 4c.

6. **Report Preparation**: Assisted with organizing and formatting the written report, including its required sections and numerical results.

## Files Modified or Created

- **analysis.py**: Complete implementation of Parts 1-3 with detailed calculations, plotting, and output formatting
- **test_analysis.py**: 12 automated tests verifying all requirements including:
  - Data integrity (held-out values don't affect training)
  - n-1 denominator in sample variance
  - Prediction interval wider than confidence interval
  - Reproducibility across runs
  - Hypothesis test calculations
  - Type II error calculations

## Tests Proposed and Run

All 12 tests pass:
- `test_training_stats_invariant_to_held_out_values`: PASS
- `test_held_out_not_in_training_calculation`: PASS
- `test_sample_std_uses_n_minus_1_denominator`: PASS
- `test_denominator_impact_on_variance`: PASS
- `test_prediction_interval_wider_than_ci`: PASS
- `test_ci_pi_width_ratio`: PASS (verifies PI/CI margin ratio = sqrt(n+1))
- `test_reproducibility_of_calculations`: PASS
- `test_reproducibility_of_bootstrap_independent_stats`: PASS
- `test_hypothesis_test_calculations`: PASS
- `test_type_ii_error_calculation`: PASS
- `test_data_length_and_split`: PASS
- `test_baseline_forecast_lengths`: PASS

Tests were run with: `pytest -q` returning "12 passed"

## Suggestions Accepted, Revised, or Rejected

### Accepted: Comprehensive Test Suite Structure
The agent's suggestion to create separate test functions for each statistical property (data integrity, variance denominator, interval widths, reproducibility) was accepted. This approach provides clear verification of each requirement and makes debugging easier if any aspect fails.

**Statistical Reason**: Each test isolates one aspect of the requirements, making it easier to identify which statistical principle might be violated. This aligns with the course emphasis on verifiable results.

### Revised: Prediction Interval Formula
The agent initially suggested using a standard prediction interval formula. This was revised to ensure the correct formula x̄ ± t * s * sqrt(1 + 1/n) was used instead of x̄ ± t * SE.

**Statistical Reason**: The prediction interval accounts for both sampling variability and individual observation variability around the mean. Using SE alone (as in confidence intervals) would produce incorrect, artificially narrow intervals.

### Rejected: Use of Random Seed
The agent suggested adding `np.random.seed()` for "reproducibility." This was rejected because:

**Statistical Reason**: The analysis contains no randomness - all calculations are deterministic. Setting a seed implies future code might use randomness, which could introduce confusion. Reproducibility is achieved through using only training data and deterministic calculations, not through seed-setting.

## Unresolved Limitations or Risks

1. **PDF Library Limitations**: The fpdf2 library has restricted font support (Latin-1 encoding). This required replacing mathematical symbols (Greek letters, special characters) with ASCII equivalents. A more robust solution would use reportlab or PDFKit with better Unicode support.

2. **Temporal Autocorrelation Not Modeled**: While the analysis correctly identifies that the 6 held-out forecast errors are not independent (Part 2c), the baseline forecasts themselves don't account for this autocorrelation. A more sophisticated forecast might use ARIMA or exponential smoothing.

3. **Sample Size for Type II Error**: In Part 3c, with n=10, sigma=1.5, and a 5-degree effect size, the Type II error is vanishingly small (≈0). In realistic studies, smaller effect sizes would give more meaningful beta values. This limitation is inherent to the problem specification, not the implementation.

4. **Visualization Clarity**: While plots correctly distinguish training and held-out data, they could be enhanced with annotations showing the exact cutoff time and confidence/prediction interval formulas. This depends on matplotlib capabilities and code complexity.

## Summary

The agent effectively assisted with:
- Translating mathematical formulas into correct Python implementations
- Creating a comprehensive test suite that validates all four requirements
- Generating properly formatted reports and documentation
- Identifying and fixing errors in proposed (intentionally flawed) code

The implementation demonstrates proper data handling (no leakage), correct statistical formulas (n-1 denominator, proper interval construction), and reproducible analysis (deterministic, verifiable results).
