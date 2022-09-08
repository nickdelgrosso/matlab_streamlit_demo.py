from functools import partial
from random import random
import time
from turtle import update
import streamlit as st
import asyncio


async def get_delayed_work(widget):
    await asyncio.sleep(delay := random())
    return delay




event_loop = asyncio.new_event_loop()

for _ in range(20):
    widget = st.empty()
    widget.write("Placeholder")
    (
        event_loop.create_task(
            get_delayed_work(widget)
        )
        .add_done_callback(
            partial(
                lambda widget, t: widget.write(t.result()), 
                widget
            )
        )
    )

event_loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(event_loop)))