from functools import partial
from random import random
import time
from turtle import update
import streamlit as st
import asyncio


async def get_delayed_work(widget):
    await asyncio.sleep(delay := random() * 3) 
    return delay


def extract_result(fun):
    def wrapper(task: asyncio.Task, *args, **kwargs):
        result = task.result()
        return fun(result, *args, **kwargs)
    return wrapper



event_loop = asyncio.new_event_loop()


status = st.empty()

for _ in range(20):
    widget = st.empty()
    widget.write("Placeholder")
    task = event_loop.create_task(get_delayed_work(widget))
    task.add_done_callback(extract_result(widget.write))
    task.add_done_callback(status.write)

event_loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(event_loop)))