# test
from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data


# Read in global data
movies = data.movies()
movies_nan = movies.dropna(
    subset=["Major_Genre", "Production_Budget", "Distributor"])
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
movies_tidy = movies_nan.select_dtypes(include=numerics)
movies_tidy["Major_Genre"] = movies_nan["Major_Genre"]

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Iframe(
        id='bar',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='Production_Budget',
        options=[{'label': col, 'value': col} for col in movies_tidy.columns])])

# Set up callbacks/backend


@app.callback(
    Output('bar', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair(xcol):
    chart = alt.Chart(movies_tidy, title="Facts about diffrent movie genres").mark_bar().encode(
        x=xcol,
        y='Major_Genre',
        tooltip='Production_Budget').interactive()
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True, port=1234)
