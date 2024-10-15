import yaml
import json
import os
from functools import wraps


def ensure_directory_exists(func):
    @wraps(func)
    def wrapper(file_path, *args, **kwargs):
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return func(file_path, *args, **kwargs)
    return wrapper


dict_data_for_yaml = [{'countries': ['USA', 'Germany', 'France', 'Poland', 'Spain', 'Canada']},
                      {'capital': ['Washington', 'Berlin', 'Paris', 'Warsaw', 'Madrid', 'Ottawa']}]

dict_for_json = {
    'name': 'John Smith',
    'age': 26,
    'city': 'New York',
    'gender': 'male'
}


@ensure_directory_exists
def create_yaml_file(file_path, data):
    with open(file_path, 'w') as file:
        documents = yaml.dump(data, file)


@ensure_directory_exists
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        yaml_object = yaml.safe_load(file)
    return yaml_object


@ensure_directory_exists
def create_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


@ensure_directory_exists
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_object = json.load(file)
    return json_object


if __name__ == "__main__":
    yaml_file_path = r'.\data\store_file.yaml'
    json_file_path = r'.\data\store_file.json'

    # create_yaml_file(file_path=yaml_file_path, data=dict_data_for_yaml)
    # print(read_yaml_file(yaml_file_path))

    create_json_file(json_file_path, dict_for_json)
    print(read_json_file(json_file_path))
