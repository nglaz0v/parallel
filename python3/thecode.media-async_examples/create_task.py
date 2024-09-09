#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создаём отдельные асинхронные задачи через create_task

https://thecode.media/asinkhronnyj-kod-na-python-sintaksis-i-osobennosti/
"""

import asyncio


async def fetch_data(id, wait_time):
    """Создаём корутину, которая симулирует IO операцию."""
    print(f'\nКорутина с IO-операцией {id} начала работу')
    # asyncio.sleep имитирует асинхронное ожидание на внешней системе,
    # мы можем ждать сразу несколько таких операций параллельно
    await asyncio.sleep(wait_time)
    # отчитываемся о завершении работы и возвращаем данные в виде строки
    print(f'Данные из корутины {id} загружены')
    return f'Данные, которые возвращает корутина {id}'


async def main():
    """Создаём корутину с основной логикой."""
    # создаём 3 задачи, используя create_task и корутину с IO-операцией
    task1 = asyncio.create_task(fetch_data(1, 3))
    task2 = asyncio.create_task(fetch_data(2, 3))
    task3 = asyncio.create_task(fetch_data(3, 3))
    # запускаем все три задачи
    result1 = await task1
    result2 = await task2
    result3 = await task3
    # смотрим на результат, который возвращает каждая из задач
    print(result1)
    print(result2)
    print(result3)


# запускаем код
asyncio.run(main())
