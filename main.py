import os
from PIL import Image
import numpy as np

def join_bmp_files(file_path, num_rows):
    files = os.listdir(file_path)
    files.sort(key=lambda x: int(x[4:].split('.')[0]))
    width = Image.open(os.path.join(file_path, files[0])).width
    height = Image.open(os.path.join(file_path, files[0])).height
    final_image = np.zeros((0, 0, 3), dtype=np.uint8)
    row_separator = np.zeros((1, width, 3), dtype=np.uint8)
    column_separator = np.zeros((height * num_rows + num_rows - 1, 1, 3), dtype=np.uint8)
    current_column = np.zeros((0, 0, 3), dtype=np.uint8)
    column = 0
    for filename in files:
        if column % num_rows == 0:
            current_column = Image.open(os.path.join(file_path, filename))
        elif column % num_rows == num_rows - 1:
            current_image = Image.open(os.path.join(file_path, filename))
            current_column = np.vstack((np.vstack((current_column, row_separator)), current_image))
            if column == num_rows - 1:
                final_image = current_column
            else:
                final_image = np.hstack((np.hstack((final_image, column_separator)), current_column))
        else:
            current_image = Image.open(os.path.join(file_path, filename))
            current_column = np.vstack((np.vstack((current_column, row_separator)), current_image))
        column += 1
    Image.fromarray(final_image, "RGB").save("output/" + file_path.split("/")[-1] + ".bmp")
    return 0

def main():
    num_columns = int(input("Write number of columns\n"))
    full_directory = 'resources/'
    output_directory = 'output/'
    if not os.path.isdir(full_directory):
        print("Directory not found")
        return
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for filename in os.listdir(full_directory):
        file_path = os.path.join(full_directory, filename)
        if os.path.isdir(file_path):
            join_bmp_files(file_path, num_columns)


if __name__ == '__main__':
    main()

