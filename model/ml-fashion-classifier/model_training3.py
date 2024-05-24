import nnfs
from Model import Model
from Layer import Layer_Dense
from Optimizers import Optimizer_Adam
from Activations import Activation_ReLU, Activation_Softmax
from Metrics import Loss_CategoricalCrossentropy, Accuracy_Categorical
from Utility import download_mnist_dataset, create_data_mnist, preprocess_dataset


nnfs.init()   # Configuration 



# Download dataset 
download_mnist_dataset()


# Split dataset (train - test)
X, y, X_test, y_test = create_data_mnist('fashion_mnist_images')

# Dataset Pre-processing
X, X_test, y = preprocess_dataset(X, X_test, y)


# Instantiate the model
model = Model(X)

# Initial configuration of the model
model.add(Layer_Dense(X.shape[1], 1000))
model.add(Activation_ReLU())
model.add(Layer_Dense(1000, 1000))
model.add(Activation_ReLU())
model.add(Layer_Dense(1000, 10))
model.add(Activation_Softmax())

# # Set loss, optimizer and accuracy objects
model.set(
    loss=Loss_CategoricalCrossentropy(),
    optimizer=Optimizer_Adam(decay=1e-3),
    accuracy=Accuracy_Categorical()
)

# Finalize the model
model.finalize()

# Train the model
model.train(X, 
            y, 
            validation_data=(X_test, y_test),
            epochs=10, 
            batch_size=128, 
            print_every=100
)

# Training performance - Graphs 
model.step_accuracy_graph()
model.epoc_accuracy_graph()
model.confusion_matrix()

# model.save_parameters('fashion_mnist.parms')
model.save('fashion_mnist2.model')

# Set the parameters of the trained model
model.evaluate(X_test, y_test)


