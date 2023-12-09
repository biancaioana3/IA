import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

file_path = r"C:\Users\bianc\Desktop\materiale facultate\IIIA3\IA\laborator\lab_6\seeds_dataset.txt"
column_names = ["area", "perimeter", "compactness", "length_of_kernel", "width_of_kernel", "asymmetry_coefficient",
                "length_of_kernel_groove", "class"]
data = pd.read_csv(file_path, delimiter='\s+', header=None, names=column_names)

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

print("Train Data:")
print(train_data.to_string())

print("\nTest Data:")
print(test_data.to_string())

input_size = 7
hidden_size = 5
output_size = 3
learning_rate = 0.01
max_epochs = 1000

weights_input_hidden = np.random.uniform(size=(input_size, hidden_size))
weights_hidden_output = np.random.uniform(size=(hidden_size, output_size))
