# %% [markdown]
# # Beveridge Curve

# %%
import altair as alt
import datapane as dp
import pandas as pd
import pandas_datareader as pdr

# %%
bv = pdr.get_data_fred(["UNRATE", "JTSJOR"], start="2000-01-01")

bv.rename(
    columns={"UNRATE": "Unemployment Rate", "JTSJOR": "Job Openings Rate"}, inplace=True
)
bv.index.name = "Date"
bv["Beveridge Factor"] = bv["Job Openings Rate"] / bv["Unemployment Rate"]

select_year = alt.selection_interval(encodings=["x"])

bar_slider = (
    alt.Chart(bv.reset_index())
    .mark_bar()
    .encode(x="year(Date)", y="mean(Beveridge Factor)")
    .properties(height=50, width=800)
    .add_selection(select_year)
)

plot = (
    alt.Chart(bv.reset_index())
    .mark_point(size=100)
    .encode(
        x="Unemployment Rate",
        y="Job Openings Rate",
        color="Job Openings Rate",
        tooltip=["Date", "Unemployment Rate", "Job Openings Rate"],
        opacity=alt.condition(select_year, alt.value(0.7), alt.value(0.1)),
    )
    .interactive()
).properties(
    title="The Beveridge Curve (job openings rate vs. unemployment rate), seasonally adjusted",
    width=800,
    height=400,
)
plot & bar_slider


# %%
dp.Report(dp.Plot(plot & bar_slider), dp.DataTable(bv))

# %%
