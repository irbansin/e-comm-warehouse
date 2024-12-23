from data_downloader import download_dataset, get_full_file_paths
from s3_uploader import upload_to_s3
from redshift_loader import copy_to_redshift
from config import S3_BUCKET_NAME

def start_etl():
    """Orchestrate the entire ETL process"""
    try:
        # Step 1: Download dataset
        base_path = download_dataset()
        data_files = get_full_file_paths(base_path)
        
        # Step 2: Process each table
        for table_name, file_path in data_files.items():
            # Upload to S3
            object_name = f"data/{table_name}.csv"
            if not upload_to_s3(file_path, S3_BUCKET_NAME, object_name):
                print(f"Failed to upload {table_name} to S3")
                continue

            # Load to Redshift
            s3_file_path = f"s3://{S3_BUCKET_NAME}/{object_name}"
            if not copy_to_redshift(table_name, s3_file_path):
                print(f"Failed to load {table_name} to Redshift")
                continue
                
            print(f"Successfully processed {table_name}")
            
        return True
        
    except Exception as e:
        print(f"ETL process failed: {e}")
        return False

if __name__ == "__main__":
    start_etl()
