# Snippet to plot a thing with subplots

list_of_frames = []
i = 0
fig, axes = plt.subplots(
    figsize=(
        30, 30), nrows=int(
            define_length(
                len(years))), ncols=int(
                    define_length(
                        len(years))))
for year in years:
    list_of_frames.append(df[df["EXERCICE"] == float(year)].groupby("CODE_COURS")["CODELEV"]
                          .nunique()
                          .reset_index(name="Nb élèves")
                          .sort_values(by="Nb élèves")
                          )
for axe in axes.flatten():
    try:
        axe.title.set_text(f'{years[i]}')
        list_of_frames[i].plot(x="CODE_COURS", kind='bar', ax=axe)
        for p in axe.patches:
            axe.annotate(str(p.get_height()), (p.get_x()
                                               * 1.005, p.get_height() * 1.02))
    except BaseException:
        error = True
        pass
    i = i + 1

if error:
    axes.flat[-1].set_visible(False)

# Snippet to remove None values from dict
clean_dict = {k: v for k, v in dict.items() if v is not None}

# Plot a stacked bar graph with 3D dict input
def bar_plot(
        ax,
        data,
        colors=None,
        total_width=0.8,
        single_width=1,
        legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters

    ----------

    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.
    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.
        Example:
        data = {
            "x":[1,2,3],

            "y":[1,2,3],

            "z":[1,2,3],
        }
    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)
    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.
    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.
    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.

    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)
    # The width of a single bar
    bar_width = total_width / n_bars
    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x +
                         x_offset, y, width=bar_width *
                         single_width, color=colors[i %
                                                    len(colors)], edgecolor='k')

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])
        ax.set_xticklabels(["", 1, 2, 3, 4, 5])
        ax.set_xlabel("Cateǵorie")
        ax.set_ylabel("Nb cours pris")

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())
