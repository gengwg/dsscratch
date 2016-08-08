# dsscratch
data science from scratch

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

**Probability of event "both children are girls" (B)
conditioned on the event "the older child is a girl" (G)**

    P(B|G) = P(B,G) / P(G) = P(B) / P(G) = 1/2

since the event B and G is just event B.
(Once you know both children are girls, it's necessarily true that
the older child is a girl.)

#### Probability of the event "both children are girls" (B)
conditioned on the event "at least one of the children is a girl" (L):

    P(B|L) = P(B, L) / P(L) = P(B) / P(L) = 1/3

again, the event B and G is just event B.

