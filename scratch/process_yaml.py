# process_yaml.py file

import yaml

with open(r'fruits.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    fruits_list = yaml.load(file, Loader=yaml.FullLoader)

    print(fruits_list)

    sort_file = yaml.dump(fruits_list, sort_keys=True)
    print(sort_file)
