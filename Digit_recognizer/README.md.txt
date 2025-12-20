# 🧠 Interactive Digit Recognizer (Built from Scratch)

## 📌 Overview
	A real-time handwritten digit recognizer built from first principles. By eschewing high-level frameworks like TensorFlow or PyTorch in favor of raw NumPy,
	 this project demonstrates the foundational mathematics of Deep Learning (Matrix Multiplication, Forward Propagation, and Gradient Descent) without abstraction.
	It features a responsive Pygame Interface, allowing users to draw digits on a digital canvas and visualize the model's predictions instantly.

## 🚀 Key Features
* 	**No ML Frameworks:		** The Neural Network logic (Forward/Backward propagation, Activation functions) is implemented using raw Linear Algebra.
*	**Interactive GUI:		** Built with `pygame` to allow real-time drawing and testing.
* 	**Pre-Trained Model:		** Includes `trained_weights.csv` and `trained_biases.csv` so the application works immediately without retraining.
* 	**Geometric Feature Engineering:** Implements a custom vector extraction algorithm that prioritizes geometric structure over raw pixel density.
	 				 By calculating vectors from the digit's corners, the model learns spatial relationships (strokes and angles) directly, 
					 demonstrating a novel approach to feature preprocessing.

## 🛠️ Tech Stack
* 	**Language:** Python 3.x
* 	**Interface:** Pygame
* 	**Computation:** NumPy, Pandas
* 	**Data Source:** MNIST (Fetched via Scikit-Learn)

## 📂 Project Structure
	| File 					| Description 										    |
	______________________________________________________________________________________________________________________________________
	| :--- 					| :---											    |
	| **`digit_recognizer_test.py`** 	| **Start Here.** The main GUI application. Run this to draw and test the AI. 		    |
	| `Digit_recognizer_vectors.py`         | The **Trainer**. Fetches MNIST data, trains the network, and saves weights/biases to CSV. |
	| `vectors_from_digits_extractor.py`    | Helper utility to convert Pygame grid pixels into normalized vectors. 		    |
	| `trained_weights.csv`                 | The "Brain" of the model (Matrices). 							    |
	| `trained_biases.csv`                  | The learned biases for the network. 							    |

## 💻 How to Run

	### 1. Install Dependencies
	Ensure you have Python installed, then run:
	```bash
	pip install -r requirements.txt

	### 2. Launch the App (Inference Mode)
	To use the recognizer immediately:
	```bash
	python digit_recognizer_test.py

	Controls: Left Click to Draw, Right Click (or defined key) to Clear.
	Output: The prediction will appear in the console/window title.

	### 3. Retrain the Network (Optional)
	If you want to experiment with the learning rate or epochs:
	```bash
	python Digit_recognizer_vectors.py

	Note: This will overwrite the existing CSV weight files.

## 🧠 Theory & Logic
	This project demonstrates the fundamental math behind Deep Learning:

	1.Input Layer: 784 nodes (representing a 28x28 pixel grid).
	2.Hidden Layers: Uses ReLu/Sigmoid activation functions.
	3.Output Layer: 10 nodes (probabilities for digits 0-9)
	4.Math: Uses Matrix Multiplication (Dot Product) for signal propagation.

## 📜 License
	This project is open-source. Feel free to fork and improve!
