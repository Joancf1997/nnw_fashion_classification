"""
This file contains the activations functions to use on the neural network
"""
import numpy as np

#===== ReLU activation
class Activation_ReLU:

    # Forward pass
    def forward(self, inputs, training):
        self.inputs = inputs                    # Remember inputs
        self.output = np.maximum(0, inputs)     # Output from inputs

    # Backward pass
    def backward(self, dvalues):
        # Zero gradient where input values were negative
        self.dinputs = dvalues.copy()
        self.dinputs[self.inputs <= 0] = 0

    # Calculate predictions for outputs
    def predictions(self, outputs):
        return outputs




#===== Softmax activation
class Activation_Softmax:

    # Forward pass
    def forward(self, inputs, training):
        self.inputs = inputs                                                   # Remember input values
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))    # Get unnormalized probabilities
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True) # Normalize for each sample
        self.output = probabilities

    # Backward pass
    def backward(self, dvalues):
        self.dinputs = np.empty_like(dvalues)         # Create uninitialized array

        # Enumerate outputs and gradients
        for index, (single_output, single_dvalues) in enumerate(zip(self.output, dvalues)):
            single_output = single_output.reshape(-1, 1)            # Flatten output array
            # Calculate Jacobian matrix of the output
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
            # Calculate sample-wise gradient and add it to the array of sample gradients
            self.dinputs[index] = np.dot(jacobian_matrix, single_dvalues)

    # Calculate predictions for outputs
    def predictions(self, outputs):
        return np.argmax(outputs, axis=1)