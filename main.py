import json
import streamlit as st

from model import AppModel
from math_backend_matlab import MatlabMath, get_matlab_engine



def main():
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
    st.caption("A Demo Project by Nicholas Del Grosso")

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

        df = model.calc_wide()
        
        with col1:
            st.line_chart(data=df, x='x', y=['sin', 'cos'])

        with col2:
            st.dataframe(df.set_index('x').style.background_gradient())


        st.header("Power Spectrum", anchor="power-spectrum")
        col1, col2, col3 = st.columns([2, 2, 1])

        df = model.calc_power_spectra()
        with col1:
            st.line_chart(df, x='freq', y=['sine_power', 'cosine_power'])

        with col2:
            st.dataframe(data=df.style.background_gradient())

        with col3:
            metrics = model.get_freq_metrics()
            st.metric("Cosine Freq", value=metrics['cos']['freq'])
            st.metric("Sine Freq", value=metrics['sin']['freq'])


        st.success("Done!")
        

        st.write(model)
        st.json(json.dumps(model.to_dict()))

        
if __name__ == '__main__':
    main()



