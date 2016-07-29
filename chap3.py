
from matplotlib import pyplot as plt

## line chart

def make_chart_simple_line_chart():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
    gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

    # create a line chart, years on x-axis, gdp on y-axis
    plt.plot(years, gdp, color='green', marker='o', linestyle='solid')

    # add a title
    plt.title("Nominal GDP")

    # add a lable to the y-axis
    plt.ylabel("Billions of $")

    plt.show()

make_chart_simple_line_chart()

## bar charts

def make_chart_simple_bar_chart(plt):

    movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
    num_oscars = [5, 11, 3, 8, 10]

    # bars are by default width 0.8
    # add 0.1 to the left coordinates so that each bar is centered
    xs = [i + 0.1 for i, _ in enumerate(movies)]

    # plot bars with left x-coordinates [xs], heights [num_oscars]
    plt.bar(xs, num_oscars)

    plt.ylabel("# of Academy Awards")
    plt.title("My Favorite Movies")

    # label x-axis with movie names at bar centers
    plt.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)

    plt.show()

make_chart_simple_bar_chart(plt)

## bar chart of histogram

from collections import Counter


def make_chart_histogram(plt):
    grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]
    decile = lambda grade: grade // 10 * 10
    histogram = Counter(decile(grade) for grade in grades)

    # shift each bar to the left by 4, so they are centered
    # due to below x axis range -5 to 105
    plt.bar([x - 4 for x in histogram.keys()],
            histogram.values(),
            8)  # each bar has a width 8

    # x-axis from -5 to 105, y axis from 0 to 5
    plt.axis([-5, 105, 0, 5])

    plt.xticks([10 * i for i in range(11)])
    plt.xlabel("Decile")
    plt.ylabel("# of Students")
    plt.title("Distribution of Exam 1 grades")

    plt.show()

make_chart_histogram(plt)

def make_chart_misleading_y_axis(plt, mislead=True):
    mentions = [500, 505]
    years = [2013, 2014]

    plt.bar([2012.6, 2013.6], mentions)
    plt.xticks(years)
    plt.ylabel("# of times I heard someone say 'data science'")

    # if you don't do this, matplotlib will lable the x-axis
    # 0, 1, then add a + 2.013e3 off in the corner
    plt.ticklabel_format(useOffset=False)

    if mislead:
        # misleading y-axis only showing the part above 500
        plt.axis([2012.5, 2014.5, 499, 506])
        plt.title("Look at the 'Huge' increase!")
    else:
        plt.axis([2012.5, 2014.5, 0, 550])
        plt.title("Not so huge anymore")

    plt.show()

make_chart_misleading_y_axis(plt, mislead=True)
make_chart_misleading_y_axis(plt, mislead=False)

## multiple line charts

def make_chart_several_line_charts(plt):

    variance     = [1,2,4,8,16,32,64,128,256]
    bias_squared = [256,128,64,32,16,8,4,2,1]
    total_error  = [x + y for x, y in zip(variance, bias_squared)]
    xs = [i for i, _ in enumerate(variance)]

    # make multiple calls to plt.plot
    # to show multiple series on the same chart
    plt.plot(xs, variance,      'g-', label='variance')     # green solid line
    plt.plot(xs, bias_squared,  'r-.', label='bias^2')      # red dot-dashed line
    plt.plot(xs, total_error,   'b:', label='total error')  # blue dotted line

    # assigned labels to each series, get label for free
    plt.legend(loc=9)   # loc=9 means 'top center'
    plt.xlabel("model complexity")
    plt.title("the bias-variance tradeoff")

    plt.show()

make_chart_several_line_charts(plt)

## Scatterplots
def make_chart_scatter_plot(plt):

    friends = [ 70, 65, 72, 63, 71, 64, 60, 64, 67]
    minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    plt.scatter(friends, minutes)

    # label each point
    for label, friend_count, minute_count in zip(labels, friends, minutes):
        plt.annotate(label,
            xy=(friend_count, minute_count),
            xytext=(5, -5),
            textcoords='offset points')

    plt.title("Daily minutes vs Number of friends")
    plt.xlabel("# of Friends")
    plt.ylabel("daily minutes spent on the site")

    plt.show()

make_chart_scatter_plot(plt)

def make_chart_scatterplot_axes(plt, equal_axes=False):

    test_1_grades = [ 99, 90, 85, 97, 80]
    test_2_grades = [100, 85, 60, 90, 70]

    plt.scatter(test_1_grades, test_2_grades)
    plt.xlabel("test 1 grade")
    plt.ylabel("test 2 grade")
    if equal_axes:
        plt.title("Axes are compariable")
        plt.axis("equal")
    else:
        plt.title("Axes aren't compariable")

    plt.show()

make_chart_scatterplot_axes(plt, equal_axes=False)
make_chart_scatterplot_axes(plt, equal_axes=True)