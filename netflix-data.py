import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"

netflix_data = pd.read_csv("netflix_content_2023.csv")

netflix_data.head()

netflix_data["Hours Viewed"] = netflix_data["Hours Viewed"].replace(",", "", regex=True).astype(float)

netflix_data[["Title", "Hours Viewed"]].head()

content_type_viewership = netflix_data.groupby("Content Type")["Hours Viewed"].sum()

fig = go.Figure(data=[go.Bar(
        x = content_type_viewership.index,
        y = content_type_viewership.values,
        marker_color = ["skyblue", "salmon"]
    )
])

fig.update_layout(
    title = "Total Viewership Hours by Content Type (2023)",
    xaxis_title = "Content Type",
    yaxis_title = "Total Hours Viewed (in billions)",
    xaxis_tickangle = 0,
    height = 500,
    width = 800
)

fig.show()


language_viewership = netflix_data.groupby("Language Indicator")["Hours Viewed"].sum().sort_values(ascending=False)

fig = go.Figure(data=[go.Bar(
        x = language_viewership.index,
        y = language_viewership.values,
        marker_color = "lightcoral"
    )
])

fig.update_layout(
    title = "Total Viewership Hours by Language (2023)",
    xaxis_title = "Language",
    yaxis_title = "Total Hours Viewed (in billions)",
    xaxis_tickangle = 45,
    height = 600,
    width = 1000
)

fig.show()


netflix_data["Release Date"] = pd.to_datetime(netflix_data["Release Date"])
netflix_data["Release Month"] = netflix_data["Release Date"].dt.month



monthly_viewership = netflix_data.groupby("Release Month")["Hours Viewed"].sum()

fig = go.Figure(data=[go.Scatter(
        x = monthly_viewership.index,
        y = monthly_viewership.values,
        mode = "lines+markers",
        marker = dict(color= "blue"),
        line = dict(color= "blue")
    )
])

fig.update_layout(
    title = "Total Viewership Hours by Release Month (2023)",
    xaxis_title= "Month",
    yaxis_title= "Total Hours Viewed (in billions)",
    xaxis=dict(
        tickmode = "array",
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ),
    height = 600,
    width = 1000
)

fig.show()


"""top_5_titles = netflix_data.nlargest(5, "Hours Viewed")

top_5_titles[["Title", "Hours Viewed", "Language Indicator", "Content Type", "Release Date"]]"""



monthly_viewership_by_type = netflix_data.pivot_table(index = "Release Month",
                                                      columns = "Content Type",
                                                      values = "Hours Viewed",
                                                      aggfunc = "sum")

fig = go.Figure()

for content_type in monthly_viewership_by_type.columns:
    fig.add_trace(
        go.Scatter(
            x = monthly_viewership_by_type.index,
            y = monthly_viewership_by_type[content_type],
            mode = "lines+markers",
            name = content_type
        )
    )

fig.update_layout(
    title = "Viewership Trends by Content Type and Release Month (2023)",
    xaxis_title= "Month",
    yaxis_title= "Total Hours Viewed (in billions)",
    xaxis = dict(
        tickmode = "array",
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ),
    height = 600,
    width = 1000,
    legend_title = "Content Type"
)

fig.show()


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


netflix_data["Release Season"] = netflix_data["Release Month"].apply(get_season)


seasonal_viewership = netflix_data.groupby("Release Season")["Hours Viewed"].sum()


seasons_order = ["Winter", "Spring", "Summer", "Fall"]
seasonal_viewership = seasonal_viewership.reindex(seasons_order)

fig = go.Figure(data=[go.Bar(
        x = seasonal_viewership.index,
        y = seasonal_viewership.values,
        marker_color = "red"
    )
])

fig.update_layout(
    title = "Total Viewership Hours by Release Season (2023)",
    xaxis_title = "Season",
    yaxis_title = "Total Hours Viewed (in billions)",
    xaxis_tickangle = 0,
    height = 500,
    width = 800,
    xaxis = dict(
        categoryorder = "array",
        categoryarray = seasons_order
    )
)

fig.show()



monthly_releases = netflix_data["Release Month"].value_counts().sort_index()

monthly_viewership = netflix_data.groupby("Release Month")["Hours Viewed"].sum()

fig = go.Figure()

fig.add_trace(go.Bar(
        x = monthly_releases.index,
        y = monthly_releases.values,
        name = "Number of Releases",
        marker_color = "goldenrod", 
        opacity = 0.7,
        yaxis = "y1"
    )
)

fig.add_trace(
    go.Scatter(
        x = monthly_viewership.index,
        y = monthly_viewership.values,
        name = "Viewership Hours",
        mode = "lines+markers",
        marker = dict(color = "red"),
        line = dict(color = "red"),
        yaxis = "y2"
    )
)

fig.update_layout(
    title = "Monthly Release Patterns and Viewership Hours (2023)",
    xaxis = dict(
        title = "Month",
        tickmode = "array",
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ),
    yaxis = dict(
        title = "Number of Releases",
        showgrid = False,
        side = "left"
    ),
    yaxis2 = dict(
        title = "Total Hours Viewed (in billions)",
        overlaying = "y",
        side = "right",
        showgrid = False
    ),
    legend = dict(
        x = 1.05,  
        y = 1,
        orientation = "v",
        xanchor = "left"
    ),
    height = 600,
    width = 1000
)

fig.show()


netflix_data["Release Day"] = netflix_data["Release Date"].dt.day_name()

weekday_releases = netflix_data["Release Day"].value_counts().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)


weekday_viewership = netflix_data.groupby("Release Day")["Hours Viewed"].sum().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

fig = go.Figure()

fig.add_trace(go.Bar(
        x = weekday_releases.index,
        y = weekday_releases.values,
        name = "Number of Releases",
        marker_color = "blue",
        opacity = 0.6,
        yaxis = "y1"
    )
)

fig.add_trace(go.Scatter(
        x = weekday_viewership.index,
        y = weekday_viewership.values,
        name = "Viewership Hours",
        mode = "lines+markers",
        marker = dict(color="red"),
        line = dict(color="red"),
        yaxis = "y2"
    )
)

fig.update_layout(
    title = "Weekly Release Patterns and Viewership Hours (2023)",
    xaxis = dict(
        title = "Day of the Week",
        categoryorder = "array",
        categoryarray = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ),
    yaxis = dict(
        title = "Number of Releases",
        showgrid = False,
        side = "left"
    ),
    yaxis2 = dict(
        title = "Total Hours Viewed (in billions)",
        overlaying = "y",
        side = "right",
        showgrid = False
    ),
    legend = dict(
        x = 1.05,  
        y = 1,
        orientation = "v",
        xanchor = "left"
    ),
    height = 600,
    width = 1000
)

fig.show()
