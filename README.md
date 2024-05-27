# MLP Neural Network - Classification
![](Images_repo/classification.png)

## Overview

This project is focused on the development and deployment of a MLP Neural Network for image classification using the [fashionmnist dataset](https://www.kaggle.com/datasets/zalando-research/fashionmnist). The development was done with the hand of the book [Neural Networks from Scratch in Python](https://nnfs.io/) and the deployment was done on a simple web UI developed in Vuejs on wich the user can upload an image or draw a picture to be classify. 

## Architecture
This UI is connected to a Flask server that loads the model and process the image returning the prediction and confidence for the prediction following the next architecture on docker.

![](Images_repo/Architecture.png)

## Docker Setup - Production

To play with the development docker system.

clone this repository. 

```sh
git clone https://github.com/Joancf1997/nnw_fashion_classification.git
cd nnw_fashion_classification
docker-compose up
```

Open the project UI at [Web UI](http://localhost:5173/)




## Python Setup - Development

To play with the neural network code you can download the code and environment of the model. 

clone this repository. 

```sh
git clone https://github.com/Joancf1997/nnw_fashion_classification.git
cd nnw_fashion_classification/model/ml-fashion-classifier/
conda env create --file environment.yml
```

Play with the different training files: 

```sh
python model_training.py    # 128 Neurons
python model_training2.py   # 784 Neurons
python model_training3.py   # 1000 Neurons
```

Use the model to predict: 

```sh
python model_predicting.py  # Same model as production 
```
