#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Инструменты синхронизации: Event

https://thecode.media/prokachivaem-asinkhronnoe-programmirovanie-na-python-ispolzuem-kontekstnyj-menedzher/
"""

import asyncio


async def waiter(event):
    """Корутина, которая ждёт установки event."""
    print(f'Ожидание event для назначения. Сейчас event равен {event}')
    await event.wait()
    print('Event назначено, можно продолжать программу')


async def setter(event):
    """Корутина, которая устанавливает event."""
    # имитация работы
    await asyncio.sleep(2)
    # устанавливаем event и отчитываемся
    event.set()
    print(f'Event назначено внутри корутины setter. Сейчас event равен {event}')


async def main():
    """Создаём корутину с основной логикой."""
    # создаём объект Event
    event = asyncio.Event()
    # запускаем две корутины и смотрим на результат
    await asyncio.gather(waiter(event), setter(event))


# запускаем код
asyncio.run(main())
