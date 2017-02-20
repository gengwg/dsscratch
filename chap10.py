from collections import Counter
from matplotlib import pyplot as plt
import math
import random
from chap6_probability import inverse_normal_cdf
from chap5_statistics import correlation

def bucketize(point, bucket_size):
    """floor the pont to the nxt lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)

def make_histogram(points, bucket_size):
    """buckets the ponts and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()

def random_normal():
    """:returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

if __name__ == '__main__':
    random.seed(0)

    ## 1 dimension
    # uniform between -100 and 100
    uniform = [200 * random.random() - 100 for _ in range(100000)]

    # normal distribution with mean 0, standard deviation 57
    normal = [57 * inverse_normal_cdf(random.random())
              for _ in range(10000)]

    # both have means close to 0, and standard deviation close to 58.
    # however they have very different distributions.
    plot_histogram(uniform, 10, "Uniform Histogram")
    plot_histogram(normal, 10, "Normal Histogram")

    ## 2 dimension
    xs = [random_normal() for _ in range(1000)]
    ys1 = [ x + random_normal() / 2 for x in xs]
    ys2 = [-x + random_normal() / 2 for x in xs]

    # plot on ys1 and ys2 get very similar looking
    # both are normally distributed with the same mean and standard deviation
    plot_histogram(ys1, 1, title="test")
    plot_histogram(ys2, 1, title="test")

    # each has a very different joint distribution with xs
    plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
    plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    plt.title("Very Different Joint Distributions")
    plt.show()

    # difference would also be apparent if you look at the correlations
    print correlation(xs, ys1)  #  0.9
    print correlation(xs, ys2)  # -0.9
