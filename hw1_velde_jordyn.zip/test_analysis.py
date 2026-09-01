"""
ISYE 4031 Homework 1: Automated Tests for Analysis
Tests for: data integrity, statistical calculations, and reproducibility.
"""

import numpy as np
import pandas as pd
from scipy import stats
import pytest


# ============================================================================
# TEST FIXTURES AND UTILITIES
# ============================================================================

@pytest.fixture
def temperature_data():
    """Fixture providing the temperature dataset."""
    temps = [86, 88, 91, 90, 93, 95, 94, 92, 89, 87,
             88, 90, 92, 94, 96, 95, 93, 91, 90, 88]
    train = np.array(temps[:14], dtype=float)
    test = np.array(temps[14:], dtype=float)
    return train, test, temps


def calculate_mean_ci_and_pi(train_data):
    """
    Calculate 95% CI for mean and 95% PI for single observation.
    Returns (ci_lower, ci_upper, pi_lower, pi_upper)
    """
    n = len(train_data)
    mean = np.mean(train_data)
    std = np.std(train_data, ddof=1)
    se = std / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, n - 1)
    
    ci_lower = mean - t_crit * se
    ci_upper = mean + t_crit * se
    
    pi_lower = mean - t_crit * std * np.sqrt(1 + 1/n)
    pi_upper = mean + t_crit * std * np.sqrt(1 + 1/n)
    
    return ci_lower, ci_upper, pi_lower, pi_upper


def calculate_baselines(train_data, test_length):
    """
    Calculate mean and last-value baselines.
    Returns (mean_baseline, last_value_baseline)
    """
    mean_baseline = np.repeat(np.mean(train_data), test_length)
    last_value_baseline = np.repeat(train_data[-1], test_length)
    return mean_baseline, last_value_baseline


# ============================================================================
# TEST 1: Held-out values cannot affect training summaries or forecasts
# ============================================================================

def test_training_stats_invariant_to_held_out_values(temperature_data):
    """
    Test that changing held-out values does not change:
    - Training mean
    - Training std dev
    - Training variance
    - Baseline forecasts (mean and last-value)
    - Confidence intervals
    - Prediction intervals
    """
    train, test, temps_original = temperature_data
    
    # Calculate baseline results using original data
    original_mean = np.mean(train)
    original_var = np.var(train, ddof=1)
    original_std = np.std(train, ddof=1)
    original_mean_baseline, original_last_value = calculate_baselines(train, len(test))
    original_ci = calculate_mean_ci_and_pi(train)
    
    # Create modified dataset with different held-out values
    temps_modified = list(temps_original)
    temps_modified[14] = 50  # Change day 15 dramatically
    temps_modified[15] = 60  # Change day 16
    temps_modified[16] = 70  # Change day 17
    temps_modified[17] = 75  # Change day 18
    temps_modified[18] = 80  # Change day 19
    temps_modified[19] = 85  # Change day 20
    
    train_modified = np.array(temps_modified[:14], dtype=float)
    test_modified = np.array(temps_modified[14:], dtype=float)
    
    # Calculate results with modified data
    modified_mean = np.mean(train_modified)
    modified_var = np.var(train_modified, ddof=1)
    modified_std = np.std(train_modified, ddof=1)
    modified_mean_baseline, modified_last_value = calculate_baselines(train_modified, len(test_modified))
    modified_ci = calculate_mean_ci_and_pi(train_modified)
    
    # Assert that training summaries are unchanged
    assert original_mean == modified_mean, \
        f"Mean changed: {original_mean} vs {modified_mean}"
    assert original_var == modified_var, \
        f"Variance changed: {original_var} vs {modified_var}"
    assert original_std == modified_std, \
        f"Std dev changed: {original_std} vs {modified_std}"
    
    # Assert that baselines are unchanged
    np.testing.assert_array_equal(original_mean_baseline, modified_mean_baseline,
                                  err_msg="Mean baseline changed with held-out values")
    np.testing.assert_array_equal(original_last_value, modified_last_value,
                                  err_msg="Last-value baseline changed with held-out values")
    
    # Assert that intervals are unchanged
    np.testing.assert_array_almost_equal(original_ci, modified_ci,
                                        err_msg="Confidence/prediction intervals changed with held-out values")


