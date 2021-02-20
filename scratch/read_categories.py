# read_categories.py file

import yaml

with open(r'categories.yaml') as file:
    documents = yaml.full_load(file)

    for item, doc in documents.items():
        print(item, ":", doc)
