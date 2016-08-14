from __future__ import division
import random
from matplotlib import pyplot as plt

## conditional probability
def random_kid():
    return random.choice(["boy", "girl"])

both_girls = 0
older_girl = 0
either_girl = 0

random.seed(0)
for _ in range(10000):
    younger = random_kid()
    older = random_kid()
    if older == "girl":
        older_girl += 1
    if older == "girl" and younger == "girl":
        both_girls += 1
    if older == "girl" or younger == "girl":
        either_girl += 1

print "P(both | older):", both_girls / older_girl
print "P(both | either):", both_girls / either_girl


# density function for uniform distribution
def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0

print uniform_pdf(0.4)


# cumulative distribution function for uniform distribution
def uniform_cdf(x):
    ":returns the probability that a uniform randomn variable is <= x"
    if x < 0:   return 0    # uniform random is nver less than 0
    elif x < 1: return x    # e.g. P(x <= 0.4) = 0.4
    else:       return 1        # uniform random is always less than 1

print uniform_cdf(0.4)

import math
# normal distribution
def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return math.exp(-(x-mu) ** 2 /2 / sigma ** 2) / (sqrt_two_pi * sigma)

print normal_pdf(0.4)

def plot_normal_pdf(plt):
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_pdf(x, sigma=1) for x in xs], '-', label='mu=0, sigma=1')
    plt.plot(xs, [normal_pdf(x, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
    plt.plot(xs, [normal_pdf(x, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
    plt.plot(xs, [normal_pdf(x, mu=-1) for x in xs], '-.', label='mu=-1, sigma=1')
    plt.title("Various normal pdfs")
    plt.legend()
    plt.show()

plot_normal_pdf(plt)

# the cumulative distribution function for normal distribution
# cannot be written in "elementary" manner.
# we can use python's math.erf Error Function
def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x -mu) / math.sqrt(2) / sigma)) / 2

def plot_normal_cdf(plt):
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_cdf(x, sigma=1) for x in xs], '-', label='mu=0, sigma=1')
    plt.plot(xs, [normal_cdf(x, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
    plt.plot(xs, [normal_cdf(x, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
    plt.plot(xs, [normal_cdf(x, mu=-1) for x in xs], '-.', label='mu=-1, sigma=1')
    plt.title("Various normal cdfs")
    plt.legend(loc=4)
    plt.show()

plot_normal_cdf(plt)

# invert normal_cdf to find the value corresponding
# to a specific probability. use binary search
def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find the approximate inverse using binary search"""

    # if not standard, compute standard and rescale??
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0     # normal_cdf(-10) is (very close to) 0
    hi_z,  hi_p  =  10.0, 1     # normal_cdf(10) is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2  # consider midpoint
        mid_p = normal_cdf(mid_z)  # the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            hi_z, hi_p = mid_z, mid_p
        else:
            break

    return mid_z

print inverse_normal_cdf(0.2, mu=3)

# Bernoulli(p) random variable equals 1 with probability p
# and 0 with probability 1-p
def bernoulli_trial(p):
    return 1 if random.random() < p else 0

print bernoulli_trial(0.5)

# A Binomial(n,p) random variable is sum of n independent
# Bernoulli(p) random variables
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))

# plot both binomial and normal
def make_hist(p, n, num_points):

    data = [binomial(n, p) for _ in range(num_points)]

    from collections import Counter
    # use a bar chart t oshow the actual binomial samples
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
            [v / num_points for v in histogram.values()],
            0.8,
            color='0.75')

    # use a line chart to show the normal approximation
    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))

    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma)
    #ys = [normal_pdf(i, mu, sigma)
          for i in xs]
    plt.plot(xs, ys)
    plt.title("binomial distribution vs normal approximation")
    plt.show()

make_hist(0.75, 100, 10000)