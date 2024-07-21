"""Plotly helper fns to generate quick-and-dirty plots using one-liner."""

from typing import Any
from typing import Union

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def splom(
    data_frame: pd.DataFrame,
    dimensions: Union[list[str], None] = None,
    selected_marker_opacity: float = 0.9,
    selected_marker_color: str = "green",
    unselected_marker_opacity: float = 0.1,
    showupperhalf: bool = False,
    diagonal_visible: bool = False,
    **kwargs: Any
) -> Figure:
    """Create a scatter plot matrix (SPLOM).

    Create a scatter plot matrix (SPLOM) for visualizing relationships between
    multiple variables in a data frame.

    It's just a convenience fn to use a one-liner to generate the plot with
    some custom defaults (most of which can be overridden via `**kwargs`). Key
    customizations include the use of `make_hover_template()` to show via
    hover tooltips, all the data associated to one point in the plot.

    This function uses Plotly Express (`px`) to create a scatter matrix where
    each subplot displays the relationship between two variables from the
    provided data frame. Additional features include:

    * **Hover information:** Hovering over a data point displays information
        about all variables (columns) in the data frame using a custom hover
        template. This template is generated by the `make_hover_template`
        function.
    * **Selected point highlighting:** Points corresponding to a selected data
        point in another subplot are highlighted with the specified opacity and
        color.
    * **Customization options:** Keyword arguments (`**kwargs`) can be used to
        further customize the plot appearance (e.g., title, labels, colors).

    Args:
        data_frame (pandas.DataFrame): The data frame containing the data for
            the SPLOM.
        dimensions (list, optional): A list of column names to
            include in the SPLOM. If None, all columns from the data frame are
            used. Defaults to None.
        selected_marker_opacity (float): Opacity of highlighted points
            when a data point is selected in another subplot. Defaults to 0.9.
        selected_marker_color (str): Color of highlighted points.
            Defaults to "green".
        unselected_marker_opacity (float): Opacity of unselected points
            when a data point is selected in another subplot. Defaults to 0.1.
        showupperhalf (bool): Controls whether to display the upper
            triangle of the scatter matrix (default behavior). If True, only
            the lower triangle is displayed. Defaults to False.
        diagonal_visible (bool): Controls whether to display diagonal
            subplots (which typically show the distribution of each variable).
            Defaults to False.
        **kwargs:** Additional keyword arguments passed to `px.scatter_matrix`
            for further customization.

    Returns:
        Figure: The generated scatter plot matrix (SPLOM)
        figure. It can be further manipulated, e.g. `fig.update_layout
        (height=800, width=800,)`, `fig.update_layout(autosize=True)` or shown
        `fig.show(renderer="browser")`
    """
    if dimensions is None:
        dimensions = data_frame.columns.to_list()

    # Set default values for certain keyword arguments and
    # Combine default values with provided kwargs
    default_kwargs = {
        "opacity": 0.35,
        "dimensions": dimensions,
        "hover_data": data_frame.columns,
        # "height": 700,
        # "width": 700,
    }
    merged_kwargs = {**default_kwargs, **kwargs}

    # https://plotly.com/python/splom/
    # https://plotly.com/python/reference/splom/
    # https://plotly.com/python-api-reference/generated/plotly.express.scatter_matrix
    # https://community.plotly.com/t/how-can-i-change-the-color-of-selected-points-in-scatterplots/32013/3
    fig = px.scatter_matrix(data_frame=data_frame, **merged_kwargs)

    fig.update_traces(
        dict(
            selected_marker_color=selected_marker_color,
            selected_marker_opacity=selected_marker_opacity,
            unselected_marker_opacity=unselected_marker_opacity,
            diagonal=dict(visible=diagonal_visible),
            showupperhalf=showupperhalf,
        ),
        selector=dict(type="splom"),
    )

    fig.update_layout(
        autosize=True, legend=dict(x=0.75, y=0.9), margin=dict(l=0, r=0, t=0, b=0)
    )

    fig.update_traces(hovertemplate=make_hover_template(data_frame))

    return fig


def make_hover_template(data: pd.DataFrame, max_hover_height: int = 20) -> str:
    """Make a hover template for Plotly visualizations.

    Make a hover template for Plotly visualizations, to display
    show in the hover information from all columns in the dataset

    This function generates a hover template string for use with Plotly graphs.
    The template displays information about the data point under the cursor,
    including:

    * **Axis labels and values:** The x-axis and y-axis labels are displayed along
      with their corresponding values for the hovered point.
    * **Custom data columns:** Up to `max_hover_height` custom data columns are
      displayed with their corresponding values retrieved from the `customdata`
      attribute of the data frame.
    * **Overflow handling:** If the data frame has more than `max_hover_height`
      custom data columns, a section labeled "Extra" is added, displaying
      additional columns up to a maximum of `2 * max_hover_height`.

    Args:
        data (pandas.DataFrame): The data frame containing the data for the plot.
        max_hover_height (int): The maximum number of custom data
            columns to display in the hover template before adding an "Extra"
            section. Defaults to 20.

    Returns:
        str: The formatted hover template string.
    """
    # https://plotly.com/python/reference/pie/#pie-hovertemplate
    # The variables available in `hovertemplate` are the ones emitted as event
    # data described at this link
    # https://plotly.com/javascript/plotlyjs-events/#event-data. Additionally,
    # every attributes that can be specified per-point (the ones that are
    # `arrayOk: True`) are available. Finally, the template string has access to
    # variables `label`, `color`, `value`, `percent` and `text`. Anything
    # contained in tag `<extra>` is displayed in the secondary box, for example
    # "<extra>{fullData.name}</extra>". To hide the secondary box completely,
    # use an empty tag `<extra></extra>`.
    # https://plotly.com/python/hover-text-and-formatting/customizing-hover-text-with-a-hovertemplate
    hovertemplate = (
        "<b>%{yaxis.title.text}</b>: %{y}"
        + "<br><b>%{xaxis.title.text}</b>: %{x}<br>"
        + "".join(
            [
                "<br>- %s: %%{customdata[%d]}" % (col, i)
                for i, col in enumerate(data.columns[:max_hover_height])
            ]
        )
        + "<extra><br><br>"
        + "".join(
            [
                "<br>- %s: %%{customdata[%d]}" % (col, i)
                for i, col in enumerate(
                    data.columns[max_hover_height : (max_hover_height * 2)]
                )
            ]
        )
        + "</extra>"
    )

    return hovertemplate
