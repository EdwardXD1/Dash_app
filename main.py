from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import time
import asyncio
from multiprocessing import Process, Queue
import threading


class CurrencyDataGenerator:
    """Класс для генерации данных о курсах валют и их изменениях."""

    def __init__(self):
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY']

    def generate_data(self):
        """Генерирует случайные курсы валют и их изменения."""
        rates = np.random.uniform(70, 150, size=len(self.currencies))
        changes = np.random.uniform(-5, 5, size=len(self.currencies))
        return pd.DataFrame({
            'Currency': self.currencies,
            'Rate': rates,
            'Change': changes
        })


class AsyncDataGenerator:
    """Асинхронный генератор данных."""

    async def generate_data(self):
        """Асинхронно генерирует данные о курсах валют."""
        await asyncio.sleep(1)
        generator = CurrencyDataGenerator()
        return generator.generate_data()


app = Dash(__name__)
data_queue = Queue()
data_generator = CurrencyDataGenerator()
async_data_generator = AsyncDataGenerator()


def generate_data_thread():
    """Функция для генерации данных в отдельном потоке."""
    while True:
        time.sleep(2)
        data = data_generator.generate_data()
        data_queue.put(data)


def generate_data_process(queue):
    """Функция для генерации данных в отдельном процессе."""
    while True:
        time.sleep(2)
        new_data = data_generator.generate_data()
        queue.put(new_data)


@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('input-method', 'value')]
)
def update_graph(n, method):
    """Обновляет графики на основе выбранного метода генерации данных."""
    if method == 'process' and not data_queue.empty():
        data = data_queue.get()
    elif method == 'thread' and not data_queue.empty():
        data = data_queue.get()
    elif method == 'async':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(async_data_generator.generate_data())
    else:
        return {}, {}, {}

    pie_fig = px.pie(data, values='Rate', names='Currency', title='Currency Rate Distribution')
    line_fig = px.line(data, x='Currency', y='Rate', title='Currency Rates Over Time')
    bar_fig = px.bar(data, x='Currency', y='Change', title='Currency Rate Changes')

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
    """Запускает выбранный метод генерации данных."""
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
