# pytest -s tests/ --cov=epyfun
from epyfun.plotly import splom

import pandas as pd


# TODO: good practice in testing plots
def test_splom() -> None:
    df_iris = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-11-27/baltimore_bridges.csv"
    )

    # plot all variables in df
    toy = splom(df_iris)

    # plot only selected variables, without naming the argument
    toy = splom(df_iris, ["lat", "long", "yr_built"])

    # plot only selected variables, naming the argument
    toy = splom(df_iris, dimensions=["lat", "long", "yr_built"])

    # override some defaults
    toy = splom(
        df_iris,
        dimensions=["lat", "long", "yr_built"],
        opacity=0.3,
        selected_marker_opacity=0.1,
    )
