from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import time
import asyncio
from multiprocessing import Process, Queue
import threading

app = Dash(__name__)
data_queue = Queue()
data = pd.DataFrame(columns=['Category', 'Income', 'Expenses', 'Purchases'])

def generate_data_thread():
    global data
    while True:
        time.sleep(2)
        data = pd.DataFrame({
            'Category': ['Food', 'Transport', 'Entertainment', 'Utilities'],
            'Income': (1000, 5000, 2750, 4500),
            'Expenses': np.random.randint(200, 1000, size=4),
            'Purchases': np.random.randint(1, 20, size=4)
        })

def generate_data_process(queue):
    while True:
        time.sleep(2)
        new_data = pd.DataFrame({
            'Category': ['Food', 'Transport', 'Entertainment', 'Utilities'],
            'Income': (4500, 1500, 4750, 2150),
            'Expenses': np.random.randint(200, 1000, size=4),
            'Purchases': np.random.randint(1, 20, size=4)
        })
        queue.put(new_data)

async def generate_data_async():
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
    [Input('interval-component', 'n_intervals'),
     Input('input-method', 'value')]
)
def update_graph(n, method):
    global data
    if method == 'process' and not data_queue.empty():
        data = data_queue.get()
    elif method == 'thread':
        if data.empty:
            return {}, {}, {}
    elif method == 'async':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(generate_data_async())

    pie_fig = px.pie(data, values='Income', names='Category', title='Income Distribution by Category')
    line_fig = px.line(data, x=data['Category'], y='Expenses', title='Monthly Expenses')
    bar_fig = px.bar(data, x='Category', y='Purchases', title='Number of Purchases by Category')

    return pie_fig, line_fig, bar_fig

app.layout = html.Div([
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart'),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),
    dcc.Input(id='input-method', type='text', placeholder='Введите метод: "async", "thread", "process"'),
    html.Button('Запустить', id='submit-button', n_clicks=0),
    html.Div(id='output-method')
])

@app.callback(
    Output('output-method', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('input-method', 'value')
)
def run_method(n_clicks, method):
    if n_clicks > 0:
        if method == 'process':
            data_process = Process(target=generate_data_process, args=(data_queue,))
            data_process.start()
            return f'Запущен метод: {method}'
        elif method == 'thread':
            data_thread = threading.Thread(target=generate_data_thread)
            data_thread.daemon = True
            data_thread.start()
            return f'Запущен метод: {method}'
        elif method == 'async':
            return 'Метод "async" будет использоваться при обновлении графиков.'
        else:
            return 'Неизвестный метод. Используйте "async", "thread" или "process".'
    return ''

if __name__ == "__main__":
    app.run_server(debug=True)