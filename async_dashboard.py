from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import asyncio

app = Dash(__name__)

async def generate_data():
    await asyncio.sleep(1)
    return pd.DataFrame({
        'Category': ['Food', 'Transport', 'Entertainment', 'Utilities'],
        'Income': (2000, 1750, 4000, 3500),
        'Expenses': np.random.randint(200, 1000, size=4),
        'Purchases': np.random.randint(1, 20, size=4)
    })

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(generate_data())

    pie_fig = px.pie(data, values='Income', names='Category', title='Income Distribution by Category')
    line_fig = px.line(data, x=data['Category'], y=data['Expenses'], title='Monthly Expenses')
    bar_fig = px.bar(data, x='Category', y='Purchases', title='Number of Purchases by Category')

    return pie_fig, line_fig, bar_fig

app.layout = html.Div([
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart'),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
])

if __name__ == '__main__':
    app.run_server(debug=True)
