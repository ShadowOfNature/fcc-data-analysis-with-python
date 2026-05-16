import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=True
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(16, 6))

    ax.plot(df.index, df["value"])

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    df_bar = df_bar[month_order]

    fig = df_bar.plot(
        kind="bar",
        figsize=(10, 8)
    ).figure

    ax = fig.axes[0]
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    df_box = df.copy()

    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]
    df_box["month_num"] = [d.month for d in df_box.date]

    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig