import pygame
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
mnist = fetch_openml('mnist_784', version=1)
y =  mnist["target"]
#trandform the file into a list of lists of vectors values
X_vectors=[]
with open("mnist_vectors_normalized.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        if line == lines[0]:
            continue  # Skip header line
        X_vectors.append([int(x) for x in line.strip().split(',')])
X_matrix = np.array(X_vectors)
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
def gradient_descent(weights, inputs, Learning_rate, target, prediction, bias):
    error = target - prediction
    # assuming weights and inputs are numpy arrays
    weights += Learning_rate * error * inputs
    bias += Learning_rate * error
    return weights, bias
def predict(weights, inputs, bias):
    weighted_sum = np.dot(weights, inputs) + bias #np.dot for  product between arrays
    return sigmoid(weighted_sum)
input_size = 308 #i'll just take the value of the vectors
output_size = 10 #digits from 0 to 9
# Initialize weights and bias
weights=np.random.rand(output_size, input_size) * 0.01
biases=np.random.rand(output_size) * 0.01
Learning_rate = 0.01# Here learning rate if i want after to adjust it !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def train_epoch(X, y_true):
    global weights, biases
    total_loss = 0
    total_accuracy = 0
    y_true = np.array(y_true)  # Convert to numpy array
    for i in range(len(X)):#loop through images
        inputs=X[i]
        targets = np.zeros(output_size)
        targets[int(y_true[i])] = 1   
        for digit in range(output_size):
            prediction=predict(weights[digit], inputs, biases[digit])
            weights[digit], biases[digit] = gradient_descent(weights[digit], inputs, Learning_rate, targets[digit], prediction, biases[digit])
            loss = (targets[digit] - prediction) ** 2
            total_loss += loss
        all_predictions = [predict(weights[digit], inputs, biases[digit]) for digit in range(output_size)]
        guessed_digit = np.argmax(all_predictions) # Returns index of max value (e.g., 5)
        if guessed_digit == int(y_true[i]):
            total_accuracy += 1
    return total_loss, total_accuracy
def train_model(epochs):
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        loss, accuracy = train_epoch(X_matrix, y)
        print(f"percentage of Loss: {loss*100/(len(X_matrix)*output_size)}%")
        print(f"percentage of Accuracy: {accuracy*100/(len(X_matrix)*output_size)}%")
    print("Training completed.")
epochs=20
train_model(epochs)
# Save the trained weights and biases to files
np.savetxt("trained_weights.csv", weights, delimiter=",")
np.savetxt("trained_biases.csv", biases, delimiter=",")




            


  


