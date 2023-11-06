# Deep Learning Vocal Separator

This project hosts a neural network specifically trained to separate vocal and instrumental tracks from songs by Post Malone. The architecture is the work of github user: tsurumeso and has been trained with a dataset consisting solely of Post Malone songs, due to time constraints. It was trained for 36 epochs spanned across ~26 hours. It was developed as part of a TigerHacks hackathon project, and due to the targeted nature of its training and time constraints, it performs optimally on Post Malone tracks.

## Prerequisites

Before running this application, please refer to `requirements.txt` for a list of prerequisites.

## Installation

1. Download the zip of the vocal remover repo
2. Export it to some directory on your computer
3. Open a terminal and perform the following commands:
```bash
cd your\dir\to\vocal-remover
pip install -r requirements.txt
```
4. Models must be downloaded separately and replaced in directory due to GitHub's downloading constraints

## Usage

1. Open the folder directory in some code editor
2. Run the "programgui.py" script
3. Select your desired .wav file input to split
4. Select your desired output folder to save the files to

For the rest of the options:

### Model

This selection is for selecting the desired trained model to run inference with.
The names represent the different stages in which the model was saved at.

0.0 represents the first completed epoch's result
0.5 represents the middle completed epoch's result
1.0 represents the final best completed epoch's result

### Use GPU

This selection is to choose whether or not to use gpu for inference
If you have a pytorch version that supports cuda, you can select this (DO NOT PIP INSTALL TORCH AGAIN IF YOU HAVE THE CUDA VERSION)

### Processing Options

This selection is for selecting whether or not you want to process the input data further to possibly increase accuracy.

#### Postprocess

Masks instrumental part based on the vocals volume to improve the separation quality (NOT WORKING)

#### Test-Time-Augmentation

Improves the performance of machine learning models on unseen data by applying various augmentations, like rotations or flips, to the test data. The model makes predictions on each augmented version of the data, and these predictions are then combined, often by averaging, to produce a final prediction. This often produces a better result.

## Demonstration

[![Demonstration](https://img.youtube.com/vi/q3MoDmhh2UE&ab/0.jpg)](https://www.youtube.com/watch?v=q3MoDmhh2UE&ab)

## References

1. https://github.com/tsurumeso/vocal-remover
