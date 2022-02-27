# CCHD-2022
A Python program can collect, record and analyze CCHD(Critical congenital heart disease) symptom. 

## Hardware Requirments
1. A Linux computer with BLE(Bluetooth Low Energy) support.
2. Nonin 3150 WristOx2 Pulse Oximeter x2

## Dependencies 
- [Bluepy: Python interface to Bluetooth LE on Linux](https://github.com/IanHarvey/bluepy)
- [dtw-python: Dynamic Time Warping in Python](https://dynamictimewarping.github.io/python/)
- [Pandas: powerful Python data analysis toolkit](https://pandas.pydata.org/)
- [PyQt5: Python bindings for the Qt cross platform application toolkit](https://pypi.org/project/PyQt5/)
- [Matplotlib: Visualization with Python](https://matplotlib.org/)
- [SciPy: Fundamental algorithms for scientific computing in Python](https://scipy.org/)
- [scikit-learn: machine learning in Python](https://scikit-learn.org/)

## Installation
### Install Python dependencies
You can install the packages from a real or a virtual Python environment.

```bash
pip3 install bluepy dtw-python pandas PyQt5 matplotlib scipy scikit-learn
```

### Download the code from source
```bash
git clone https://github.com/wasdwasd0105/CCHD_2022
```

### Configuration
The file `Config/config.ini` configs the connection of Nonin Oximeter devices and the CCHD and AWAD model selection. 

To use the project, you need to specify the MAC address of the devices, the filename of the pre-trained models, and their corresponding features. 

```ini
# config.ini
[Nonin]
Hand_MAC = 08:6b:d7:1f:e3:47
Foot_MAC = 08:6b:d7:1f:d1:62

[AWAD_model]
model_name = AWAD_RF.joblib
model_features = 'Sys Ratio','Dias/Sys Ratio','Mid Sys Val','Amplitude'

[CCHD_model]
model_name = CCHD_self_2f.joblib
model_features = 'Max_PAI_h','Variance_SPO2_f'
```

