# Интерактивный дашборд с использованием асинхронного программирования в Python

## Описание проекта

Проект направлен на создание интерактивного дашборда, который демонстрирует различные подходы к асинхронному программированию в Python. 
Реализованы три подхода для генерации данных и их визуализации: 
- asyncio для асинхронного выполнения;
- threading для многопоточности;
- multiprocessing для распределения задач по процессам.

## Цели проекта:
- Обеспечить интерактивность и наглядность данных.
- Демонстрировать использование различных подходов к асинхронному программированию.
- Показать преимущества и недостатки каждого из подходов.

## Установка проекта  

1. Клонируйте проект с GitHub:
git clone https://github.com/EdwardXD1/Dash_app

2. Создайте виртуальное окружение (если используется):  
python -m venv venv #
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate  # Для Windows

3. Установите зависимости:  
pip install -r requirements.txt

## Основной функционал

Главные модули и их функции:  

### 1. Асинхронный подход (asyncio)
- Генерация данных с использованием asyncio.
- Обновление графиков с помощью асинхронных вызовов.

### 2. Многопоточность (threading)
- Генерация данных в отдельном потоке.
- Обновление графиков с использованием глобальных переменных.

### 3. Мультипроцессинг (multiprocessing)
- Генерация данных в отдельном процессе.
- Использование очереди для передачи данных между процессами.

## Структура проекта  

- main.py - Главный файл запуска
- asyncio_module.py - Модуль для работы с asyncio
- threading_module.py - Модуль для работы с threading
- multiprocessing_module.py - Модуль для работы с multiprocessing
- README.md - Документация проекта
- requirements.txt - Список зависимостей

## Автор проекта

Эдвард Кулагин, начинающий разработчик Python
