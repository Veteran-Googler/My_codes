# 🛡️ LSB Bitwise Steganography

## Overview
	A lightweight, low-level steganography tool that hides secret text messages inside PNG images using **Least Significant Bit (LSB)** manipulation. 
	Unlike high-level libraries that abstract the process, this project manually handles binary arithmetic (`pixel & 254 | bit`) to embed data directly into the RGB channels of an image. 
	It features a custom **Brute-Force Decryption Algorithm** that automatically detects message length without requiring a shared key.

## 🛠️ Technical Highlights
* 	**Bitwise Operations:** Uses raw binary masking to modify pixel values with minimal visual distortion.
* 	**Lossless Encryption:** Forces `.png` output to prevent compression artifacts from corrupting the hidden bits.
* 	**Algorithmic Decryption:** Solves the "Circular Dependency" problem (receiver needing message length to read the message) by scanning the image spectrum until a valid termination flag (`#####`) is found.

## 🚀 How to Run

	### 1. Install Dependencies
		```bash
		pip install -r requirements.txt

	### 2. Encrypt a Message
		```bash
		python src/encryptor.py

		Input: Path to source image + Secret Message.
		Output: Generates encrypted_image.png.

	### 3. Decrypt a Message
		```bash
		python src/decryptor.py

		Input: Path to encrypted_image.png.
		Output: Prints the hidden text if found.

## 🧠 How it Works
	Encoding: Converting text to 8-bit binary strings (ASCII).
	Embedding: Iterating through the image array, replacing the last bit of selected pixels with message bits.
	Spacing: Distributing bits evenly across the image to maximize stealth (Variable Stride).

## ⚠️ Disclaimer
	This tool is for educational purposes and demonstrates the fundamentals of digital data hiding.