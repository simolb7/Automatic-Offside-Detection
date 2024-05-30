# Automatic Offside Detection
## _AI Lab: Computer Vision and NLP_


Project related to the exam AI lab: Computer Vision and NLP of the academic year 2023/2024.\
\
Authors:

- Tommaso Bernardini
- Simone La Bella https://github.com/simolb7
- Mattia Di Marco https://github.com/SasakiKun22
- Jacopo Spallotta


The project is structured in three parts:
- Homography
- Team Classification
- GUI

```
├── GUI
│   └── src
│       ├── elements
│       ├── fonts
│       ├── icons
│       ├── images
│       └── offside
├── mainGUI.py
├── model
│   ├── sportsfield_release
│   │   ├── calculateHomography.py
│   │   ├── data
│   │   ├── datasets
│   │   │   ├── aligned_dataset.py
│   │   │   └── __init__.py
│   │   ├── models
│   │   │   ├── base_model.py
│   │   │   ├── end_2_end_optimization_helper.py
│   │   │   ├── end_2_end_optimization.py
│   │   │   ├── init_guesser.py
│   │   │   ├── __init__.py
│   │   │   ├── loss_surface.py
│   │   │   ├── __pycache__
│   │   │   └── resnet.py
│   │   ├── options
│   │   │   ├── fake_options.py
│   │   │   ├── __init__.py
│   │   │   ├── options_check.py
│   │   │   ├── options.py
│   │   │   ├── options_utils.py
│   │   │   └── __pycache__
│   │   ├── out
│   │   │   ├── pretrained_init_guess
│   │   │   └── pretrained_loss_surface
│   │   ├── __pycache__
│   │   ├── test_end2end.py
│   │   ├── utils
│   │   │   ├── constant_var.py
│   │   │   ├── image_utils.py
│   │   │   ├── __init__.py
│   │   │   ├── metrics.py
│   │   │   ├── __pycache__
│   │   │   ├── util.py
│   │   │   └── warp.py
│   │   ├── video_out
│   │   └── world_cup_data_augmentation
│   │       ├── h5_builder.py
│   │       ├── raw_data_loader.py
│   │       └── soccer_field_template
│   └── teamClassification
│       ├── frame
│       ├── __pycache__
│       ├── team_classification.py
│       └── weights
├── offside.py
├── __pycache__
├── result
└── samples
```

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

## How To Use
If you want to use the gpu to speed up the execution, you have to edit in `model/sportsfield_release/calculateHomography.py` the follow line: 
- In the function `calculateOptimHomography`, set `constant_var.USE_CUDA` to *True*.

## How to run
1. Move to directory where you previously installed the repository
2. Launch 
```sh
python mainGUI.py
```
3. The application makes a prediction on which team is attacking in the picture and marks this team as Team A but the user still can choose which team is attacking beetween Team A and Team B.
4. Video demonstration
   

https://github.com/simolb7/Automatic-Offside-Detection/assets/149960121/0c9ccf2a-8788-42e4-be8c-88198bd99232




