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

