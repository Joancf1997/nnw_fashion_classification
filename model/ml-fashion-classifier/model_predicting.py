import cv2
import nnfs
from Model import Model
from Utility import preprocess_produnction_image

# Read an image
# image = preprocess_produnction_image('../production_images/sneaker-not_filled.png')

fashion_mnist_labels = {
    0: 'T-shirt/top',
    1: 'Trouser',
    2: 'Pullover',
    3: 'Dress',
    4: 'Coat',
    5: 'Sandal',
    6: 'Shirt',
    7: 'Sneaker',
    8: 'Bag',
    9: 'Ankle boot'
}

model = Model.load('fashion_mnist.model')
confidences = model.predict(image)
predictions = model.output_layer_activation.predictions(confidences)
prediction_label = fashion_mnist_labels[predictions[0]]
print(prediction_label)