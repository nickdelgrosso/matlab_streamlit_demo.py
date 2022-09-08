import time
import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx, add_script_run_ctx
import threading

widgets = [st.empty() for _ in range(20)]
for widget in widgets:
    widget.write("Placeholder")


def update_widget(widget):
    time.sleep(.0000000000001)
    widget.write(f'Updated on thread {threading.get_ident()}')


for widget in widgets:
    thread = threading.Thread(target=update_widget, args=(widget,), daemon=True)
    add_script_run_ctx(thread, ctx=get_script_run_ctx())
    thread.start()


