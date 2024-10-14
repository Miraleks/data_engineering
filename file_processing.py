import yaml

dict_data = [{'countries': ['USA', 'Germany', 'France', 'Poland', 'Spain', 'Canada']},
             {'capital': ['Washington', 'Berlin', 'Paris', 'Warsaw', 'Madrid', 'Ottawa']}]


def create_yaml_file(data, file_name):
    with open(file_name, 'w') as file:
        documents = yaml.dump(data, file)


def read_yaml_file():
    pass


def create_json_file():
    pass


def read_json_file():
    pass


if __name__ == "__main__":
    file_name = r'.\data\store_file.yaml'

    create_yaml_file(data=dict_data, file_name=file_name)
