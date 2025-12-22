import PIL.Image as PIL
import numpy as np
message=input("Enter the message to be encrypted: ")
image_path=input("Enter the path of the image: ")
message_finish="#####"
def process_image(image_path):
    with PIL.open(image_path) as img:
        # Convert image to RGB if not already in that mode
        img = img.convert('RGB')
        #convert image to numpy array
        img_array = np.array(img)
    return img_array
def save_image(image_array, output_path):
    # Convert numpy RGB array back to image and save it
    img = PIL.fromarray(image_array.astype('uint8'), 'RGB')
    img.save(output_path)
def binary_message(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message
def encrypt_image(image_array, message_binary):
    flat_image = image_array.flatten()
    msg_length = len(message_binary)
    if msg_length > len(flat_image):
        raise ValueError("Message is too long to be encrypted in the image.")
    place_for_letter = (len(flat_image))//(msg_length)
    if place_for_letter < 8: 
        raise ValueError("Image too small! Need 8x more pixels than bits.")
    for i in range(0, msg_length, 8):
        first_pixel_index =(i//8)*place_for_letter
        for j in range(8):
            pixel_index = first_pixel_index + j
            flat_image[pixel_index] = (flat_image[pixel_index] & 254) | int(message_binary[i+j])
    encrypted_image = flat_image.reshape(image_array.shape)
    return encrypted_image
def main():
    image_array = process_image(image_path)
    message_with_finish = message + message_finish
    message_binary = binary_message(message_with_finish)
    encrypted_image_array = encrypt_image(image_array, message_binary)
    output_path = "encrypted_image.png"
    save_image(encrypted_image_array, output_path)
    print(f"Message encrypted and saved to {output_path}")
if __name__ == "__main__":
    main()

        
