"""Statistical helper functions for confidence intervals and percentiles."""

import numpy as np
from scipy import stats as st
from scipy.stats import norm
from scipy.stats import bootstrap

def confidence_interval_t(data, confidence=0.95):
    data_array = 1.0 * np.array(data)
    degree_of_freedom = len(data_array) - 1
    sample_mean, sample_standard_error = np.mean(data_array), st.sem(data_array)
    t = st.t.ppf((1 + confidence) / 2., degree_of_freedom)
    margin_of_error_greedy = sample_standard_error * t
    Confidence_Interval = 1.0 * np.array([sample_mean - margin_of_error_greedy, sample_mean + margin_of_error_greedy])
    return sample_mean, Confidence_Interval, margin_of_error_greedy

def confidence_interval_normal(data, confidence=0.95):
    data_array = 1.0 * np.array(data)
    sample_mean, sample_standard_error = np.mean(data_array), st.sem(data_array)
    z = norm().ppf((1 + confidence) / 2.)
    margin_of_error = sample_standard_error * z
    Confidence_Interval = np.array([sample_mean - margin_of_error, sample_mean + margin_of_error])
    return sample_mean, Confidence_Interval, margin_of_error

def confidence_interval_init(data, confidence=0.95):
    data_array = 1.0 * np.array(data)
    dimensions = data_array.shape
    if len(dimensions) > 1:
        rows, columns = dimensions[0], dimensions[1]
        if columns <= 30:
            sample_mean, Confidence_Interval_array, margin_of_error_greedy = confidence_interval_t(data_array[0], confidence=0.95)
            sample_mean_array = 1.0 * np.array(sample_mean)
            margin_of_error_greedy_array = 1.0 * np.array(margin_of_error_greedy)
            for row in range(1,rows):
                sample_mean_new_row, Confidence_Interval_new_row, margin_of_error_greedy_new_row =\
                    confidence_interval_t(data_array[row], confidence=0.95)
                sample_mean_array = np.append(sample_mean_array, sample_mean_new_row)
                Confidence_Interval_array = np.vstack((Confidence_Interval_array, Confidence_Interval_new_row))
                margin_of_error_greedy_array = np.append(margin_of_error_greedy_array, margin_of_error_greedy_new_row)
            return sample_mean_array, Confidence_Interval_array, margin_of_error_greedy_array
        else:
            sample_mean, Confidence_Interval_array, margin_of_error_greedy = \
                confidence_interval_normal(data_array[0], confidence=0.95)
            sample_mean_array = 1.0 * np.array(sample_mean)
            margin_of_error_greedy_array = 1.0 * np.array(margin_of_error_greedy)
            for row in range(1, rows):
                sample_mean_new_row, Confidence_Interval_new_row, margin_of_error_greedy_new_row = \
                    confidence_interval_normal(data_array[row], confidence=0.95)
                sample_mean_array = np.append(sample_mean_array, sample_mean_new_row)
                Confidence_Interval_array = np.vstack((Confidence_Interval_array, Confidence_Interval_new_row))
                margin_of_error_greedy_array = np.append(margin_of_error_greedy_array, margin_of_error_greedy_new_row)
            return sample_mean_array, Confidence_Interval_array, margin_of_error_greedy_array
    else:
        if len(data_array <= 30):
            return confidence_interval_t(data_array, confidence=0.95)
        else:
            return confidence_interval_normal(data_array, confidence=0.95)

def bootstrap_percentile(data, percentile=50, confidence=0.95, n_resamples=10000):
    def percentile_func(data, axis):
        return np.percentile(data, percentile, axis=axis)

    res = bootstrap((data,), percentile_func, axis=0, confidence_level=confidence, n_resamples=n_resamples)
    return np.percentile(data, percentile),  np.array([res.confidence_interval.low, res.confidence_interval.high])

def bootstrap_percentile_init(data, percentile=50, confidence=0.95, n_resamples=10000):
    data_array = 1.0 * np.array(data)
    dimensions = data_array.shape
    if len(dimensions) > 1:
        rows, columns = dimensions[0], dimensions[1]
        perc, Confidence_Interval_array = bootstrap_percentile(data_array[0], percentile, confidence, n_resamples)
        percentile_array = 1.0 * np.array(perc)
        for row in range(1, rows):
            perc_new_row, Confidence_Interval_new_row = bootstrap_percentile(data_array[row], percentile, confidence, n_resamples)
            percentile_array = np.append(percentile_array, perc_new_row)
            Confidence_Interval_array = np.vstack((Confidence_Interval_array, Confidence_Interval_new_row))
        return percentile_array, Confidence_Interval_array
    else:
        perc, Confidence_Interval_array = bootstrap_percentile(data_array, percentile, confidence, n_resamples)
        return perc, Confidence_Interval_array
