from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import asyncio
import random


class CurrencyDataGenerator:
    """Класс для генерации данных о курсах валют."""

    def __init__(self):
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY']

    async def generate_data(self):
        """Генерирует случайные курсы валют."""
        await asyncio.sleep(1)
        rates = np.random.uniform(70, 150, size=len(self.currencies))  # Генерация случайных курсов
        return pd.DataFrame({
            'Currency': self.currencies,
            'Rate': rates,
            'Change': np.random.uniform(-5, 5, size=len(self.currencies))  # Изменение курса
        })


def create_pie_chart(data):
    """Создает круговую диаграмму на основе данных о курсах валют."""
    return px.pie(data, values='Rate', names='Currency', title='Currency Rate Distribution')


def create_line_chart(data):
    """Создает линейный график на основе данных о курсах валют."""
    return px.line(data, x='Currency', y='Rate', title='Currency Rates Over Time')


def create_bar_chart(data):
    """Создает столбчатую диаграмму на основе данных о курсах валют."""
    return px.bar(data, x='Currency', y='Change', title='Currency Rate Changes')


app = Dash(__name__)
data_generator = CurrencyDataGenerator()


@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
async def update_graph(n):
    """Обновляет графики при каждом интервале."""
    data = await data_generator.generate_data()

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

if __name__ == '__main__':
    app.run_server(debug=True)