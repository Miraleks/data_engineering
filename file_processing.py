import yaml
import json
import os
import abc
from functools import wraps
import pandas as pd


def ensure_path_exists(func):
    def wrapper(self, file_path, *args, **kwargs):
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return func(self, file_path, *args, **kwargs)
    return wrapper


# Abstract class
class DataHandler(abc.ABC):
    def __init__(self, data):
        self.data = data  # Data: list, dict or DataFrame

    @abc.abstractmethod
    def create_file(self, file_path):
        pass

    @abc.abstractmethod
    def add_to_file(self, file_path, new_data):
        pass

    @abc.abstractmethod
    def read_file(self, file_path):
        pass


class JSONHandler(DataHandler):
    def __init__(self, data):
        super().__init__(data)

    @ensure_path_exists
    def create_file(self, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    @ensure_path_exists
    def add_to_file(self, file_path, new_data):
        with open(file_path, 'r+') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {}

            self.update_data(existing_data, new_data)

            json_file.seek(0)
            json.dump(existing_data, json_file, indent=4)
            json_file.truncate()

    def update_data(self, existing_data, new_data):
        for key, value in new_data.items():
            if key in existing_data:
                if isinstance(existing_data[key], list):
                    existing_data[key].append(value)
                else:
                    existing_data[key] = [existing_data[key], value]
            else:
                existing_data[key] = value

            for k in existing_data:
                if k != key and existing_data[k] is None:
                    existing_data[k] = None

    def read_file(self, file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)


class YAMLHandler(DataHandler):
    def __init__(self, data):
        super().__init__(data)

    @ensure_path_exists
    def create_file(self, file_path):
        with open(file_path, 'w') as yaml_file:
            yaml.dump(self.data, yaml_file)

    @ensure_path_exists
    def add_to_file(self, file_path, new_data):
        with open(file_path, 'r+') as yaml_file:
            try:
                existing_data = yaml.safe_load(yaml_file)
            except yaml.YAMLError:
                existing_data = []
            if existing_data is None:
                existing_data = []
            existing_data.append(new_data)
            yaml_file.seek(0)
            yaml.dump(existing_data, yaml_file)

    def read_file(self, file_path):
        with open(file_path, 'r') as yaml_file:
            obj = yaml.safe_load(yaml_file)
        return obj


class CSVHandler(DataHandler):
    def __init__(self, data):
        super().__init__(data)  # We expected than data it's a DataFrame

    @ensure_path_exists
    def create_file(self, file_path):
        self.data.to_csv(file_path, index=False)

    @ensure_path_exists
    def add_to_file(self, file_path, new_data):
        new_df = pd.DataFrame([new_data])
        new_df.to_csv(file_path, mode='a', header=False, index=False)

    def read_file(self, file_path):
        df = pd.read_csv(file_path)
        return df

# @ensure_directory_exists
# def create_yaml_file(file_path, data):
#     with open(file_path, "w") as file:
#         documents = yaml.dump(data, file)
#
#
# @ensure_directory_exists
# def read_yaml_file(file_path):
#     with open(file_path, "r") as file:
#         yaml_object = yaml.safe_load(file)
#     return yaml_object
#
#
# @ensure_directory_exists
# def create_json_file(file_path, data):
#     with open(file_path, "w") as file:
#         json.dump(data, file)
#
#
# @ensure_directory_exists
# def read_json_file(file_path):
#     with open(file_path, "r") as file:
#         json_object = json.load(file)
#     return json_object
#
#
# @ensure_directory_exists
# def append_to_json_file(new_data, file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             try:
#                 existing_data = json.load(f)
#             except json.JSONDecodeError:
#                 existing_data = []
#     else:
#         existing_data = []
#
#     if isinstance(existing_data, list):
#         existing_data.append(new_data)
#     else:
#         if isinstance(existing_data, dict) and isinstance(new_data, dict):
#             existing_data.update(new_data)
#         else:
#             raise ValueError("The JSON file must contain a list or dictionary to add data to.")
#     with open(file_path, 'w') as f:
#         json.dump(existing_data, f, indent=4)
#
#
# @ensure_directory_exists
# def create_csv_file(file_path, data):
#     df1 = pd.DataFrame(data)
#     df1.to_csv(file_path, index=False)
#
#
# @ensure_directory_exists
# def read_csv_file(file_path):
#     df = pd.read_csv(file_path)
#     return df


if __name__ == "__main__":
    yaml_file_path = r".\data\store_file.yaml"
    json_file_path = r".\data\store_file.json"
    csv_file_path = r".\data\store_file.csv"

    dict_data_for_yaml = [
        {"countries": ["USA", "Germany", "France", "Poland", "Spain", "Canada"]},
        {"capital": ["Washington", "Berlin", "Paris", "Warsaw", "Madrid", "Ottawa"]},
    ]

    dict_for_json = {"name": "John Smith", "age": 26, "city": "New York", "gender": "male"}

    data_for_csv = [
        {"user_name": "etl_user", "password": "123", "host": "127.0.0.1"},
        {"user_name": "test_user", "password": "456", "host": "127.0.0.2"},
    ]

    # Пример использования:
    json_handler = JSONHandler(dict_for_json)
    json_handler.create_file(json_file_path)
    json_handler.add_to_file(json_file_path, {"name": "Jane", "age": 25, "city": "Boston", "gender": "female"})
    data = json_handler.read_file(json_file_path)
    print(data)

    yaml_handler = YAMLHandler(dict_data_for_yaml)
    yaml_handler.create_file(yaml_file_path)
    yaml_handler.add_to_file(yaml_file_path, {'population': [331000000, 83000000, 67000000, 38000000, 47000000, 38000000]})
    data = yaml_handler.read_file(yaml_file_path)
    print(data)

    csv_handler = CSVHandler(pd.DataFrame(data_for_csv))
    csv_handler.create_file(csv_file_path)
    csv_handler.add_to_file(csv_file_path, {"user_name": "temp_user", "password": "789", "host": "127.0.0.3"})
    data = csv_handler.read_file(csv_file_path)
    print(data)