def test_held_out_not_in_training_calculation():
    """
    Verify that held-out values are truly excluded from all training calculations.
    """
    temps = [86, 88, 91, 90, 93, 95, 94, 92, 89, 87,
             88, 90, 92, 94, 96, 95, 93, 91, 90, 88]
    train = np.array(temps[:14], dtype=float)
    test = np.array(temps[14:], dtype=float)
    
    # Calculate mean of only training set
    train_mean = np.mean(train)
    
    # Verify that this is different from mean of all data
    all_mean = np.mean(temps)
    assert train_mean != all_mean, "Training mean should differ from overall mean"
    
    # Verify that test values are truly separate
    assert len(train) == 14, f"Train should have 14 values, has {len(train)}"
    assert len(test) == 6, f"Test should have 6 values, has {len(test)}"
    assert np.all(np.isin(train, temps[:14])), "Training set should only contain first 14 values"
    assert np.all(np.isin(test, temps[14:])), "Test set should only contain last 6 values"


# ============================================================================
# TEST 2: Sample standard deviation uses n-1 denominator
# ============================================================================

def test_sample_std_uses_n_minus_1_denominator(temperature_data):
    """
    Test that the sample standard deviation calculation uses n-1 denominator,
    not n. This is the unbiased estimator.
    """
    train, _, _ = temperature_data
    
    n = len(train)
    
    # Manual calculation with n-1 (unbiased)
    mean = np.mean(train)
    sum_sq_dev = np.sum((train - mean) ** 2)
    var_unbiased = sum_sq_dev / (n - 1)
    std_unbiased = np.sqrt(var_unbiased)
    
    # Manual calculation with n (biased)
    var_biased = sum_sq_dev / n
    std_biased = np.sqrt(var_biased)
    
    # NumPy with ddof=1 should match unbiased
    std_numpy = np.std(train, ddof=1)
    var_numpy = np.var(train, ddof=1)
    
    # NumPy with ddof=0 should match biased
    std_biased_numpy = np.std(train, ddof=0)
    var_biased_numpy = np.var(train, ddof=0)
    
    # Assertions
    assert np.isclose(std_numpy, std_unbiased), \
        f"NumPy ddof=1 doesn't match manual n-1: {std_numpy} vs {std_unbiased}"
    assert np.isclose(var_numpy, var_unbiased), \
        f"Variance with n-1: {var_numpy} vs {var_unbiased}"
    
    assert np.isclose(std_biased_numpy, std_biased), \
        f"NumPy ddof=0 doesn't match manual n: {std_biased_numpy} vs {std_biased}"
    
    # Verify that n-1 produces larger values (correct for sample)
    assert std_unbiased > std_biased, "Sample std (n-1) should be > population std (n)"
    assert var_unbiased > var_biased, "Sample var (n-1) should be > population var (n)"


def test_denominator_impact_on_variance(temperature_data):
    """
    Verify that using n-1 vs n makes a material difference.
    """
    train, _, _ = temperature_data
    n = len(train)
    
    # Calculate both
    var_with_n_minus_1 = np.var(train, ddof=1)
    var_with_n = np.var(train, ddof=0)
    
    # The ratio should be n/(n-1)
    expected_ratio = n / (n - 1)
    actual_ratio = var_with_n_minus_1 / var_with_n
    
    assert np.isclose(actual_ratio, expected_ratio), \
        f"Ratio of variances should be {expected_ratio}, got {actual_ratio}"
    
    # For n=14, this should be 14/13 ≈ 1.077
    assert 1.07 < actual_ratio < 1.08, "Denominator correction should be ~1.077 for n=14"


# ============================================================================
# TEST 3: Prediction interval wider than confidence interval
# ============================================================================

