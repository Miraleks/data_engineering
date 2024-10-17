import yaml
import json
import os
from functools import wraps
import pandas as pd


def ensure_directory_exists(func):
    @wraps(func)
    def wrapper(file_path, *args, **kwargs):
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return func(file_path, *args, **kwargs)

    return wrapper


dict_data_for_yaml = [
    {"countries": ["USA", "Germany", "France", "Poland", "Spain", "Canada"]},
    {"capital": ["Washington", "Berlin", "Paris", "Warsaw", "Madrid", "Ottawa"]},
]

dict_for_json = {"name": "John Smith", "age": 26, "city": "New York", "gender": "male"}

data_for_csv = [
    {"user_name": "etl_user", "password": "123", "host": "127.0.0.1"},
    {"user_name": "test_user", "password": "456", "host": "127.0.0.2"},
]


@ensure_directory_exists
def create_yaml_file(file_path, data):
    with open(file_path, "w") as file:
        documents = yaml.dump(data, file)


@ensure_directory_exists
def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        yaml_object = yaml.safe_load(file)
    return yaml_object


@ensure_directory_exists
def create_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)


@ensure_directory_exists
def read_json_file(file_path):
    with open(file_path, "r") as file:
        json_object = json.load(file)
    return json_object


@ensure_directory_exists
def append_to_json_file(new_data, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    if isinstance(existing_data, list):
        existing_data.append(new_data)
    else:
        if isinstance(existing_data, dict) and isinstance(new_data, dict):
            existing_data.update(new_data)
        else:
            raise ValueError("The JSON file must contain a list or dictionary to add data to.")
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)


@ensure_directory_exists
def create_csv_file(file_path, data):
    df1 = pd.DataFrame(data)
    df1.to_csv(file_path, index=False)


@ensure_directory_exists
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    yaml_file_path = r".\data\store_file.yaml"
    json_file_path = r".\data\store_file.json"
    csv_file_path = r".\data\store_file.csv"

    # create_yaml_file(file_path=yaml_file_path, data=dict_data_for_yaml)
    # print(read_yaml_file(yaml_file_path))
    #
    # create_json_file(json_file_path, dict_for_json)
    # print(read_json_file(json_file_path))
    #
    # create_csv_file(csv_file_path, data_for_csv)
    # print(read_csv_file(csv_file_path))

    append_json_file(json_file_path, dict_for_json)
