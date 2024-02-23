from configuration.configuration import get_database_airqualityserbia
import requests

collection = get_database_airqualityserbia()


def get_data_from_openaq(url, parameters, headers):
    response = requests.get(url, params=parameters, headers=headers)
    if response.status_code == 200:
        air_quality_data = response.json()['results']

        collection.insert_many(air_quality_data)
        print(air_quality_data)
        print(f"Stored {len(air_quality_data)} records.")

        # Provera da li ima jos stranica
        meta = response.json()['meta']
        if 'next' in meta:
            next_url = meta['next']
            get_data_from_openaq(next_url, parameters, headers)
        else:
            print("All data fetched.")
    else:
        print(f"Failed to fetch data from OpenAQ API. Error: {response.text}")