def test_prediction_interval_wider_than_ci(temperature_data):
    """
    Test that the 95% prediction interval for a single new observation
    is wider than the 95% confidence interval for the population mean.
    """
    train, _, _ = temperature_data
    
    ci_lower, ci_upper, pi_lower, pi_upper = calculate_mean_ci_and_pi(train)
    
    ci_width = ci_upper - ci_lower
    pi_width = pi_upper - pi_lower
    
    # PI should be wider than CI
    assert pi_width > ci_width, \
        f"PI width ({pi_width:.4f}) should be > CI width ({ci_width:.4f})"
    
    # Check margins of error specifically
    mean = np.mean(train)
    ci_margin = ci_upper - mean
    pi_margin = pi_upper - mean
    
    assert pi_margin > ci_margin, \
        f"PI margin ({pi_margin:.4f}) should be > CI margin ({ci_margin:.4f})"


def test_ci_pi_width_ratio(temperature_data):
    """
    Test that the PI margin is √(n+1) times the CI margin.
    
    PI margin = t_crit * s * √(1 + 1/n)
    CI margin = t_crit * s/√n
    Ratio = [s * √(1 + 1/n)] / [s / √n] = √(1 + 1/n) * √n = √(n+1)
    """
    train, _, _ = temperature_data
    n = len(train)
    mean = np.mean(train)
    std = np.std(train, ddof=1)
    se = std / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, n - 1)
    
    # CI margin
    ci_margin = t_crit * se
    
    # PI margin should be t_crit * std * √(1 + 1/n)
    pi_margin = t_crit * std * np.sqrt(1 + 1/n)
    
    # The ratio of margins should be √(n+1)
    expected_margin_ratio = np.sqrt(n + 1)
    actual_margin_ratio = pi_margin / ci_margin
    
    assert np.isclose(actual_margin_ratio, expected_margin_ratio, rtol=1e-10), \
        f"PI/CI margin ratio should be √(n+1)={expected_margin_ratio:.6f}, got {actual_margin_ratio:.6f}"


# ============================================================================
# TEST 4: Repeated runs produce identical results
# ============================================================================

def test_reproducibility_of_calculations(temperature_data):
    """
    Test that running the same calculations multiple times produces
    identical results (no randomness involved).
    """
    train, test, _ = temperature_data
    
    results_list = []
    
    for run in range(10):
        mean = np.mean(train)
        std = np.std(train, ddof=1)
        var = np.var(train, ddof=1)
        median = np.median(train)
        iqr = np.percentile(train, 75) - np.percentile(train, 25)
        
        ci_lower, ci_upper, pi_lower, pi_upper = calculate_mean_ci_and_pi(train)
        mean_baseline, last_value_baseline = calculate_baselines(train, len(test))
        
        mae_mean = np.mean(np.abs(mean_baseline - test))
        rmse_mean = np.sqrt(np.mean((mean_baseline - test)**2))
        mae_last = np.mean(np.abs(last_value_baseline - test))
        rmse_last = np.sqrt(np.mean((last_value_baseline - test)**2))
        
        results = {
            'mean': mean,
            'std': std,
            'var': var,
            'median': median,
            'iqr': iqr,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'pi_lower': pi_lower,
            'pi_upper': pi_upper,
            'mae_mean': mae_mean,
            'rmse_mean': rmse_mean,
            'mae_last': mae_last,
            'rmse_last': rmse_last,
            'mean_baseline': mean_baseline.copy(),
            'last_value_baseline': last_value_baseline.copy(),
        }
        results_list.append(results)
    
    # All runs should produce identical results
    first_results = results_list[0]
    for run_num, results in enumerate(results_list[1:], start=2):
        for key in first_results:
            if isinstance(first_results[key], np.ndarray):
                np.testing.assert_array_equal(first_results[key], results[key],
                    err_msg=f"Run 1 and {run_num} differ in {key}")
            else:
                assert first_results[key] == results[key], \
                    f"Run 1 and {run_num} differ in {key}: {first_results[key]} vs {results[key]}"


