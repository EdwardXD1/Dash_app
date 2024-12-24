from multiprocessing import Process, Queue
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import time

app = Dash(__name__)

data_queue = Queue()
data = pd.DataFrame(columns=['Category', 'Income', 'Expenses', 'Purchases'])

def generate_data(queue):
    while True:
        time.sleep(2)
        new_data = pd.DataFrame({
            'Category': ['Food', 'Transport', 'Entertainment', 'Utilities'],
            'Income': (4500, 1500, 4750, 2150),
            'Expenses': np.random.randint(200, 1000, size=4),
            'Purchases': np.random.randint(1, 20, size=4)
        })
        queue.put(new_data)

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global data
    if not data_queue.empty():
        data = data_queue.get()

    if data.empty:
        return {}, {}, {}

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
    process = Process(target=generate_data, args=(data_queue,))
    process.start()
    app.run_server(debug=True)
