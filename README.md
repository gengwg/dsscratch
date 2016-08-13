#data science from scratch

## chapter 2 - a crash course in python

The ds community is still firmly stuck on py 2.7.

Anaconda comes with pip and IPython.

https://en.wikipedia.org/wiki/Anaconda_(Python_distribution)

Ipython

white space is ignored inside parentheses and brackets.

```python
"user" in tweet.keys()  # use slow list in 
"user" in tweet         # use fast dict in 
```
dictionary keys must be immutable, e.g. can't use lists as keys.
if i need a multipart key, use a tuple. or turn the key into a string.

## Chapter 3 - Visualizing Data

sudo yum install python-matplotlib

* bar charts
    good for showing how some quantity varies among some discrete set of items.
    plotting histograms of bucketed numeric values, in order to visually explore how the values are distributed.

* line charts
    good for showing trends.

* scatterplots
    for visualizing the relationship between two paired sets of data


## Chapter 4 - Linear Algebra

vectors are points in some finite-dimensional space.

using lists as vectors is great for exposition but terrible for performance.

in production, i would want to use the NumPy library,
which includes a high-performance array class
with all sorts of arithmetic operations included.

represent matrices as lists of lists,
with each inner list having the same length
and representing a row of a matrix.

=> matrix A has len(A) rows, and len(A[0]) columns.

* matrix to represent a data set consisting of multiple vectors.
* use n x k matrix to represent a linear function that maps k-dimensional
 vectors to n-dimensional.
* use to represent binary relationships

## Chapter 5 - Statistics

a generalization of the median is the quantile,
which represents the value less than which a certain percentile of the data lies.
the median represents the value less than which 50% of the data lies.

Simpson's Paradox

correlations can be misleading when confounding variables are ignored.

correlation is measuring the relationship between two variables
all else being equal.

## Chapter 6 - Probability

### A family with two (unknown) children

Assumption:

    1. Each child is equally likely to be a boy or girl
    2. The gender of the second child is independent of
    the gender of the first child

then the event "no girls" has a probability of 1/4,
the event "one girl, one boy" has probability 1/2,
and the event "two girls" has probability 1/4.

**Probability of the event "both children are girls" (B)
conditioned on the event "the older child is a girl" (G)**

    P(B|G) = P(B,G) / P(G) = P(B) / P(G) = 1/2

since the event B and G is just event B.
(Once you know both children are girls, it's necessarily true that
the older child is a girl.)

**Probability of the event "both children are girls" (B)
conditioned on the event "at least one of the children is a girl" (L)**

    P(B|L) = P(B, L) / P(L) = P(B) / P(L) = 1/3

again, the event B and G is just event B.
(If you all you know is that at least one of the children is a girl,
then it is twice as likely that the family has one boy and one girl
than it has both girls.)

### Bayes's Theorem

```
    P(E|F) = P(E,F) / P(F) = P(F|E)*P(E) / P(F)
```

The event F can be split into two mutually exclusive events "F and E" and "F and not E".

```
    P(F) = P(F,E) + P(F,^E)
```

so that

```
    P(E|F) = P(F|E)*P(E) / [P(F|E)*P(E) + P(F|^E)*P(^E)]
```

#### Positive test

A certain disease affects 1 in every 10,000 people.
There is a test for this disease that gives the correct result 99% of the time.

T for "your test is positive";
D for "you have the disease".

Bayes Theorem says that the probability that you have the disease,
conditional on testing positive:

```
    P(D|T) = P(T|D)*P(D) / [P(T|D)*P(D) + P(T|^D)*P(^D)]

P(T|D)  - probability that someone with the disease tests positive = 0.99
P(D)    - probability that any person has the disease: 1/10,000 = 0.0001
P(T|^D) - probability that someone w/o the disease tests positive = 0.01
P(^D)   - probability that any person doesn't have the disease: 0.9999

>>> 0.99*0.0001/(0.99*0.0001 + 0.01*0.9999)
0.00980392156862745

==>
    P(D|T) = 0.98 %
```

Less than 1% of the people who test positive actually have the disease.

A more intuitive way to see this is to image a population of 1 million people.
You expect 100 of them to have disease, 99 of those 100 test positive.
Expect 999,900 not to have disease, 9999 test positive.
Which means you expect 99 out of (99+9999) positive testers to actually have the disease.

### Random Variables

A *random variable* is a variable whose possible values have an
associated probability distribution.

The associated *probability distribution* gives the probability
that the variable realizes each of its possible values.

*Expected value* of a random variable is the average of its value
weighted by their probabilities.

Random variables can be *conditioned* on events.

### Continuous distributions

*discrete distribution* associates positive probabilities with discrete outcomes.

*uniform distribution* puts equal weight on all the numbers between 0 and 1.
Python's random.random() is a random variable with uniform density.

We represent a continuous distribution with a *probability density function* (pdf)
such that the probability of seeing a value in a certain interval
equals the integral of the density function over the interval.

*cumulative distribution function* (cdf) gives the probability
that a random variable is less than or equal to a certain value.

### Normal Distribution

Normal Distribution is completely determined by two factors:
its mean u (mu) and its standard deviation s (sigma).

    f(x|u,s) = 1/sqrt(2*pi)*s * exp(-(x-u)**2 / 2*s**2)

When u = 0 and s =1, it's called *standard normal distribution*.
