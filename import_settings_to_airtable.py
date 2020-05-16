import json
import os

from pathlib import Path
from airtable import Airtable

airtables = {
    'iPhone': Airtable(os.getenv('AIRTABLE_BASE_ID'), 'iPhone'),
    'iPad': Airtable(os.getenv('AIRTABLE_BASE_ID'), 'iPhone'),
    'Mac': Airtable(os.getenv('AIRTABLE_BASE_ID'), 'iPhone')
}


def main():
    schemas = {}
    for item in Path('schema').iterdir():
        if item.is_file():
            with open(item) as schema_json_file:
                schema = json.load(schema_json_file)
                schemas[os.path.splitext(item.name)[0]] = schema

    for os_name in schemas:
        airtable = airtables[os_name]
        for item in Path(f'settings/{os_name}').iterdir():
            if item.is_file():
                with open(item) as settings_file:
                    settings = json.load(settings_file)
                    response = airtable.search('App Name', settings['App Name'])
                    if len(response) > 0:  # delete first
                        airtable.delete_by_field('App Name', settings['App Name'])
                    airtable.insert(settings)


if __name__ == "__main__":
    main()
