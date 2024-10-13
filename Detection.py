import os
import hashlib
from collections import defaultdict

def find_duplicates_by_size(directory):
    """
    Find and group files with the same size to optimize the duplicate detection process.

    Args:
    directory (str): The path of the directory to scan.

    Returns:
    dict: A dictionary where the key is the file size, and the value is a list of file paths with that size.
    """
    size_dict = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                size_dict[file_size].append(file_path)
            except OSError as e:
                print(f"Error accessing {file_path}: {e}")
    
    # Filter out unique sizes (i.e., no duplicates in size)
    size_dict = {size: paths for size, paths in size_dict.items() if len(paths) > 1}
    
    return size_dict

def hash_file(file_path, block_size=65536):
    """
    Generate a hash for a given file.

    Args:
    file_path (str): The path of the file to hash.
    block_size (int): Size of each block for reading the file.

    Returns:
    str: The hash of the file content.
    """
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read(block_size)
            while buf:
                hasher.update(buf)
                buf = f.read(block_size)
    except OSError as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
    return hasher.hexdigest()

def find_duplicates_by_hash(size_dict):
    """
    Compare files of the same size by hashing their contents to detect duplicates.

    Args:
    size_dict (dict): A dictionary where the key is the file size, and the value is a list of file paths.

    Returns:
    dict: A dictionary where the key is the file hash, and the value is a list of duplicate file paths.
    """
    hash_dict = defaultdict(list)

    for file_list in size_dict.values():
        for file_path in file_list:
            file_hash = hash_file(file_path)
            if file_hash:
                hash_dict[file_hash].append(file_path)
    
    # Filter out unique hashes (i.e., no duplicates in content)
    hash_dict = {file_hash: paths for file_hash, paths in hash_dict.items() if len(paths) > 1}

    return hash_dict

def display_duplicates(duplicate_dict):
    """
    Display the detected duplicate files.

    Args:
    duplicate_dict (dict): A dictionary where the key is the file hash, and the value is a list of duplicate file paths.
    """
    for file_hash, file_paths in duplicate_dict.items():
        print(f"\nDuplicate files with hash {file_hash}:")
        for file_path in file_paths:
            print(f"  {file_path}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory path to scan for duplicates: ")

    # Step 1: Find files with the same size
    size_duplicates = find_duplicates_by_size(directory_to_scan)
    if not size_duplicates:
        print("No duplicate files found based on size.")
    else:
        # Step 2: Compare files with the same size by their content (hash)
        content_duplicates = find_duplicates_by_hash(size_duplicates)
        if not content_duplicates:
            print("No duplicate files found based on content.")
        else:
            display_duplicates(content_duplicates)
