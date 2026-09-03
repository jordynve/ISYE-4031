"""Corrected Part 4b implementation for transparent forecast baselines."""

import numpy as np
from scipy import stats


def training_summary(train_data, confidence=0.95):
    """Return training-only summary statistics and intervals."""
    train = np.asarray(train_data, dtype=float)
    if train.ndim != 1 or train.size < 2:
        raise ValueError("train_data must be a one-dimensional array with at least two values")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    n = train.size
    mean = np.mean(train)
    std = np.std(train, ddof=1)
    t_critical = stats.t.ppf(1 - (1 - confidence) / 2, n - 1)
    ci_margin = t_critical * std / np.sqrt(n)
    pi_margin = t_critical * std * np.sqrt(1 + 1 / n)

    return {
        "n": n,
        "mean": mean,
        "std": std,
        "variance": np.var(train, ddof=1),
        "ci": (mean - ci_margin, mean + ci_margin),
        "pi": (mean - pi_margin, mean + pi_margin),
    }


def mean_baseline(train_data, forecast_horizon):
    """Forecast the training mean at every future time point."""
    train = np.asarray(train_data, dtype=float)
    return np.repeat(np.mean(train), forecast_horizon)


def last_value_baseline(train_data, forecast_horizon):
    """Forecast the final observed training value at every future time point."""
    train = np.asarray(train_data, dtype=float)
    return np.repeat(train[-1], forecast_horizon)


def evaluate_forecast(forecast, observed):
    """Evaluate a fixed forecast against held-out observations."""
    forecast = np.asarray(forecast, dtype=float)
    observed = np.asarray(observed, dtype=float)
    if forecast.shape != observed.shape:
        raise ValueError("forecast and observed must have the same shape")
    errors = forecast - observed
    return {
        "mae": np.mean(np.abs(errors)),
        "rmse": np.sqrt(np.mean(errors**2)),
    }
