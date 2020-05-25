import math
from typing import Sequence, Tuple, Callable, Optional


def normal_cdf(x: float) -> float:
    return (1.0 + math.erf(x * 0.7071067811865)) * 0.5


def binomial_test_statistic(actual: float, expected: float, n: int) -> float:
    return (actual - expected) / math.sqrt(expected * (1.0 - expected) / n)


def two_tailed_p_val(test_statistic: float) -> float:
    return 2.0 * normal_cdf(-abs(test_statistic))


def log_bayes_factor_against_uniform(
        actual: float,
        expected: float,
        n: int) -> float:
    # Uses a normal approximation to the binomial distribution; n should
    # be greater than 9.0 * expected / (1.0 - expected) and
    # 9.0 * (1.0 - expected) / expected.
    assert n > 9.0 * expected / (1.0 - expected), 'Insufficient samples'
    assert n > 9.0 * (1.0 - expected) / expected, 'Insufficient samples'
    # Null hypothesis: n * actual ~ B(n, expected)
    # P_null(actual) = Pr(n * actual == k) where k ~ B(n, expected)
    # which we approximate as P(actual == x) where
    # x ~ N(n*expected, sqrt(n * expected * (1.0 -expected)))
    p_null_approx = (1.0 / math.sqrt(2.0 * math.pi * n * expected * (1.0 - expected))) * \
        math.exp(-0.5 * n * (actual - expected) * (actual - expected) /
                 ((1.0 - expected) * expected))
    # Alternate hypothesis: n * actual ~ B(n, q) where q ~ U(0, 1)
    # integral from 0 to 1 of Pr(n * actual == k) where k ~ B(n, q), dq
    p_alt = 1.0 / (n + 1.0)
    return math.log10(p_null_approx / p_alt)


def get_discrete_histogram(
        samples: Sequence,
        population: Sequence,
        weights: Sequence[float]) -> Tuple:
    assert len(population) == len(weights)
    weights_total = sum(weights)
    weights_normalized = [weight / weights_total for weight in weights]
    histogram = [samples.count(item) / len(samples) for item in population]
    return population, histogram, weights_normalized, 1.0


def get_continuous_histogram(
        samples: Sequence[float],
        low: float,
        high: float,
        histogram_size: int,
        cdf_func: Callable[[float], float]) -> Tuple:
    weights_normalized = [0.0] * histogram_size
    histogram = [0.0] * histogram_size
    population = [None] * histogram_size
    dx = (high - low) / histogram_size
    left = low
    left_cdf = cdf_func(left)
    start_cdf = left_cdf
    for i in range(histogram_size):
        right = left + dx
        right_cdf = cdf_func(right)
        weights_normalized[i] = right_cdf - left_cdf
        histogram[i] = sum(1 for sample in samples if left <= sample < right) / len(samples)
        population[i] = (left, right)
        left = right
        left_cdf = right_cdf
    return population, histogram, weights_normalized, right_cdf - start_cdf


def build_histogram_table(
        n: int,
        population: Sequence,
        histogram: Sequence[float],
        expected_weights: Sequence[float]):
    assert len(histogram) == len(population)
    assert len(expected_weights) == len(population)
    result = [tuple()] * len(population)
    for i in range(len(result)):
        item = population[i]
        actual = histogram[i]
        expected = expected_weights[i]
        bin_test_stat = binomial_test_statistic(actual, expected, n)
        p_val = two_tailed_p_val(bin_test_stat)
        k_val = log_bayes_factor_against_uniform(actual, expected, n)
        result[i] = (item, actual, expected, bin_test_stat, p_val, k_val)
    return result


def _format_population_item(item):
    if isinstance(item, tuple):
        low, high = item
        return '[{0:.3f}, {1:.3f})'.format(low, high)
    else:
        return repr(item)


def _right_justify(items):
    items = list(items)
    width = max(len(x) for x in items)
    return (x.rjust(width) for x in items)


