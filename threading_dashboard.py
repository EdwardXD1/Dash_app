import time
import threading
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

class CurrencyDataGenerator:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Currency', 'Rate'])

    def generate_data(self):
        """Генерирует случайные курсы валют каждую секунду."""
        while True:
            time.sleep(2)
            self.data = pd.DataFrame({
                'Currency': ['USD', 'EUR', 'GBP', 'JPY'],
                'Rate': np.random.uniform(50, 150, size=4)  # Генерация случайных курсов валют
            })

app = Dash(__name__)
currency_data_generator = CurrencyDataGenerator()


data_thread = threading.Thread(target=currency_data_generator.generate_data)
data_thread.daemon = True
data_thread.start()

def create_pie_chart(data):
    """Создает круговую диаграмму на основе данных."""
    return px.pie(data, values='Rate', names='Currency', title='Currency Rate Distribution')

def create_line_chart(data):
    """Создает линейный график на основе данных."""
    return px.line(data, x='Currency', y='Rate', title='Currency Rates Over Time')

def create_bar_chart(data):
    """Создает столбчатую диаграмму на основе данных."""
    return px.bar(data, x='Currency', y='Rate', title='Currency Rates')

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    """Обновляет графики при каждом интервале."""
    data = currency_data_generator.data
    if data.empty:
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
    app.run(debug=True)
