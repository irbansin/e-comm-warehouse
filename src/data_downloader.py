import kagglehub
import os
from config import DATA_FILES

def download_dataset():
    """Download the e-commerce dataset from Kaggle and return the path"""
    path = kagglehub.dataset_download("abdelrahmanalimo/e-commerce-dataset")
    base_path = path + "/Dataset"
    print("Path to dataset files:", base_path)
    
    # Check files in the path
    data_files = os.listdir(base_path)
    print("Files in dataset:", data_files)
    
    return base_path

def get_full_file_paths(base_path):
    """Get full file paths for all data files"""
    return {
        table_name: f"{base_path}/{file_name}"
        for table_name, file_name in DATA_FILES.items()
    }
