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


## Code Organization

```
main.py is the gui script that calls
   AppModel, which has all the data and methods it needs to store and show, and uses
      MatlabMath to do the numerical calculations used with Matlab
```

## Coding Ideas:
  - [ ] Create NumpyMath, an alternate backend that AppModel can use instead of MatlabMath that uses Numpy and Scipy-Signal.  Let the user select which backend should be used via a selection widget.
  - [ ] Fix the power spectrum so the frequencies are correct. 
  - [ ] Create a PyQt app that renders the same information.  Create a CLI that lets the user launch the desired gui backend.
  - [ ] Add a unit circle display, explaining how the sine and cosine are calculated.
  - [x] There's a noticable delay when updating the widgets (~100-200 msecs); could we decrease this by adding some concurrent processing?

