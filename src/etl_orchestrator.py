from data_downloader import download_dataset, get_full_file_paths
from s3_uploader import upload_to_s3
from redshift_loader import copy_to_redshift
from config import S3_BUCKET_NAME

def start_etl():
    """Orchestrate the entire ETL process"""
    try:
        print("Starting ETL process...")
        
        # Step 1: Download dataset
        print("Step 1: Downloading dataset...")
        base_path = download_dataset()
        if not base_path:
            raise Exception("Failed to download dataset")
        
        print(f"Dataset downloaded to: {base_path}")
        data_files = get_full_file_paths(base_path)
        print(f"Found data files: {data_files}")
        
        # Step 2: Process each table
        for table_name, file_path in data_files.items():
            print(f"\nProcessing table: {table_name}")
            print(f"Source file: {file_path}")
            
            # Upload to S3
            object_name = f"data/{table_name}.csv"
            print(f"Uploading to S3: {object_name}")
            if not upload_to_s3(file_path, S3_BUCKET_NAME, object_name):
                print(f"ERROR: Failed to upload {table_name} to S3")
                continue

            # Load to Redshift
            s3_file_path = f"s3://{S3_BUCKET_NAME}/{object_name}"
            print(f"Loading to Redshift from: {s3_file_path}")
            if not copy_to_redshift(table_name, s3_file_path):
                print(f"ERROR: Failed to load {table_name} to Redshift")
                continue
                
            print(f"Successfully processed {table_name}")
            
        print("\nETL process completed successfully!")
        return True
        
    except Exception as e:
        print(f"ETL process failed with error: {str(e)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    start_etl()
