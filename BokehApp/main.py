from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh.layouts import column
import pandas as pd

# Load and prep data
df = pd.read_csv(
    "data/311_Service_Requests_from_2024_clean.csv",
    parse_dates=["Created Date", "Closed Date"],
    dtype={"Incident Zip": str}
)
df = df[(df["Created Date"].dt.year == 2024) & df["Closed Date"].notna()]
df["response_hours"] = (df["Closed Date"] - df["Created Date"]).dt.total_seconds() / 3600
df["year_month"] = df["Closed Date"].dt.to_period("M").astype(str)

# overall average monthly averages
overall = df.groupby("year_month")["response_hours"].mean().reset_index()

# Wigits
zipcodes = sorted(df["Incident Zip"].dropna().unique())
zip1_select = Select(title = "Zipcode 1", value = zipcodes[0], options = list(zipcodes))
zip2_select = Select(title = "Zipcode 2", value = zipcodes[1], options = list(zipcodes))

# Data Sources
def make_sources(z1,z2):
    overall_src = ColumnDataSource(overall)
    zip1 = df[df["Incident Zip"] == z1].groupby("year_month")["response_hours"].mean().reset_index()
    zip1_src = ColumnDataSource(zip1)

    zip2 = df[df["Incident Zip"] == z2].groupby("year_month")["response_hours"].mean().reset_index()
    zip2_src = ColumnDataSource(zip2)

    

    return overall_src, zip1_src, zip2_src

overall_src, zip1_src, zip2_src = make_sources(zip1_select.value, zip2_select.value)

overall = df.groupby("year_month")["response_hours"].mean().reset_index()
overall = overall.sort_values("year_month")

# Plot
plot = figure(x_range=overall["year_month"],
              title="Average Response Time by Month (hours)",
              x_axis_label="Month", y_axis_label="Hours"
              )


plot.line(x="year_month", y="response_hours", source=overall_src, color="black", legend_label="All 2024", line_width=2)
plot.line(x="year_month", y="response_hours", source=zip1_src, color="blue", legend_label="Zipcode 1", line_width=2)
plot.line(x="year_month", y="response_hours", source=zip2_src, color="red", legend_label="Zipcode 2", line_width=2)
months_2024 = [f"2024-{m:02d}" for m in range(1,13)]
plot.x_range.factors = months_2024
plot.legend.location = "top_left"

# call backs
def update(attr, old, new):
    z1, z2 = zip1_select.value, zip2_select.value
    _, z1_tmp, z2_tmp = make_sources(z1, z2)
    zip1_src.data = dict(z1_tmp.data)
    zip2_src.data = dict(z2_tmp.data)

zip1_select.on_change("value", update)
zip2_select.on_change("value", update)

# layout
layout = column(zip1_select, zip2_select, plot)

curdoc().add_root(layout)

