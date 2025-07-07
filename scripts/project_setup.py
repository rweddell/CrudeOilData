"""Summary:
Run this file once Postgres has been installed locally. 

This file will: 
    - Download the  US-Crude-Oil-Imports dataset 
    - Drop/create a table in the public dataset of local postgres
    - Insert the US-Crude-Oil-Imports data into the new table
"""

from os import getenv, listdir, path
import zipfile
import pandas as pd
import psycopg2
from kagglehub import dataset_download



DB_CONFIG = {
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
    "dbname": getenv("DB_NAME"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
}

TABLE_NAME = "us_crude_oil_imports"


def download_and_extract_dataset():
    print("Downloading dataset from Kaggle...")
    path = dataset_download("alistairking/u-s-crude-oil-imports")
    print("Downloaded to:", path)

    for file in listdir(path):
        if file.endswith(".zip"):
            zip_path = path.join(path, file)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(path)
            print(f"Extracted {file}")
    return path

def infer_postgres_type(dtype):
    dtype_mapping = {
        "int64": "INTEGER",
        "float64": "DOUBLE PRECISION",
        "bool": "BOOLEAN",
        "datetime64[ns]": "TIMESTAMP",
        "object": "TEXT",
        "category": "TEXT"
    }
    return dtype_mapping.get(str(dtype), "TEXT")

def drop_and_create_table(conn, table_name, sample_df):
    columns = ['"id" SERIAL PRIMARY KEY']
    for col in sample_df.columns:
        pg_type = infer_postgres_type(sample_df[col].dtype)
        columns.append(f'"{col}" {pg_type}')
    drop_table_query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(columns)}
    );
    """
    with conn.cursor() as cur:
        cur.execute(drop_table_query)
        cur.execute(create_table_query)
        conn.commit()
    print(f"Table '{table_name}' created with inferred column types.")

def load_data_to_postgres(conn, table_name, csv_path):
    df = pd.read_csv(csv_path)
    drop_and_create_table(conn, table_name, df)
    col_str = ', '.join([f'"{col}"' for col in df.columns])
    print(col_str)
    # Load using copy_from (fast for large CSVs)
    with conn.cursor() as cur:
        with open(csv_path, 'r') as f:
            next(f)
            cur.copy_expert(f"COPY {table_name} ({col_str}) FROM STDIN WITH CSV HEADER", f)
        conn.commit()
    print(f"Loaded data into '{table_name}' from '{csv_path}'")

def main():
    dir_path = download_and_extract_dataset()
    csv_file = next((f for f in listdir(dir_path) if f.endswith(".csv")), None)
    if not csv_file:
        raise FileNotFoundError("No CSV file found in downloaded dataset.")
    csv_path = path.join(dir_path, csv_file)
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        load_data_to_postgres(conn, TABLE_NAME, csv_path)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
