from flask import jsonify
import boto3
import redshift_connector
import pandas as pd
import kagglehub
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()


# Configuration
AWS_ACCESS_KEY = "<your_aws_access_key>"
AWS_SECRET_KEY = "<your_aws_secret_key>"
S3_BUCKET_NAME = "<your_s3_bucket_name>"
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_DB = os.getenv("REDSHIFT_DB")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")
REDSHIFT_PORT = os.getenv("REDSHIFT_PORT")

# Download dataset from Kaggle
path = kagglehub.dataset_download("abdelrahmanalimo/e-commerce-dataset")
path = path + "/Dataset"
print("Path to dataset files:", path)

# Check files in the path
data_files = os.listdir(path)
print("Files in dataset:", data_files)

# Files to upload
DATA_FILES = {
    "customers_dim": f"{path}/Customers.csv",
    "products_dim": f"{path}/Products.csv",
    "sellers_dim": f"{path}/Sellers.csv",
    "categories_dim": f"{path}/Categories.csv",
    "time_dim": f"{path}/Time.csv",  # Ensure this is prepared manually or derived from Orders.csv
    "sales_fact": f"{path}/SalesFact.csv"  # Fact table derived from data
}

# S3 Upload Function
def upload_to_s3(file_name, bucket, object_name=None):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    try:
        s3.upload_file(file_name, bucket, object_name or file_name)
        print(f"Uploaded {file_name} to S3 bucket {bucket}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

# Redshift COPY Function
def copy_to_redshift(table_name, s3_file_path):
    try:
        conn = redshift_connector.connect(
            host=REDSHIFT_HOST,
            database=REDSHIFT_DB,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD,
            port=REDSHIFT_PORT
        )
        cursor = conn.cursor()
        
        copy_query = f"""
        COPY {table_name}
        FROM '{s3_file_path}'
        IAM_ROLE '<your_iam_role_arn>'
        CSV
        IGNOREHEADER 1;
        """

        cursor.execute(copy_query)
        conn.commit()
        print(f"Data loaded into {table_name} from {s3_file_path}")
    except Exception as e:
        print(f"Error loading data into Redshift: {e}")
    finally:
        cursor.close()
        conn.close()

def startETL():
    for table_name, file_path in DATA_FILES.items():
        # Step 1: Upload file to S3
        object_name = f"data/{table_name}.csv"
        upload_to_s3(file_path, S3_BUCKET_NAME, object_name)

        # Step 2: Load data into Redshift
        s3_file_path = f"s3://{S3_BUCKET_NAME}/{object_name}"
        copy_to_redshift(table_name, s3_file_path)

    return True
