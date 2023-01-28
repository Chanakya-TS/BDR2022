# 🚨 Documentation for BDR 🚨

## Resources
Github for [Motor Imagery EEG Detection paper](https://github.com/Chanakya-TS/BDR2022/blob/main/Papers/A_CNN-LSTM_Deep_Learning_Classifier_for_Motor_Imagery_EEG_Detection_Using_a_Low-invasive_and_Low-Cost_BCI_Headband.pdf)

## Get Started

### [Mind Monitor](https://mind-monitor.com/#page-top)
We will use this Mobile application for recording the signals in real time. The app processes the raw data to obtain the brain waves at different frequency bands by using PSD. 

Run the application on a mobile device. We used an iPhone.  Turn on the Muse headset, then connect to the Muse headset through the app via bluetooth connection. 


### Download the Code
Here, we are installing the code onto our local machines. This code will handle how the data is processed and handled within our system.
[CODE](https://github.com/Chanakya-TS/BDR2022)

### Prepare Drone
We used the [CoDroneEDU](https://www.robolink.com/products/codrone-edu), which can be coded using python. After having the batteries charged, insert them into the drone for it to be turn on. Next, the controller needs to be connected to the laptop via USB (seems insignificant, but important). 

### Run Code
Python:

```
pip install
python RealTime_Engagement.py
```

Python3:

```
pip3 install
python3 RealTime_Engagement.py
```
