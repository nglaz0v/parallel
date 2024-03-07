# многопроцессность и многопоточность vs асинхронный ввод-вывод (*Python*)

**Параллельность (*Parallelism*)** - выполнение множества операций в одно и то же время.

**Многопроцессность (*Multiprocessing*)** чаще всего относится к эффекту параллельности и означает распределение задач между частями центральной вычислительной системы (процессорами или ядрами). Многопроцессность хорошо себя показали при задачах связанных с циклами for и математическими вычислениями.

**Одновременность (*Concurrency*)** - это чуть более широкий термин, чем параллельность. Он допускает, что задачи могут выполняться перекрывая друг друга. (это говорит что одновременность не всегда равна параллельности)

**Многопоточность (*Threading*)** - это модель, при которой задача разбивается на множество потоков, занимающихся её решением. Один процесс может содержать множество потоков. Самое важное, что стоит знать о многопоточности — она прекрасно решает задачи связанные с вводом/выводом (I/O) информации. Если задачи, привязанные к расчётам задействуют процессоры на протяжении всего периода решения, то задачи ввода/вывода допускают большие периоды ожиданий.

Чтобы немного подытожить, одновременность включает в себя и многопроцессность (идеальна для задач, требующих многих расчётов) и многопоточность (подходит для задач ввода/вывода). Многопроцессность это форма параллельности, которая является особым типом одновременности. Стандартные библиотеки Python достаточно давно могут поддерживать оба формата с помощью пакетов `multiprocessing` (process-based parallelism), `threading` (thread-based parallelism) и `concurrent.futures` (launching parallel tasks).

Пакет Python `asyncio` (**асинхронный ввод-вывод - *asynchronous I/O***) используется для написания кода, поддерживающего одновременное выполнение задач с использованием синтаксиса `async/await`. Однако она не использует ни мультипроцессность, ни многопоточность. Асинхронный ввод-вывод построен вокруг одного потока и одного процесса: он использует кооперативную многозадачность (*cooperative multitasking*). Другими словами, асинхронность позволяет создать впечатление многопоточности, несмотря на только 1 поток и процесс. Сопрограммы (*coroutines*) (главная особенность асинхронности - специализированная функция-генератор) могут находиться в графике одновременно, но не исполняться.

Чтобы закрепить, асинхронность близка к понятию одновременность, но не использует параллельность. Она ближе к многопоточности, чем к многопроцессности, но имеет так же и множество отличий от этих подходов, заслуживая отдельное место в череде терминов.

Это заставляет нас задуматься, что значит быть асинхронным? Для наших целей наиболее важны два свойства:
- асинхронные подпрограммы способны вставать на паузу, ожидая получение какого-то результата и давая работать другим подпрограммам
- учитывая сказанное выше, асинхронный код позволяет выполнять задачи одновременно. Если быть точным, то он имитирует ощущение одновременности.

Асинхронность удобна в случаях, когда есть большие «периоды ожидания», которые бы блокировали исполнение программы в случае стандартного исполнения кода.

| Concurrency Type | Switching Decision | Number of Processors |
|---|---|:---:|
| Pre-emptive multitasking (`threading`) | The operating system decides when to switch tasks external to Python. | 1 |
| Cooperative multitasking (`asyncio`) | The tasks decide when to give up control. | 1 |
| Multiprocessing (`multiprocessing`) | The processes all run at the same time on different processors. | Many |

**Используйте потоки для одновременного ввода-вывода и процессы для параллельных вычислений.**

## When to Use Concurrency

The first step of this process is deciding if you *should* use a concurrency module. Concurrency always comes with extra complexity and can often result in bugs that are difficult to find.

Hold out on adding concurrency until you have a known performance issue and *then* determine which type of concurrency you need.

Once you’ve decided that you should optimize your program, figuring out if your program is CPU-bound or I/O-bound is a great next step. Remember that I/O-bound programs are those that spend most of their time waiting for something to happen while CPU-bound programs spend their time processing data or crunching numbers as fast as they can.

As you saw, CPU-bound problems only really gain from using `multiprocessing`. `threading` and `asyncio` did not help this type of problem at all.

For I/O-bound problems, there’s a general rule of thumb in the Python community: ***“Use `asyncio` when you can, `threading` when you must.”*** `asyncio` can provide the best speed up for this type of program, but sometimes you will require critical libraries that have not been ported to take advantage of `asyncio`. Remember that any task that doesn’t give up control to the event loop will block all of the other tasks.

---
[Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)  
[Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/)  
