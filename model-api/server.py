import os
import cv2
import nnfs
from Model import Model
from flask_cors import CORS
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from Utility import preprocess_produnction_image

# Create a Flask app
app = Flask(__name__)
CORS(app)

# Model inicialization
model = Model.load('fashion_mnist.model')

# Define the /predictions route
@app.route('/predictions', methods=['POST'])
def get_predictions():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  file = request.files['file']
  filename = secure_filename(file.filename)
  file_path = os.path.join(os.getcwd(), filename)
  file.save(file_path)

  # Read an image
  image = preprocess_produnction_image(file_path)

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

  confidences = model.predict(image)
  predictions = model.output_layer_activation.predictions(confidences)
  prediction_label = fashion_mnist_labels[predictions[0]]
  return jsonify({
    'prediction': prediction_label,
    'confidence': round(max(confidences[0]) * 100, 2)
  })



# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
