#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Инструменты синхронизации: Semaphore

https://thecode.media/prokachivaem-asinkhronnoe-programmirovanie-na-python-ispolzuem-kontekstnyj-menedzher/
"""

import asyncio


async def shared_data(resource_id, semaphore_arg):
    """Корутина, которая имеет доступ к общему файлу."""
    # используем контекстный менеджер с объектом Semaphore
    async with semaphore_arg:
        # имитация ограниченного процесса
        print(f'Доступ к ресурсу {resource_id} отрыт, идёт работа')
        # сейчас sleep имитирует время работы с ресурсом
        await asyncio.sleep(1)
        print(f'Доступ к ресурсу {resource_id} закрыт, работа закончена')


async def main():
    """Создаём корутину с основной логикой."""
    # semaphore разрешает два асинхронных доступа
    semaphore = asyncio.Semaphore(2)
    # мы запускаем 5 корутин, но semaphore разрешает одновременную работу только двум
    await asyncio.gather(*(shared_data(i, semaphore) for i in range(5)))


# запускаем код
asyncio.run(main())
