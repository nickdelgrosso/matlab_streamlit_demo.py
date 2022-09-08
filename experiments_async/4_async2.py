from functools import partial
from random import random
import time
from turtle import update
import streamlit as st
import asyncio



async def get_delayed_work(widget):
    await asyncio.sleep(delay := random())
    return delay


async def main():
    for _ in range(20):
        widget = st.empty()
        widget.write("Placeholder")
        (
            asyncio.create_task(
                get_delayed_work(widget)
            )
            .add_done_callback(
                partial(
                    lambda widget, t: widget.write(t.result()), 
                    widget
                )
            )
        )
    
    await asyncio.gather(*asyncio.all_tasks())
    

t0 = time.perf_counter()
asyncio.run(main())
print(time.perf_counter() - t0)

