import zipfile
import pandas as pd
import psycopg2
from kagglehub import dataset_download
from os import getenv, listdir, getcwd
from os.path import join as path_join


DB_CONFIG = {
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
    "dbname": getenv("DB_NAME"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
}

TABLE_NAME = "us_crude_oil_imports"


def download_and_extract_dataset():
    import shutil

    print("Downloading dataset from Kaggle...")
    dir_path = dataset_download("alistairking/u-s-crude-oil-imports")
    print("Downloaded to:", dir_path)

    extracted_paths = []

    for file in listdir(dir_path):
        if file.endswith(".zip"):
            zip_path = path_join(dir_path, file)
            print(f"Extracting {file} to current working directory...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(getcwd())
                extracted_paths.extend(zip_ref.namelist())
            print(f"Extracted {file}")
    file_path = path_join(getcwd(), file)
    for file in listdir(dir_path):
        if file.endswith(".csv"):
            shutil.copy(path_join(dir_path, file), getcwd())
            print(f"Copied {file} to working directory")
    return file_path 



def infer_postgres_type(dtype):
    mapping = {
        "int64": "INTEGER",
        "float64": "DOUBLE PRECISION",
        "bool": "BOOLEAN",
        "datetime64[ns]": "TIMESTAMP",
        "object": "TEXT",
        "category": "TEXT"
    }
    return mapping.get(str(dtype), "TEXT")


def drop_and_create_table(conn, table_name, sample_df):
    columns = ['"id" SERIAL PRIMARY KEY']
    for col in sample_df.columns:
        pg_type = infer_postgres_type(sample_df[col].dtype)
        columns.append(f'"{col}" {pg_type}')
    drop_query = f"DROP TABLE IF EXISTS {table_name};"
    create_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"

    with conn.cursor() as cur:
        cur.execute(drop_query)
        cur.execute(create_query)
        conn.commit()
    print(f"Table '{table_name}' created.")


def main():
    csv_path = download_and_extract_dataset()
    short_df = pd.read_csv(csv_path, nrows=10)
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        drop_and_create_table(conn, TABLE_NAME, short_df)
    finally:
        conn.close()
    print(f"Dataset ready and table created. CSV located at: {csv_path}")


if __name__ == "__main__":
    main()