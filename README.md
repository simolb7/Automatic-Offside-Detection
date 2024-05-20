# Automatic-Offside-Detection
Project for the course 'Ai Lab'

# TODO
- sistemare cartelle (spostare football object detection dentro la dir model, rinominare automatic offside recognition gui con solo gui)
- commentare codice
- inserire targhetta giocatori in fuorigioco
- Risaltare giocatori che si intersecano con linea
- Fare read.me completo
- lista requirements

# Download Weights to insert into model/sportsfield_release/out -> https://drive.google.com/drive/folders/1CXyRhw3WUcZj8UItCA0oA9utbg-V-V_2?usp=drive_link
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

