#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Группировка асинхронных задач в Python

https://thecode.media/prokachivaem-asinkhronnoe-programmirovanie-na-python-ispolzuem-kontekstnyj-menedzher/
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
    # создаём пустой список
    tasks = []
    # создаём контекстный менеджер, используя функцию сразу для нескольких задач
    async with asyncio.TaskGroup() as tg:
        # нумеруем каждую задачу и добавляем их в список
        for i, wait_main in enumerate([1, 2, 3], start=1):
            task = tg.create_task(fetch_data(i, wait_main))
            tasks.append(task)

    # объявляем переменную, в которой лежат результаты всех функций в одном списке
    results = [task.result() for task in tasks]
    # смотрим результат и время появления каждой задачи
    for result in results:
        print(f'Получен результат: {result}')


# запускаем код
asyncio.run(main())