def format_histogram_table(
        test_name: str,
        table: Sequence,
        n: int,
        coverage: float,
        show_all: bool,
        bad_p_val: float,
        bad_log_k: float,
        suspect_p_val: Optional[float] = None,
        suspect_log_k: Optional[float] = None) -> str:
    title_format = '{title} - {n} Samples, {bands} Bands - {cov:.1f}% Support Coverage'
    row_format = '{item} - ' \
                 'Freq: {actual}\tExpected: {expected}\t' \
                 'z = {z}\tp = {p}\tLog k = {k}' \
                 '{message}'

    result = [title_format.format(
        title=test_name,
        n=n,
        bands=len(table),
        cov=coverage * 100.0), None]
    result[-1] = '=' * len(result[-2])

    table = [(item, actual, expected, z, p, k)
             for item, actual, expected, z, p, k
             in table
             if show_all or
             p < (suspect_p_val or bad_p_val) or
             k < (suspect_log_k or bad_log_k)]
    if not table:
        result.append('All bands within expected values.')
        return '\n'.join(result)

    items, actuals, expecteds, zs, ps, ks = zip(*table)
    items = _right_justify(_format_population_item(item) for item in items)
    actuals = _right_justify('{0:.3f}'.format(actual) for actual in actuals)
    expecteds = _right_justify('{0:.3f}'.format(expected) for expected in expecteds)
    zs = _right_justify('{0:+.3f}'.format(z) for z in zs)
    ps = _right_justify('{0:0.3f}'.format(p) for p in ps)
    ks = _right_justify('{0:+0.2f}'.format(k) for k in ks)
    message = ('\tOUT OF RANGE' if (p < bad_p_val or k < bad_log_k) else
               '\tSUSPECT' if ((suspect_p_val and p < suspect_p_val) or
                             (suspect_log_k and k < suspect_log_k))
               else ''
               for _, _, _, _, p, k in table)
    rows_as_str = zip(items, actuals, expecteds, zs, ps, ks, message)

    rows = [row_format.format(
        item=item,
        actual=actual,
        expected=expected,
        z=z, p=p, k=k,
        message=message)
        for item, actual, expected, z, p, k, message
        in rows_as_str]
    result.extend(rows)
    return '\n'.join(result)


def build_metric_table(
        population: Sequence,

        title: str,
        show_all: bool,
        show_suspect: bool,
        suspect_p_val: float,
        bad_p_val: float,
        suspect_bayes: float,
        bad_bayes: float) \
        -> Sequence[str]:
    weights_normalized, histogram, bin_errors, p_vals, bayes_factors = metrics

    def make_row(i):
        return 'Item: {0}\tExpected: {1:.3f}\tActual: {2:.3f}\tZ: {3:+.2f}\tp: {4:.4f}\t'.format(
            population[i], weights_normalized[i], histogram[i], errors[i], p_vals[i])

    suspect_indices = [i
                       for i in range(len(p_vals))
                       if bad_p_val < p_vals[i] <= suspect_p_val]
    bad_indices = [i
                   for i in range(len(p_vals))
                   if p_vals[i] <= bad_p_val]

    result = [title, None]
    result[-1] = '=' * len(result[-2])

    if not suspect_indices and not bad_indices:
        result.append('All frequencies within expected range (p > {})'.format(suspect_p_val))
        result.append('')

    if suspect_indices:
        result.extend(['Suspect frequencies (p < {})'.format(suspect_p_val), None])
        result[-1] = '-' * len(result[-2])
        for i in suspect_indices:
            result.append(make_row(i))
        result.append('')

    if bad_indices:
        result.extend(['Invalid frequencies (p < {})'.format(bad_p_val), None])
        result[-1] = '-' * len(result[-2])
        for i in bad_indices:
            result.append(make_row(i))
        result.append('')
    return result[:-1]


