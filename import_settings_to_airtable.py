import json
import os

from pathlib import Path
from airtable import Airtable

PRIMARY_FIELD_NAME = 'App Name'
GITHUB_BASE_URL = 'https://github.com/tianrunhe/app-settings/commits/master/settings'
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
                    app_name = settings[PRIMARY_FIELD_NAME]
                    settings['Change History'] = f'{GITHUB_BASE_URL}/{os_name}/{app_name}.json'
                    response = airtable.search(PRIMARY_FIELD_NAME, settings[PRIMARY_FIELD_NAME])
                    if len(response) > 0:  # delete first
                        airtable.delete_by_field(PRIMARY_FIELD_NAME, settings[PRIMARY_FIELD_NAME])
                    airtable.insert(settings)


if __name__ == "__main__":
    main()
