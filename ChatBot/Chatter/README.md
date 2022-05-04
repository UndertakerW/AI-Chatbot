## Chatter

### Test Requirement
python = 3.10
tensorflow = 2.8
keras = 2.8
nltk = 3.7

### Train Requirement
tensorflow-gpu = 2.8
cuda toolkit = 11.3
cudnn = 8.2 (in conda virtual environment)

## Interface
UI2Chatter() receive the UI input

Chatter2UI(msg) provide output to UI

task_affair() call for affair scheduler

task_email() call for email filter

task_search() call for search online

## test
python test_chatter.py

## train
python train_chatter.py
