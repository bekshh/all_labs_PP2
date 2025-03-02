#TASK1
import os

def list_directories(path):
    """List only directories in the specified path"""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path):
    """List only files in the specified path"""
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def list_all(path):
    """List all directories and files in the specified path"""
    return os.listdir(path)

if __name__ == "__main__":
    path = input("Enter the path: ")
    if os.path.exists(path):
        print("Directories:", list_directories(path))
        print("Files:", list_files(path))
        print("All items:", list_all(path))
    else:
        print("The specified path does not exist.")

#TASK2
import os

def list_directories(path):
    """List only directories in the specified path"""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path):
    """List only files in the specified path"""
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def list_all(path):
    """List all directories and files in the specified path"""
    return os.listdir(path)

def check_access(path):
    """Check access permissions for the specified path"""
    return {
        "Exists": os.path.exists(path),
        "Readable": os.access(path, os.R_OK),
        "Writable": os.access(path, os.W_OK),
        "Executable": os.access(path, os.X_OK)
    }

if __name__ == "__main__":
    path = input("Enter the path: ")
    if os.path.exists(path):
        print("Directories:", list_directories(path))
        print("Files:", list_files(path))
        print("All items:", list_all(path))
        print("Access permissions:", check_access(path))
    else:
        print("The specified path does not exist.")
#TASK3
import os

def check_path(path):
    if os.path.exists(path):
        print(f"The path '{path}' exists.")
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        print(f"Directory: {directory}")
        print(f"Filename: {filename}")
    else:
        print(f"The path '{path}' does not exist.")

# Example usage
path = input("Enter a file or directory path: ")
check_path(path)
#TASK4
def count_lines(filename):
    try:
        with open(filename, 'r') as file:
            line_count = sum(1 for line in file)
        print(f"The file '{filename}' contains {line_count} lines.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
filename = 'example.txt'  # Replace with your file name
count_lines(filename)
#TASK5
def write_list_to_file(filename, data_list):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for item in data_list:
                file.write(f"{item}\n")
        print(f"List successfully written to {filename}.")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Example usage
data = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
filename = input("Enter the filename to save the list: ")
write_list_to_file(filename, data)
#TASK6
import string

def generate_text_files():
    for letter in string.ascii_uppercase:
        filename = f"{letter}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"This is file {filename}\n")
            print(f"Created {filename}")
        except Exception as e:
            print(f"Error creating {filename}: {e}")

# Generate 26 text files
generate_text_files()
#TASK7
# Function to copy the contents of a file to another file
def copy_file(source_file, destination_file):
    try:
        # Open source file in read mode and destination file in write mode
        with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
            # Read contents from source file and write to destination file
            dest.write(src.read())
        print(f"Contents copied from {source_file} to {destination_file} successfully.")
    except FileNotFoundError:
        print("Error: Source file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
source = "source.txt"  # Replace with your source file
destination = "destination.txt"  # Replace with your destination file
copy_file(source, destination)
#TASK8
import os

def delete_file(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print("Error: File does not exist.")
            return
        
        # Check if the file is accessible
        if not os.access(file_path, os.W_OK):
            print("Error: No write permission to delete the file.")
            return
        
        # Delete the file
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_to_delete = "test.txt"  # Replace with your file path
delete_file(file_to_delete)
