import asyncio
import concurrent.futures
import os
from time import sleep
import time

import threading
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

import streamlit as st


def print_loc(msg):
    print(f"{msg:>25}", os.getpid(), threading.get_ident())

def sleep1():
    sleep(1)
    print_loc("Task")
    
    return "Done 1"

if __name__ == '__main__':

    print_loc("Main")

    t0 = time.perf_counter()


    place3 = st.empty()
    place2 = st.empty()
    place1 = st.empty()

    def show(data):
        st.write(data.result())

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as process_pool:
        task = process_pool.submit(sleep1)
        
        
        # task.
        task.add_done_callback(lambda f: print_loc("Callback"))
        
