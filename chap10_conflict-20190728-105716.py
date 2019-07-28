from collections import Counter, defaultdict
from matplotlib import pyplot as plt
import math
import random
from chap6_probability import inverse_normal_cdf
from chap5_statistics import correlation
from chap4_linear_algebra import shape, get_column, make_matrix
import dateutil.parser
import csv
import pprint

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


def correlation_matrix(data):
    """returns the num_columns x num_colunmns matrix whos (i, j)th entry
    is the correlation between columns i and j of data"""

    _, num_columns = shape(data)

    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))

    return make_matrix(num_columns, num_columns, matrix_entry)



def scatterplot_matrix(data):

    _, num_columns = shape(data)
    fig, ax = plt.subplots(num_columns, num_columns)

    for i in range(num_columns):
        for j in range(num_columns):

            # scatter column_j on the x axis vs column_i on the y-axis
            if i != j:
                ax[i][j].scatter(get_column(data, j), get_column(data, i))

            # unless i == j, in which case show the series name

            else:
                ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                                    xycoords='axes fraction',
                                    ha='center', va='center')

            # hid axis labels except left and bottom charts
            if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
            if j > 0: ax[i][j].yaxis.set_visible(False)

    # fix the bottom right and top left axis labels, which are wrong
    # because their charts only have text in them
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())

    plt.show()


def parse_row(input_row, parsers):
    """given a list of parsers (some of which may be None)
    apply the appropriate one to each element of the input row"""

    return [parser(value) if parser is not None else value
            for value, parser in zip(input_row, parsers)]


def parse_rows_with(reader, parsers):
    """wrap a reader to apply the parsers to each of its rows"""
    for row in reader:
        yield parse_row(row, parsers)

# bad data we rather get a None than crash our program
def try_or_none(f):
    """wraps f to return None if f raises an exception
    assumes f takes only one input"""

    def f_or_none(x):
        try: return f(x)
        except: return None

    return f_or_none


def parse_row(input_row, parsers):
    """given a list of parsers (some of which may be None)
    apply the appropriate one to each element of the input row"""

    return [try_or_none(parser)(value) if parser is not None else value
            for value, parser in zip(input_row, parsers)]


def try_parse_field(field_name, value, parser_dict):
    """try to parse value using the appropriate functin from parser dict"""
    parser = parser_dict.get(field_name)    # None if no such entry
    if parser is not None:
        return try_or_none(parser)(value)
    else:
        return value


def parse_dict(input_dict, parser_dict):
    return { field_name: try_parse_field(field_name, value, parser_dict)
             for field_name, value in input_dict.iteritems() }


#
# MANIPULATING DATA
#

# pull a field out of a dict
def picker(field_name):
    """returns a function that picks a field out of a dict"""
    return lambda row: row[field_name]

# pluck the same field out of a collection of dicts
def pluck(field_name, rows):
    """turns a list of dicts into the list of field_name values"""
    return map(picker(field_name), rows)


# group rows by the result of a grouper function and
# optionally apply some value_transform to each group
def group_by(grouper, rows, value_transform=None):
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)

    if value_transform is None:
        return grouped
    else:
        return {key : value_transform(rows)
                for key, rows in grouped.iteritems()}


def percent_price_change(yesterday, today):
    return today["closing_price"] / yesterday["closing_price"] - 1

def day_over_day_changes(grouped_rows):
    # sort the rows by date
    ordered = sorted(grouped_rows, key=picker("date"))

    # zip with an offset to get pairs of consecutive days
    return [{ "symbol": today["symbol"],
              "date": today["date"],
              "change": percent_price_change(yesterday, today)}
              for yesterday, today in zip(ordered, ordered[1:])]

if __name__ == '__main__':
    random.seed(0)

    g = picker('symbol')
    print g({'symbol': 'appl'})

    print picker('symbol')({'symbol': 'appl'})

    ## 1 dimension
    # uniform between -100 and 100
    uniform = [200 * random.random() - 100 for _ in range(100000)]

    # normal distribution with mean 0, standard deviation 57
    normal = [57 * inverse_normal_cdf(random.random())
              for _ in range(10000)]

    # both have means close to 0, and standard deviation close to 58.
    # however they have very different distributions.
    #plot_histogram(uniform, 10, "Uniform Histogram")
    #plot_histogram(normal, 10, "Normal Histogram")

    ## 2 dimension
    xs = [random_normal() for _ in range(1000)]
    ys1 = [ x + random_normal() / 2 for x in xs]
    ys2 = [-x + random_normal() / 2 for x in xs]

    # plot on ys1 and ys2 get very similar looking
    # both are normally distributed with the same mean and standard deviation
    #plot_histogram(ys1, 1, title="test")
    #plot_histogram(ys2, 1, title="test")

    # each has a very different joint distribution with xs
    plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
    plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    #plt.title("Very Different Joint Distributions")
    #plt.show()

    # difference would also be apparent if you look at the correlations
    print correlation(xs, ys1)  #  0.9
    print correlation(xs, ys2)  # -0.9

    # first, generate some random data

    num_points = 100


    def random_row():
        row = [None, None, None, None]
        row[0] = random_normal()
        row[1] = -5 * row[0] + random_normal()
        row[2] = row[0] + row[1] + 5 * random_normal()
        row[3] = 6 if row[2] > -2 else 0
        return row


    random.seed(0)
    data = [random_row()
            for _ in range(num_points)]

    pprint.pprint(correlation_matrix(data))

    #scatterplot_matrix(data)

    ## cleaning and mugging

    data = []

    # read and parse in a single step
    with open("comma_delimited_stock_prices.csv", "rb") as f:
        reader = csv.reader(f)
        for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
            data.append(line)

    # only need to check for None rows
    for row in data:
        if any(x is None for x in row): # check if None in row, equivalent to below
        # f None in row:
            print row
    # generally we have 3 options:
        #    get rid of them
        # go back to the source and try to fix the bad/missing data
        # do nothing and cross our fingers

    # know the highest-ever closing price for aapl

    print "stocks"
    with open("stocks.txt", "rb") as f:
        reader = csv.DictReader(f, delimiter="\t")
        data = [parse_dict(row, {'date' : dateutil.parser.parse,
                                'closing_price': float})
                for row in reader]

    # 1. restrict ourselves to aapl rows
    # 2. grab the closing_price from each row
    # 3. take the max of those prices
    max_aapl_price = max(row['closing_price']
                         for row in data
                         if row["symbol"] == "AAPL")

    print "max aapl price", max_aapl_price

    # know the highest-ever closing price for each stock in our data set

    # 1. group together all rows with the same symbol
    # 2. within each group, do the same as before

    # group rows by symbol
    by_symbol = defaultdict(list)
    for row in data:
        by_symbol[row["symbol"]].append(row)

    # print by_symbol["FB"]

    # use a dict comprehensin to find hte max for each symbol
    # output: {'AAPL': 119.0, 'FB': 81.45, 'MSFT': 49.3}
    max_price_by_symbol = {symbol : max(row["closing_price"]
                                        for row in grouped_rows)
                           for symbol, grouped_rows in by_symbol.iteritems()}

    # use group_by
    max_price_by_symbol = group_by(picker("symbol"),
                                   data,
                                   lambda rows: max(pluck("closing_price", rows)))

    print "max price by symbol"
    pprint.pprint(max_price_by_symbol)

    # key is symbol, value is a list of "change" dicts
    changes_by_symbol = group_by(picker("symbol"), data, day_over_day_changes)

    # collect all "change" dicts into one big list
    all_changes = [change
                   for changes in changes_by_symbol.values()
                   for change in changes]

