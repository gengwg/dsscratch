from __future__ import division
import random
from matplotlib import pyplot as plt
from functools import partial


def difference_quotient(f, x, h):
    return (f(x + h) - f(x)) / h

def square(x):
    return x * x

def derivative(x):
    return 2 * x

# equivalent define of the partial function tool
def derivative_estimate (x):
    return difference_quotient(square, x, h=0.00001)

def plot_derivative_estimate():
    # due to positional arg 'x' after 'f', square must be positional argument, not kw arg.
    derivative_estimate = partial(difference_quotient, square, h=0.00001)
    #derivative_estimate = partial(difference_quotient, f=square, h=0.00001)

    x = range(-10, 10)
    plt.title("Actual Derivatives vs. Estimates")
    plt.plot(x, map(derivative, x), 'rx', label='Actual')
    plt.plot(x, map(derivative_estimate, x), 'b+', label='Estimate')
    plt.legend(loc=9)
    plt.show()


"""
When f is a function of many variables, it has multiple partial derivatives,
each indicating how f changes when we make small changes injust one of the input variables.

we calculate its ith partial derivative by treating it as a function of just its ith variable,
holding the other variables fixed.
"""
def partial_difference_quotient(f, v, i, h):
    """calculate the ith partial difference quotient of f at v"""
    w = [v_j +(h if j == i else 0)
         for j, v_j in enumerate(v)]

    return (f(w) - f(v)) / h

def estimate_gradient(f, v, h=0.00001):
    return [partial_difference_quotient(f, v, i, h)
            for i, _ in enumerate(v)]

if __name__ == "__main__":
    plot_derivative_estimate()
