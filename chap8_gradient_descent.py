from __future__ import division
import random
from matplotlib import pyplot as plt
from functools import partial
import math

from chap4_linear_algebra import *

def sum_of_squares(v):
    """compute sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)

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

## using the gradient

def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [v_i + step_size * direction_i
            for v_i, direction_i in zip(v, direction)]

def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]

def safe(f):
    """returns a new function that is the same as f
    except that it otputs infinity whenever f produces an error"""
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return float('inf')

    return safe_f

## step size

def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.0001):
    """use gradient descent to find theta that minimizes target function"""

    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00000001]

    theta = theta_0
    target_fn = safe(target_fn)
    value = target_fn(theta)

    while True:
        gradient = gradient_fn(theta)
        next_thetas = [step(theta, gradient, -step_size)
                for step_size in step_sizes]

        next_theta = min(next_thetas, key=target_fn)
        next_value = target_fn(next_theta)

        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value

## if we want to maximize a funtion, we can do by minimizing its negative
## which has a corresponding negative gradient

def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)

def negate_all(f):
    """return a function that for any input x returns -f(x)
    when f returns a list of numbers"""
    return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]

def maximize_batch(target_fn, gradient_fn, theta_0, tolerance=0.0001):
    return minimize_batch(negate(target_fn),
                          negate_all(gradient_fn),
                          theta_0,
                          tolerance)

## Stochastic Gradient Descent

def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i, _ in enumberate(data)]  # create a list of indexes
    random.shuffle(indexes)                     # shuffle them
    for i in indexes:                           # return the data in that order
        yield data[i]

def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):

    data = zip(x,y)
    theta = theta_0     # initial guess
    alpha = alpha_0     # initial step size
    min_theta, min_value = None, float("inf")   # the minimum so far
    iterations_with_no_improvement = 0

    while iterations_with_no_improvement < 100:
        value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )

        if value < min_value:
            min_theta, min_value = theta, value
            iterations_with_no_improvement = 0
            alpha = alpha_0
        else:
            iterations_with_no_improvement += 1
            alpha *= 0.9

        for x_i, y_i in in_random_order(data):
            gradient_i = gradient_fn(x_i, y_i, theta)
            theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))

    return min_theta

if __name__ == "__main__":
    #plot_derivative_estimate()

    ## using the gradient

    # pick a random starting point
    v = [random.randint(-10, 10) for i in range(3)]
    tolerance = 0.00000001

    while True:
        gradient = sum_of_squares_gradient(v)   # compute the gradient at v
        next_v = step(v, gradient, -0.01)       # take a negative gradient step
        if distance(next_v, v) < tolerance:     # stop if we are converging
            break
        v = next_v                              # continue if we are not

    print v
    #print minimize_batch(sum_of_squares, sum_of_squares_gradient, [99, 0.8, 0.8])
    print minimize_batch(sum_of_squares, sum_of_squares_gradient, [random.randint(-10, 10) for i in range(3)])
