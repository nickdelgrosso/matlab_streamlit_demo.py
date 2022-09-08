from random import random
import time
import streamlit as st
import asyncio



async def update_widget(widget):
    delay = random() * 2
    delay = 0.5
    await asyncio.sleep(delay)
    widget.write('Updated')


async def main():
    widgets = [st.empty() for _ in range(20)]
    for widget in widgets:
        widget.write("Placeholder")

    
    tasks = [update_widget(widget) for widget in widgets]
    await asyncio.gather(*tasks)


t0 = time.perf_counter()
asyncio.run(main())
print(time.perf_counter() - t0)

