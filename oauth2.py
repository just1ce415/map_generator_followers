"""
Laboratory 3.3
The module for creating a request to friends_list endpoint and getting data.
"""

import requests

BASE_URL = 'https://api.twitter.com/1.1/friends/list.json'
ACCESS_TOKEN = 'Bearer'   # MY TOKEN WAS HERE

def get_endpoint_data(nickname:str) -> dict:
    '''
    The main function - gets friends-endpoint data in json format.
    '''
    search_headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
    }
    search_params = {
        'screen_name': nickname
    }
    response = requests.get(BASE_URL, headers=search_headers, params=search_params)
    json_response = response.json()
    return json_response


if __name__ == '__main__':
    get_endpoint_data('@dartydeedsdone')
