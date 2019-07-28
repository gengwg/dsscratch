from __future__ import division
import math
from chap6_probability import normal_cdf, inverse_normal_cdf
import random

def normal_approximation_to_binomial(n, p):
    """finds out mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

# the normal cdf _is_ the probability the variable is below a threshold
normal_probability_below = normal_cdf

# it's above the threshold if it's not below the threshold
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)

def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


# find nontial region or the interval around the man tha accounts for a certain
# level of likelihood.

def normal_upper_bound(probability, mu=0, sigma=1):
    """:returns z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)

def normal_lower_bound(probability, mu=0, sigma=1):
    """:returns z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """:returns the symetric (about the mean) bounds
    that contains the specified probability

    for example, if we want to find an interval centered at the mean
    and containing 60% probability, we find the cutoffs where
    the upper and lower tails each contain 20% of the probability.
    """
    tail_probability = (1 - probability) / 2

    # upper bound should have tail_probablity above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    # lower bound should have tail_probablity below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound

def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is what's less than x
        return 2 * normal_probability_below(x, mu, sigma)

upper_p_value = normal_probability_above
lower_p_value = normal_probability_below

def run_experiment():
    """flip a coin 1000 times, True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]

def reject_fairness(experiment):
    """using the 5% significance levels"""
    num_heads = len([flip for flip in experiment if flip])

    return num_heads < 469 or num_heads > 531

def estimated_parameters(N, n):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma

def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)


def B(alpha, beta):
    """a normalizing constant so that the total probability is 1"""
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)

def beta_pdf(x, alpha, beta):
    if x < 0 or x > 1:
        return 0
    return x ** (alpha - 1) * (1 - x) * (beta - 1) / B(alpha, beta)


if __name__ == "__main__":

    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    print mu_0, sigma_0

    # 95% bounds based on assumption p is 0.5
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

    # actual mu and sigma based on p = 0.55
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

    # a type 2 error means we fail to reject the null hypothesis
    # which will happen when X is still in our original interval
    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    print power # 0.887

    """
    imagine that our null hypothesis is the coin is not biased toward heads
    or p <= 0.5. In that case we wnat a one-sided test that rejects
    the null hypothesis when X is much larger than 50, but not when
    X is smaller than 50. 5%-significance test involves using the
    normal_probability_blew to find the cutoff below which 95% of the probability
    lies.
    """
    hi = normal_upper_bound(0.95, mu_0, sigma_0)
    # 526 < 531, since we need more prob in the upper tail

    type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
    power = 1- type_2_probability   # 0.936
    print power

    print two_sided_p_value(529.5, mu_0, sigma_0)   # 0.062

    # simulation of p value
    extreme_value_count = 0
    for _ in range(100000):
        num_heads = sum(1 if random.random() < 0.5 else 0   # count # heads
                        for _ in range(1000))               # in 1000 flips
        if num_heads >= 530 or num_heads <= 470:            # count how often
            extreme_value_count += 1                        # the # is extreme
    print extreme_value_count / 100000  # 0.062

    print upper_p_value(524.5, mu_0, sigma_0)   # 0.061
    print upper_p_value(526.5, mu_0, sigma_0)   # 0.047

    # if we observe 525 heads out of 1000 flips, we estimate p equals 0.525
    p_hat = 525 / 1000
    # we don't know p, so instead we use our estimate
    # this is not entirely justified, but people do it.
    mu = p_hat
    sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
    print normal_two_sided_bounds(0.95, mu, sigma)  # [0.4940, 0.5560]

    # if we see 540 heads
    p_hat = 540 / 1000
    mu = p_hat
    sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
    print normal_two_sided_bounds(0.95, mu, sigma)  # [0.5091, 0.5709]

    ## P-hacking
    random.seed(0)
    experiments = [run_experiment() for _ in range(1000)]
    num_rejections = len([experiment
                          for experiment in experiments
                          if reject_fairness(experiment)])

    print num_rejections    # 46

    # if A gets 200 clicks out of 1000 views, B gets 180 out of 1000
    z = a_b_test_statistic(1000, 200, 1000, 180)
    print z # -1.14
    # the probability of seeing such large diff if he means were actuallly equal
    print two_sided_p_value(z)  # 0.254
    # p-value is large enough. can't conclude there's much diff

    # if A gets 200 clicks out of 1000 views, B gets 150 out of 1000
    z = a_b_test_statistic(1000, 200, 1000, 150)
    print z # - 2.94
    print two_sided_p_value(z)  # 0.003
    # which means there's only 0.003 probability you'd see such a large difference
    # if the ads were equally effective
