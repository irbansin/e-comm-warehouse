from dotenv import load_dotenv
import os

load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Redshift Configuration
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_DB = os.getenv("REDSHIFT_DB")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")
REDSHIFT_PORT = os.getenv("REDSHIFT_PORT")

# Data Files Configuration
DATA_FILES = {
    "customers_dim": "Customers.csv",
    "products_dim": "Products.csv",
    "sellers_dim": "Sellers.csv",
    "categories_dim": "Categories.csv",
    "time_dim": "Time.csv",
    "sales_fact": "SalesFact.csv"
}
