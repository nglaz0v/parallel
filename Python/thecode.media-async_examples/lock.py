#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Инструменты синхронизации: Lock

https://thecode.media/prokachivaem-asinkhronnoe-programmirovanie-na-python-ispolzuem-kontekstnyj-menedzher/
"""

import asyncio


# переменная общего доступа
shared_data = 0
# объект блокировки
lock = asyncio.Lock()


async def modify_shared_data():
    """Корутина, которая имеет доступ к общему файлу."""
    # говорим, что будем работать с глобальной переменной
    global shared_data
    # запускаем контекстный менеджер
    async with lock:
        # критически важная часть: корутина что-то менят в общем файле
        print(f'Данные до изменения: {shared_data}')
        shared_data += 1
        # имитация IO операции
        await asyncio.sleep(1)
        print(f'Данные после изменения: {shared_data}\n')
        # конец критически важной части


async def main():
    """Создаём корутину с основной логикой."""
    await asyncio.gather(*(modify_shared_data() for _ in range(5)))


# запускаем код
asyncio.run(main())
