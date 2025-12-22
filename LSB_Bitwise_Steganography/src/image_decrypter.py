import PIL.Image as PIL
import numpy as np

picture_path=input("Enter the path of the image: ")
max_message_length=1000
def convert_image_to_array(image_path):
    with PIL.open(image_path) as img:
        img = img.convert('RGB')
        image_array = np.array(img)
    return image_array
def save_image(image_array, output_path):
    img = PIL.fromarray(image_array.astype('uint8'), 'RGB')
    img.save(output_path)
def Extract_LSB(image_array):
    flat_image = image_array.flatten()
    lsb_array = [str(int(pixel) & 1) for pixel in flat_image]
    return ''.join(lsb_array)
def decrpt_image(image_array):
    global max_message_length
    binary_data = Extract_LSB(image_array)
    message=""
    for msg_length in range(1,max_message_length):
        print(f"Cheking for a message in the amplitude of {msg_length}")
        place_for_letter = (len(binary_data))//(msg_length*8)
        if place_for_letter < 8:
            continue
        for pixel_index in range(0, place_for_letter*msg_length, place_for_letter):
            byte = binary_data[pixel_index:pixel_index+8]
            if len(byte) < 8:
                continue
            char = chr(int(byte, 2))
            message += char
        if "#####" in message:
            return message.replace("#####", "")
            break
        else:
            message=""
    return "No hidden message found."
def main():
    image_array = convert_image_to_array(picture_path)
    hidden_message = decrpt_image(image_array)
    print("Hidden message:", hidden_message)
if __name__ == "__main__":
    main()