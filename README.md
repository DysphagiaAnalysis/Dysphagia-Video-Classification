## This project aims to classify patients with dysphagia with various machine learning and signal processing means.

Extract Features from Hyoid Bone Location Annotations:
- ARMA [(code)](arima_alternative.py)
- HMM + EM [(code)](Read_in_Data.m)

Classfication with HB Features [(code)](arima_alternative.py):
- Logistic Regression 
- SVM
- K-Neighbours 
- GMM

Geniohyoid Muscle Classification [(code)](DL_classification/):
- CNN to extract features from GH mask annotations 
- LSTM for classification 

---

#### Dataset can be found in [Grive](https://drive.google.com/drive/folders/1H-SQDsl4pZmKeGOX7-jT6g7k0b6zq0jY?usp=sharing), and metadata can be found in [info_summary](info_summary/).

- ~ 240 swallow ultrasound clips from healthy adults, healthy elderly, dysphagia patients;

- each from 100 - 600 frames, with a size of 1068 \* 800 pixels^2;

- genihyoid muscle annotations, hyoid bone annotations, and swallowing event timestamp included.

#### Data authorship acknowledgments:

- collected by Huberta Chan;

- annotated by Man Fung, Chan Chan, Audrey Cheung, Hugo;

- cleaned by Suri Feng.