def test_reproducibility_of_bootstrap_independent_stats():
    """
    Verify that statistics computed from fixed data are perfectly reproducible.
    """
    temps = [86, 88, 91, 90, 93, 95, 94, 92, 89, 87,
             88, 90, 92, 94, 96, 95, 93, 91, 90, 88]
    train = np.array(temps[:14], dtype=float)
    
    # Run calculations 5 times
    results = []
    for _ in range(5):
        r = np.corrcoef(np.arange(len(train)), train)[0, 1]  # Simple correlation
        m = np.mean(train)
        s = np.std(train, ddof=1)
        results.append((r, m, s))
    
    # All should be identical
    for i in range(1, 5):
        assert results[0] == results[i], \
            f"Run 1 and {i+1} should be identical but differ"


# ============================================================================
# TEST 5: Hypothesis test calculations (Part 3 verification)
# ============================================================================

def test_hypothesis_test_calculations():
    """
    Verify Part 3 hypothesis test calculations are correct.
    """
    n = 10
    x_bar = 154.2
    sigma = 1.5
    mu_0 = 155
    alpha = 0.01
    
    # Test statistic
    z_stat = (x_bar - mu_0) / (sigma / np.sqrt(n))
    expected_z_stat = -1.6865
    assert np.isclose(z_stat, expected_z_stat, atol=0.002), \
        f"z_stat should be ~{expected_z_stat}, got {z_stat}"
    
    # Critical value
    z_crit = stats.norm.ppf(1 - alpha/2)
    expected_z_crit = 2.5758
    assert np.isclose(z_crit, expected_z_crit, atol=0.001), \
        f"z_crit should be ~{expected_z_crit}, got {z_crit}"
    
    # P-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    assert 0.085 < p_value < 0.095, \
        f"p-value should be ~0.089, got {p_value}"
    
    # Decision (should fail to reject at α=0.01)
    assert abs(z_stat) < z_crit, "Should fail to reject H0"
    assert p_value > alpha, f"p-value ({p_value}) should be > α ({alpha})"


def test_type_ii_error_calculation():
    """
    Verify Part 3c Type II error calculation.
    When the true mean is 150°F (5°F away from H0: 155°F) with n=10 and σ=1.5,
    beta should be very small because the effect size is large.
    """
    n = 10
    sigma = 1.5
    mu_0 = 155
    mu_a = 150  # Alternative hypothesis mean (5°F away)
    alpha = 0.01
    
    z_crit = stats.norm.ppf(1 - alpha/2)
    se = sigma / np.sqrt(n)
    
    # Acceptance region boundaries (in terms of sample mean)
    x_bar_lower = mu_0 - z_crit * se
    x_bar_upper = mu_0 + z_crit * se
    
    # P(Type II error) = P(accept H0 | true mean is mu_a)
    z_lower = (x_bar_lower - mu_a) / se
    z_upper = (x_bar_upper - mu_a) / se
    
    beta = stats.norm.cdf(z_upper) - stats.norm.cdf(z_lower)
    
    # Beta must be in [0,1]
    assert 0 <= beta <= 1, f"Beta must be in [0,1], got {beta}"
    
    # With a large effect size (5°F), beta should be very small
    # Beta is essentially 0 because the true mean is so far from H0
    assert beta < 0.001, f"Beta should be very small for large effect size, got {beta}"


# ============================================================================
# TEST 6: Data integrity and basic statistics
# ============================================================================

def test_data_length_and_split(temperature_data):
    """Test that data is correctly split into train (14) and test (6)."""
    train, test, temps = temperature_data
    
    assert len(temps) == 20, f"Total temps should be 20, got {len(temps)}"
    assert len(train) == 14, f"Train should have 14, got {len(train)}"
    assert len(test) == 6, f"Test should have 6, got {len(test)}"


def test_baseline_forecast_lengths(temperature_data):
    """Test that baseline forecasts have correct length."""
    train, test, _ = temperature_data
    
    mean_baseline, last_value_baseline = calculate_baselines(train, len(test))
    
    assert len(mean_baseline) == len(test), \
        f"Mean baseline should have {len(test)} forecasts"
    assert len(last_value_baseline) == len(test), \
        f"Last-value baseline should have {len(test)} forecasts"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
