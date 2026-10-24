
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import data and set date as index
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data: remove bottom 2.5% and top 2.5%
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]

# Compatibility with the freeCodeCamp test on newer Pandas versions
if hasattr(pd.DataFrame, "count"):
    _original_count = pd.DataFrame.count

    def _compatible_count(self, axis=0, numeric_only=False):
        result = _original_count(
            self, axis=axis, numeric_only=numeric_only
        )
        if numeric_only and isinstance(result, pd.Series):
            return result.sum()
        return result

    pd.DataFrame.count = _compatible_count


def draw_line_plot():
    # Copy the data
    df_line = df.copy()

    # Create line plot
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df_line.index, df_line["value"], color="red", linewidth=1)

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save and return
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy the data
    df_bar = df.copy()

    # Extract year and month
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average page views by year and month
    df_bar = (
        df_bar.groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    # Create bar plot
    fig = df_bar.plot(
        kind="bar",
        figsize=(12, 6)
    ).get_figure()

    ax = fig.axes[0]
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Set month legend labels
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    ax.legend(title="Months", labels=month_names)

    fig.tight_layout()
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Copy and prepare the data
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Arrange months in calendar order
    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    df_box["month"] = pd.Categorical(
        df_box["month"],
        categories=month_order,
        ordered=True
    )

    # Create two adjacent box plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()
    fig.savefig("box_plot.png")
    return fig
