import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import requests
import io

# Load environment variables
load_dotenv()

def download_csv(url):
    """
    Download CSV file from a given URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def create_raw_schema_and_tables():
    """
    Create RAW schema and load datasets
    """
    # Database connection parameters
    db_params = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT', '5432')
    }


    # Create SQLAlchemy engine for pandas to_sql method
    engine_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    engine = create_engine(engine_string)

    # Establish psycopg2 connection for schema creation
    try:
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cur = conn.cursor()

        # Create RAW schema
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
        print("RAW schema created successfully.")

        # Close cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating RAW schema: {e}")
        return

    # URLs of datasets
    datasets = {
        'hosts': 'https://dbtlearn.s3.amazonaws.com/hosts.csv',
        'reviews': 'https://dbtlearn.s3.amazonaws.com/reviews.csv', 
        'listings': 'https://dbtlearn.s3.amazonaws.com/listings.csv'
    }

    # Download and load each dataset
    for table_name, url in datasets.items():
        try:
            # Download CSV
            df = download_csv(url)
            
            if df is not None:
                # Load to PostgreSQL in RAW schema
                df.to_sql(
                    name=table_name, 
                    schema='raw', 
                    con=engine, 
                    if_exists='replace',  # Replace existing table
                    index=False  # Don't write index as a column
                )
                print(f"Loaded {table_name} into RAW schema successfully.")
                print(f"Rows in {table_name}: {len(df)}")
        except Exception as e:
            print(f"Error loading {table_name}: {e}")

def main():
    create_raw_schema_and_tables()

if __name__ == "__main__":
    main()