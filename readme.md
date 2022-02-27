# CCHD_2022
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

## Configuration
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

## Usage



## Feture work
- Continue train the models using new data.
- Add fast banchmark script.
- Replace bluepy with [Bleak](https://github.com/hbldh/bleak) to support mutiple platform (Windows, MacOS, Android).  

## Credit

### A Machine Learning Driven Pipeline for Automated Photoplethysmogram Signal Artifact Detection
#### Abstract
Recent advances in Critical Congenital Heart Dis-
ease (CCHD) research using Photoplethysmography (PPG) sig-
nals have yielded an Internet of Things (IoT) based enhanced
screening method that performs CCHD detection comparable
to SpO2 screening. The use of PPG signals, however, poses a
challenge due to its measurements being prone to artifacts. To
comprehensively study the most effective way to remove the
artifact segments from PPG waveforms, we performed feature
engineering and investigated both Machine Learning (ML) and
rule based algorithms to identify the optimal method of artifact
detection. Our proposed artifact detection system utilizes a 3-
stage ML model that incorporates both Gradient Boosting (GB)
and Random Forest (RF). The proposed system achieved 84.01%
of Intersection over Union (IoU), which is competitive to state-
of-the-art artifact detection methods tested on higher resolution
PPG.


### Enhanced Critical Congenital Cardiac Disease Screening by Combining Interpretable Machine Learning Algorithms
#### Abstract
Critical Congenital Heart Disease (CCHD) screen-
ing that only uses oxygen saturation (SpO2), measured by pulse
oximetry, fails to detect an estimated 900 US newborns annually.
The addition of other pulse oximetry features such as perfusion
index (PIx), heart rate, pulse delay and photoplethysmography
characteristics may improve detection of CCHD, especially
those with systemic blood flow obstruction such as Coarctation
of the Aorta (CoA). To comprehensively study the most relevant
features associated with CCHD, we investigated interpretable
machine learning (ML) algorithms by using Recursive Feature
Elimination (RFE) to identify an optimal subset of features.
We then incorporated the trained ML models into the cur-
rent SpO2-alone screening algorithm. Our proposed enhanced
CCHD screening system, which adds the ML model, improved
sensitivity by approximately 10 percentage points compared to
the current standard SpO2-alone method with minimal to no
impact on specificity.