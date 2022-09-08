import time
import asyncio
import random


async def show_time_after_hello(msg, t0):
    val = random.random() * 2
    await asyncio.sleep(val)
    # time.sleep(1)
    t = time.perf_counter() - t0
    print(f"{msg:<10}", val, t)
    return t

async def main():
    t0 = time.perf_counter()
    # task1 = asyncio.ensure_future(show_time_after_hello("Hello", t0))
    # task2 = asyncio.ensure_future(show_time_after_hello("Goodbye", t0))
    await asyncio.gather(
        show_time_after_hello("Hello", t0),
        show_time_after_hello("Goodbye", t0)
    )
    # asyncio.tasks.
    # await task1
    
    # await task1
    # await task2
    # await task1
    # await task1, task2
    # say_hello(1)
    # print(time.time() - t0)
    # say_hello(1)
    # print(time.time() - t0)
    # loop.run_until_complete(fun1)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    # asyncio.run(main())
    # loop.
