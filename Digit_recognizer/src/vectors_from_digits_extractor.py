import pandas as pd
import pygame
from sklearn.datasets import fetch_openml
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist["data"], mnist["target"]
def normalize_data_to_0_255(data):
    # make the pixel value 255 if it's non -zero
    data = data.map(lambda x: 255 if x > 0 else 0)
    return data
X = normalize_data_to_0_255(X)
def get_the_corner_pixel(digit):
    founded=False
    #divide the digit into list of lists 28x28
    digit_2d = digit.values.reshape(28, 28)
    for i in range(28):
        if any(digit_2d[i, :]):
            top_row_index = i
            break
    for i in range(28):
        for line in digit_2d:
            if line[i] != 0:
                left_col_index = i
                founded=True
                break
        if founded:
            break
    # return the coordinates of the corner pixel
    return (top_row_index, left_col_index)
#Function to get the other corner pixel (bottom-right)
def get_the_other_corner_pixel(digit):
    founded=False
    #divide the digit into list of lists 28x28
    digit_2d = digit.values.reshape(28, 28)
    for i in range(27, -1, -1):
        if any(digit_2d[i, :]):
            bottom_row_index = i
            break
    for i in range(27, -1, -1):
        for line in digit_2d:
            if line[i] != 0:
                right_col_index = i
                founded=True
                break
        if founded:
            break
    # return the coordinates of the corner pixel
    return (bottom_row_index, right_col_index)
#Function to get the size of the digit (width * height)
def get_digit_size(digit):
    corner_pixel = get_the_corner_pixel(digit)
    other_corner_pixel = get_the_other_corner_pixel(digit)
    width = other_corner_pixel[1] - corner_pixel[1] + 1
    height = other_corner_pixel[0] - corner_pixel[0] + 1
    return (width*height)
def get_average_digit_size():
    total_size=sum([get_digit_size(X.iloc[i]) for i in range(len(X))])
    average_size=total_size//len(X)
    return average_size
print("The average digit size is:", get_average_digit_size())

# Function to get each vector between each white pixel and the corner pixel
def get_vectors_to_corner(digit):
    corner_pixel = get_the_corner_pixel(digit)
    other_corner_pixel= get_the_other_corner_pixel(digit)
    digit_2d = digit.values.reshape(28, 28)
    #slice the digit_2d to only include the area of the digit
    digit_area = digit_2d[corner_pixel[0]:other_corner_pixel[0]+1, corner_pixel[1]:other_corner_pixel[1]+1]
    vectors = []
    for i in range(digit_area.shape[0]):
        for j in range(digit_area.shape[1]):
            if digit_area[i, j] != 0:
                value=1
            elif digit_area[i, j] == 0:
                value=0
            vector = (i + corner_pixel[0] - corner_pixel[0], j + corner_pixel[1] - corner_pixel[1], value)
            vectors.append(vector)
    return vectors




#after testing, the average is 308
#Plan: i must create a function that normalize all the digits vectors to have the same count of vectors
#if the digit has less vectors than the average, I can repeat some distant by the same length  vectors
#if the digit has more vectors than the average, I can remove some close by the same length vectors
def normalize_vectors_counts(vectors, target_count):
    if not vectors:
        return vectors
    current_count=len(vectors)
    if current_count==target_count:
        return vectors
    elif current_count<target_count:
        #repeat some vectors
        difference=target_count - current_count
        step=current_count//difference
        index=0
        while len(vectors)<target_count:
            vectors.insert(index, vectors[index])
            index=(index+step+1)%len(vectors)
        return vectors
    elif current_count>target_count:
        #remove some vectors
        difference=current_count - target_count
        step=current_count//difference
        index=0
        while len(vectors)>target_count:
            vectors.pop(index)
            index=(index+step)%len(vectors) 
        return vectors
# just a function to visualize
pygame.init()
def draw_digit(screen, digit):
    screen.fill((0, 0, 0))  # Clear the screen with black
    pixel_size = 20  # Size of each pixel block
    for i in range(28):
        for j in range(28):
            pixel_value = digit[i * 28 + j]
            color = (pixel_value, pixel_value, pixel_value)  # Grayscale color
            pygame.draw.rect(screen, color, (j * pixel_size, i * pixel_size, pixel_size, pixel_size))
    corner_pixel = get_the_corner_pixel(pd.Series(digit))
    x, y = corner_pixel[1] * pixel_size, corner_pixel[0] * pixel_size
    pygame.draw.rect(screen, (255, 0, 0), (x, y, pixel_size, pixel_size), 2)  # Draw red border around corner pixel
    #draw all vectors from corner pixel
    vectors = get_vectors_to_corner(pd.Series(digit))
    if len(vectors) == 0:
        print(f"CRITICAL ERROR: Zero vectors found for digit at index {index}")
        print(f"Corner: {get_the_corner_pixel(pd.Series(digit))}")
        print(f"Other Corner: {get_the_other_corner_pixel(pd.Series(digit))}")
    normalised_vectors = normalize_vectors_counts(vectors, 308)
    for vector in normalised_vectors:
        end_x = (corner_pixel[1] + vector[1]) * pixel_size + pixel_size // 2
        end_y = (corner_pixel[0] + vector[0]) * pixel_size + pixel_size // 2
        #diferenciate the color based on the value
        if vector[2]==1:
            pygame.draw.line(screen, (255, 0, 0), (x + pixel_size // 2, y + pixel_size // 2), (end_x, end_y), 1)
            pygame.draw.rect(screen, (0, 255, 0), (end_x - 3, end_y - 3, 6, 6))  # Draw green square at the end of the vector
        else:
            pygame.draw.line(screen, (0, 255, 0), (x + pixel_size // 2, y + pixel_size // 2), (end_x, end_y), 1)
            pygame.draw.rect(screen, (0, 0, 255), (end_x - 3, end_y - 3, 6, 6))  # Draw blue square at the end of the vector
    pygame.display.flip()
screen=pygame.display.set_mode((560, 560))
pygame.display.set_caption("MNIST Digit Display")
running = True
index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                index = (index + 1) % len(X)
            elif event.key == pygame.K_LEFT:
                index = (index - 1) % len(X)
            draw_digit(screen, X.iloc[index].values)
# Plan:
#1.get all the vectors for each digit as a list of lists of tuples
vectors=[get_vectors_to_corner(X.iloc[i]) for i in range(len(X))]
#2.normalize the vectors counts to the average count
normalized_vectors=[normalize_vectors_counts(vectors[i], 308) for i in range(len(vectors))]
#Get just the values from the tuples
final_data=[[ vector[2] for vector in normalized_vectors[i]] for i in range(len(normalized_vectors))]
#export to a csv file
df=pd.DataFrame(final_data)
df.to_csv("mnist_vectors_normalized.csv", index=False)

