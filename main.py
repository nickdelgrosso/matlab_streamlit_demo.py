import asyncio
import json
import time


import streamlit as st

from model import AppModel
from math_backend_matlab import MatlabMath, get_matlab_engine



async def main():

    t0 = time.perf_counter()
    

    #% App Initialization
    get_engine = st.experimental_singleton(get_matlab_engine)
    matlab = get_engine()
    math = MatlabMath(engine=matlab)
    init = AppModel(_mathlib=math)  # Use for default values, because Streamlit doesn't always update if "value=" changes between runs.

    if "model" not in st.session_state:
        st.session_state['model'] = init    
    model: AppModel = st.session_state['model']  # Get current model to use



    #% Display

    st.title("Understanding Sine Waves")

    with st.sidebar:
        # model.sampling_freq = st.slider("Sampling Frquency", value=init.sampling_freq, min_value=1, max_value=1000)
        model.sampling_freq = st.slider("Sampling Frequency", value=init.sampling_freq, min_value=1., max_value=200.)
        model.x_start, model.x_stop = st.slider("Time Range:", value=(init.x_start, init.x_stop), min_value=-10., max_value=20., step=0.1, help="the range of x values to show")
        model.cos_freq = st.slider(label="Frequency Cosine", value=init.cos_freq, min_value=0., max_value=model.cos_freq_max)
        model.cos_offset = st.slider(label="Offset Cosine", value=init.cos_offset, min_value=-6., max_value=6., step=0.1)
        model.cos_amplitude = st.slider(label="Amplitude Cosine", value=init.cos_amplitude, min_value=-3., max_value=3., step=0.1)
        model.sin_freq = st.slider(label="Frequency Sine", value=init.sin_freq, min_value=0., max_value=init.sin_freq_max)
        model.sin_offset = st.slider(label="Offset Sine", value=init.cos_offset, min_value=-6., max_value=6., step=0.1)
        model.sin_amplitude = st.slider(label="Amplitude Sine", value=init.sin_amplitude, min_value=-3., max_value=3., step=0.1)
        
        

    with st.spinner("Calculating...", ):
        
        
        st.header("Time Series", anchor="time-series")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            time_linechart = st.empty()
            time_linechart.text("Generating Line Chart...")

        with col2:
            time_table = st.empty()
            time_table.text("Generating Table...")


        st.header("Power Spectrum", anchor="power-spectrum")
        col1, col2, col3 = st.columns([2, 2, 1])

        
        with col1:
            power_linechart = st.empty()
            power_linechart.text("Generating Line Chart...")

        with col2:
            power_table = st.empty()
            power_table.text("Generating Table...")
            

        with col3:
            power_metrics_cos = st.empty()
            power_metrics_cos.text("Generating Measurments...")
            power_metrics_sin = st.empty()
            power_metrics_sin.text("Generating Measurments...")
            
        st.success("Done!")

        st.header("App Performance")
        st.subheader("Time Info")
        cols = st.columns(3)
        with cols[0]:
            perf_report_before = st.empty()
        with cols[1]:
            perf_report_after = st.empty()
        with cols[2]:
            perf_report_final = st.empty()

        st.subheader("Application Model (Debug Info)")
        st.json(json.dumps(model.to_dict()))

        
        perf_report_before.metric("Time until Widgets and Placeholders Rendered", value=f"{int((time.perf_counter() - t0) * 1000)}ms", )
        

        async def render_timeseries(model: AppModel):
            time_df = await model.calc_wide()
            
            await asyncio.sleep(0)
            time_linechart.line_chart(data=time_df, x='x', y=['sin', 'cos'])
            await asyncio.sleep(0)
            time_table.dataframe(time_df.set_index('x').style.background_gradient())
            perf_report_after.metric("Time until Time Series Data Rendered", value=f"{int((time.perf_counter() - t0) * 1000)}ms", )
            

        async def render_powerspectra(model: AppModel):
            
            power_df = await model.calc_power_spectra()
            
            await asyncio.sleep(0)
            power_linechart.line_chart(power_df, x='freq', y=['sine_power', 'cosine_power'])
            await asyncio.sleep(0)
            power_table.dataframe(data=power_df.style.background_gradient())
            
        
        async def render_spectra_metrics(model: AppModel):
            metrics = await model.get_freq_metrics()
            
            power_metrics_cos.metric("Cosine Freq", value=metrics['cos']['freq'])
            await asyncio.sleep(0)
            power_metrics_sin.metric("Sine Freq", value=metrics['sin']['freq'])

        tasks = [render_timeseries(model), render_powerspectra(model), render_spectra_metrics(model)]
        # await asyncio.gather(*tasks)
        for task in tasks:
            await task
        # await get_time_df(model)
        # await get_power_df(model)
        
        perf_report_final.metric("Time to end of Script", value=f"{int((time.perf_counter() - t0) * 1000)}ms", )
        
        
if __name__ == '__main__':
    asyncio.run(main())



