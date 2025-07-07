import pandas as pd
import requests
from os import listdir, getcwd
from os.path import join as path_join

CREATION_ENDPOINT = "http://localhost:8000/imports"


CSV_FILE = next((f for f in listdir(getcwd()) if f.endswith(".csv")), None)


def send_data_to_api(csv_path):
    df = pd.read_csv(csv_path)
    print(f"Sending {len(df)} rows to API at {CREATION_ENDPOINT}...")
    for i, row in df.iterrows():
        record = row.to_dict()
        try:
            response = requests.post(CREATION_ENDPOINT, json=record)
            if response.status_code not in (200, 201):
                print(f"[{i}] Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[{i}] Request error: {e}")
    print("Finished sending data.")


def main():
    if not CSV_FILE:
        raise FileNotFoundError("No CSV file found in dataset directory.")
    csv_path = path_join(getcwd(), CSV_FILE)
    send_data_to_api(csv_path)


if __name__ == "__main__":
    main()