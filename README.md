# Automatic Offside Detection
## _AI Lab: Computer Vision and NLP_


Project related to the exam AI lab: Computer Vision and NLP of the academic year 2023/2024. Authors:

- Tommaso Bernardini
- Simone La Bella
- Mattia Di Marco
- Jacopo Spallotta


The project is structured in three parts:
- Homography
- Team Classification
- GUI

# Installation

## Clone
```sh
git clone https://github.com/simolb7/Automatic-Offside-Detection.git
```

## Install dependencies


> **DISCLAIMER**: A 3.10 or later Python version is required.

The following packages are required to run the application
```sh
# for homography
tqdm
torch
numpy
os
PIL
# for team classification
ultralytics
sklearn
os
numpy
cv2
math
# for GUI
tkinter
```

## How To Run
1. Move to directory where you previously installed the repository
2. Launch 
```sh
python mainGUI.py
```
3. The application makes a prediction on which team is attacking in the picture and marks this team as Team A but the user still can choose which team is attacking beetween Team A and Team B.
4. Video demonstration
   

https://github.com/simolb7/Automatic-Offside-Detection/assets/149960121/0c9ccf2a-8788-42e4-be8c-88198bd99232




