# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: datapane
#     language: python
#     name: python3
# ---

# %% [markdown]
#  # Beveridge Curve

# %% [markdown]
#  The Beveridge curve, or UV curve, is a graphical representation of the relationship between unemployment and the job vacancy rate, the number of unfilled jobs expressed as a proportion of the labor force.

# %%
import altair as alt
import datapane as dp
import pandas as pd
import pandas_datareader as pdr

# %%
df = pdr.get_data_fred(["UNRATE", "JTSJOR"], start="2000-01-01")

# %%
df


# %%
def beveridge_factor(DF: pd.DataFrame) -> pd.DataFrame:
    return (
        DF.rename(
            columns={"UNRATE": "Unemployment Rate", "JTSJOR": "Job Openings Rate"}
        )
        .rename_axis(index={"DATE": "Date"})
        .assign(
            **{
                "Beveridge Factor": lambda d: d["Job Openings Rate"]
                / d["Unemployment Rate"]
            }
        )
    )


# %%
bv = df.pipe(beveridge_factor)

# %%
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
current_year = pd.Timestamp.today().year

# %%
dp.Blocks(
    "# Beveridge Curve",
    dp.Formula(
        r"\text{Beveridge Factor} = \frac{\text{Job Openings Rate}}{\text{Unemployment Rate}}"
    ),
    dp.Plot(plot & bar_slider),
    f"## Current Year",
    dp.Table(bv.loc[f"{current_year}"]),
)

# %%
