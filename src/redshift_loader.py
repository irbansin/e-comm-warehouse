from dotenv import load_dotenv
import redshift_connector
from config import (
    REDSHIFT_HOST,
    REDSHIFT_DB,
    REDSHIFT_USER,
    REDSHIFT_PASSWORD,
    REDSHIFT_PORT
)

load_dotenv()

# AWS Configuration
IAM_ARN = os.getenv("IAM_ARN")

def copy_to_redshift(table_name, s3_file_path):
    """Copy data from S3 to Redshift table"""
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
        IAM_ROLE '{IAM_ARN}'
        CSV
        IGNOREHEADER 1;
        """

        cursor.execute(copy_query)
        conn.commit()
        print(f"Data loaded into {table_name} from {s3_file_path}")
        return True
        
    except Exception as e:
        print(f"Error loading data into Redshift: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
