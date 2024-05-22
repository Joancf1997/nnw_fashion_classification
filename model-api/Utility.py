import os
import cv2
import urllib 
import numpy as np
import urllib.request 
from zipfile import ZipFile
import matplotlib.pyplot as plt


# Download a MNIST dataset
def download_mnist_dataset():
    print('Downloading dataset completed...')
    URL='https://nnfs.io/datasets/fashion_mnist_images.zip' 
    FILE = 'fashion_mnist_images.zip'
    FOLDER = 'fashion_mnist_images'

    if not os.path.isfile(FILE):
        urllib.request.urlretrieve(URL, FILE)
    
    with ZipFile(FILE) as zip_images: 
        zip_images.extractall(FOLDER)
    print('Dataset downloaded completed...')


# Loads a MNIST dataset Indicating the folder to read
def load_mnist_dataset(dataset, path):
    labels = os.listdir(os.path.join(path, dataset))  #0..9
    X = []
    y = []

    for label in labels:
        for file in os.listdir(os.path.join(path, dataset, label)):
            image = cv2.imread( os.path.join(path, dataset, label, file), cv2.IMREAD_UNCHANGED)  # Read the image
            X.append(image)
            y.append(label)

    return np.array(X), np.array(y).astype('uint8')


# MNIST dataset (train - test)
def create_data_mnist(path):
    # Load both sets separately
    X, y = load_mnist_dataset('train', path)
    X_test, y_test = load_mnist_dataset('test', path)

    return X, y, X_test, y_test


# Preprocess dataset 
def preprocess_dataset(X, X_test, y): 
    # Shuffle the training dataset
    keys = np.array(range(X.shape[0]))
    np.random.shuffle(keys)

    X1 = X[keys]
    y1 = y[keys]

    X1 = (X1.reshape(X1.shape[0], -1).astype(np.float32) - 127.5) / 127.5
    X_test1 = (X_test.reshape(X_test.shape[0], -1).astype(np.float32) - 127.5) / 127.

    return X1, X_test1, y1


#  Pro-process a specific data from the production environment
def preprocess_produnction_image(imgPath):

    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    # plt.imshow(img, cmap='gray')
    # plt.show()


    # Resize to the same size as Fashion MNIST images
    img = cv2.resize(img, (28, 28))

    # Invert image colors
    img = 255 - img

    # plt.imshow(img, cmap='gray')
    # plt.show()

    # plt.imsave('test.png', img, cmap='gray')


    # Reshape and scale pixel data
    return (img.reshape(1, -1).astype(np.float32) - 127.5) / 127.5
