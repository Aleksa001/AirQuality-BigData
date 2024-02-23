from service.average_value_per_date import average_value_per_date
from service.get_data_from_openaq import get_data_from_openaq
from service.pm25_foreach_location import pm25_foreach_location
from service.average_value_of_each_polutant_per_date import average_value_per_each_polutant_per_date


base_url = 'https://api.openaq.org/v2/measurements'
params = {
    'country': 'RS',
    'parameter': ['pm25'],
    'limit': 600,
}
headers = {"accept": "application/json"}

if __name__ == '__main__':
    get_data_from_openaq(base_url, params, headers)
    average_value_per_date()
    pm25_foreach_location()
    average_value_per_each_polutant_per_date()