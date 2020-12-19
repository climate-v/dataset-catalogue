import sys
import yaml
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def main():
    yaml_file = sys.argv[1]
    schema = sys.argv[2]
    validate(instance=get_yaml(yaml_file), schema=get_schema(schema))

def get_schema(filename="schema.json"):
    with open(filename, 'r') as file:
        schema = json.load(file)
    return schema

def get_yaml(filename):
    with open(filename, 'r') as file:
        yaml_data = yaml.load(file, yaml.FullLoader)
    return yaml_data

if __name__ == '__main__':
    main()
