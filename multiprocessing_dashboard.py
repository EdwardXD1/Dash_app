from multiprocessing import Process, Queue
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import time

class CurrencyDataGenerator:
    def __init__(self, queue):
        self.queue = queue

    def generate_data(self):
        """Генерирует случайные курсы валют каждую секунду."""
        currencies = ['USD', 'EUR', 'GBP', 'JPY']
        while True:
            time.sleep(2)
            new_data = pd.DataFrame({
                'Currency': currencies,
                'Rate': np.random.uniform(50, 150, size=len(currencies))  # Генерация случайных курсов валют
            })
            self.queue.put(new_data)

def create_pie_chart(data):
    """Создает круговую диаграмму на основе данных."""
    return px.pie(data, values='Rate', names='Currency', title='Currency Rate Distribution')

def create_line_chart(data):
    """Создает линейный график на основе данных."""
    return px.line(data, x='Currency', y='Rate', title='Currency Rates Over Time')

def create_bar_chart(data):
    """Создает столбчатую диаграмму на основе данных."""
    return px.bar(data, x='Currency', y='Rate', title='Currency Rates')

app = Dash(__name__)
data_queue = Queue()
data_generator = CurrencyDataGenerator(data_queue)

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    """Обновляет графики при каждом интервале."""
    if not data_queue.empty():
        data = data_queue.get()
    else:
        return {}, {}, {}

    pie_fig = create_pie_chart(data)
    line_fig = create_line_chart(data)
    bar_fig = create_bar_chart(data)

    return pie_fig, line_fig, bar_fig

app.layout = html.Div([
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart'),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
])

if __name__ == "__main__":
    data_process = Process(target=data_generator.generate_data)
    data_process.start()

    app.run(debug=True)