# How do you combine Streamlit, Python, and Matlab?

This was a small experiment used to learn Streamlit and Matlab's Python Engine. 
It shows a couple sine waves and computes a power spectrum (incorrectly, it turns out, though that's my fault)

![screenshot](imgs/screenshot.png)

## Install

### Install Matlab Engine

Note: need administrative permission in Windows
```
cd <matlab_install_directory>/extern/engines/python 
pip install .
```

### Install Python deps
```
cd <this_repo>
pip install -r requirements.txt
```

## Run
```
streamlit run main.py
```
