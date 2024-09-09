#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запускаем несколько корутин из одного места: gather

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
    # запускаем все три корутины одновременно и ждём их выполнения параллельно
    results = await asyncio.gather(fetch_data(1, 3),
                                   fetch_data(2, 3),
                                   fetch_data(3, 3))
    # смотрим на результат и скорость его появления
    for result in results:
        print(result)


# запускаем код
asyncio.run(main())
