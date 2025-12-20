import pygame
import numpy as np
#extract weights and biases from trained model
with open("trained_weights.csv", "r") as f:
    weights_lines = f.readlines()
    weights = []
    for line in weights_lines:
        weights.append([float(x) for x in line.strip().split(',')])
weights = np.array(weights)
with open("trained_biases.csv", "r") as f:
    biases_lines = f.readlines()
    biases = [float(line.strip()) for line in biases_lines]
biases = np.array(biases)
def sigmoid(x):
    return 1 / (1 + np.exp(np.clip(-x, -500, 500)))
def predict(vectors):
    probabilities=np.zeros((10,))
    for layer in range(len(weights)):
        probability=np.dot(weights[layer],vectors)+biases[layer]
        probabilities[layer]=sigmoid(probability)
    guess=np.argmax(probabilities)
    return guess
def get_the_corner_pixel(digit):
    founded=False
    
    digit_2d = digit.reshape(28, 28)
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
    
    digit_2d = digit.reshape(28, 28)
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


# Function to get each vector between each white pixel and the corner pixel
def get_vectors_to_corner(digit):
    corner_pixel = get_the_corner_pixel(digit)
    other_corner_pixel= get_the_other_corner_pixel(digit)
    digit_2d = digit.reshape(28, 28)
    #slice the digit_2d to only include the area of the digit
    digit_area = digit_2d[corner_pixel[0]:other_corner_pixel[0]+1, corner_pixel[1]:other_corner_pixel[1]+1]
    height, width = digit_area.shape
    vectors = []
    for i in range(digit_area.shape[0]):
        for j in range(digit_area.shape[1]):
            if digit_area[i, j] != 0:
                value=1
            elif digit_area[i, j] == 0:
                value=0
            vector = (i + corner_pixel[0] - corner_pixel[0], j + corner_pixel[1] - corner_pixel[1], value)
            vectors.append(vector)
    #dividethe vectors into lists of lines
    vectors=[vectors[i*width:(i+1)*width] for i in range(height)]
    return vectors



def normalize_vectors_counts(vectors, target_count):
    height = len(vectors)
    wanted_width_per_line = target_count // height if height > 0 else 0
    rest_to_add = target_count - (wanted_width_per_line * height)
    if height == 0:
        return vectors
    if not vectors:
        return vectors
    current_count=sum(len(line) for line in vectors)
    if current_count==target_count:
        return vectors
    for line in range(height):
        current_line_length = len(vectors[line])
        if current_line_length < wanted_width_per_line:
            difference = wanted_width_per_line - current_line_length
            step = current_line_length // difference if difference != 0 else 1
            index = 0
            while len(vectors[line]) < wanted_width_per_line:
                vectors[line].insert(index, vectors[line][index])
                index = (index + step + 1) % len(vectors[line])
        elif current_line_length > wanted_width_per_line:
            difference = current_line_length - wanted_width_per_line
            step = current_line_length // difference if difference != 0 else 1
            index = 0
            while len(vectors[line]) > wanted_width_per_line:
                vectors[line].pop(index)
                index = (index + step) % len(vectors[line])
    
    # Distribute the rest_to_add across first few lines
    for line in range(rest_to_add):
        current_line_length = len(vectors[line])
        if current_line_length < target_count:
            vectors[line].append(vectors[line][-1])  # Repeat the last vector for simplicity
    
    # Flatten the list of lists back into a single list
    flattened_vectors = [vector for line in vectors for vector in line]
    return flattened_vectors
    
#function to draw a 28x28 grid and get the digit drawn by the user
def get_the_digit_from_user():
    pygame.init()
    screen = pygame.display.set_mode((280, 280))
    pygame.display.set_caption("Draw a digit (0-9) and press Enter")
    clock = pygame.time.Clock()
    drawing = False
    grid = np.zeros((28, 28))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    return grid.flatten()
        if drawing:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // 10
            grid_y = mouse_y // 10
            if 0 <= grid_x < 28 and 0 <= grid_y < 28:
                grid[grid_y, grid_x] = 1.0
                #add adjacent pixels for better matching MPSI data
                if grid_x+1 < 28: grid[grid_y, grid_x+1] = 1.0
                if grid_y+1 < 28: grid[grid_y+1, grid_x] = 1.0
                if grid_x+1 < 28 and grid_y+1 < 28: grid[grid_y+1, grid_x+1] = 1.0
        screen.fill((0, 0, 0))
        for y in range(28):
            for x in range(28):
                if grid[y, x] > 0:
                    pygame.draw.rect(screen, (255, 255, 255), (x * 10, y * 10, 10, 10))
        pygame.display.flip()
        clock.tick(60)
# Main loop to get the digit and predict
if __name__ == "__main__":
    digit = get_the_digit_from_user()
    if digit is not None:
        vectors = get_vectors_to_corner(digit)
        target_vector_count =  308  # The average number of vectors in the training set(do not change this value)
        normalized_vectors = normalize_vectors_counts(vectors, target_vector_count)
        # Flatten the vectors for prediction
        input_vector = np.array([vector[2] for vector in normalized_vectors])
        prediction = predict(input_vector)
        print(f"The predicted digit is: {prediction}")

    
