"""
Laboratory 3.3
The module for map generating.
"""

import jmespath
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
import oauth2

def get_json_data(nickname:str) -> dict:
    '''
    Gets json dict via Twitter modules.
    '''
    return oauth2.get_endpoint_data(nickname)


def append_coordinates(followers_list:list) -> list:
    '''
    Appends followers' location to the list via geopy.
    '''
    modified_list = []
    geolocator = Nominatim(user_agent='map_generator')
    RateLimiter(geolocator.geocode, min_delay_seconds=0.2)
    for follower in followers_list:
        # THE METHOD GEOLOCATOR.GEOCODE MAY RAISE AN EXEPTION
        try:
            location = geolocator.geocode(follower[2])
        except Exception:
            continue
        # THE METHOD GEOLOCATOR.GEOCODE MAY ALSO RETURN NONE
        if location is None:
            continue
        modified_list.append((follower[0], follower[1],
        location.latitude, location.longitude))
    return modified_list



def get_followers(json_data:dict) -> list:
    '''
    Gets followers' location and forming it list with such tuples:
    (follower_name, follower_location, latitude, longtitude)
    '''
    followers_list = []
    users = jmespath.search('users', json_data)
    if users is None:
        return 404
    for user in users:
        followers_list.append((user['name'], user['screen_name'], user['location']))
    followers_list = followers_list[:17]
    followers_list = append_coordinates(followers_list)
    return followers_list


def get_main_layer() -> object:
    '''
    Returns raw Map object.
    '''
    return folium.Map()


def append_marker_layer(custom_map:object, followers_list:list) -> object:
    '''
    Appends the layer with markers of followers to the custom_map.
    '''
    fg = folium.FeatureGroup(name='follower_locations')
    for elem in followers_list:
        fg.add_child(folium.Marker(location=[elem[2], elem[3]],
        popup=str(elem[0] + ', ' + elem[1]), icon=folium.Icon()))
    custom_map.add_child(fg)
    return custom_map


def generate_map(nickname:str) -> int:
    '''
    The main function to generate a static HTML map.
    '''
    raw_json = get_json_data(nickname)
    #raw_json = json.load(open('data/friends_list_Obama.json', 'r', encoding='utf-8'),
    #cls=None, object_hook=None, parse_float=None, parse_int=None, object_pairs_hook=None)
    if raw_json is None:
        return 404
    custom_map = get_main_layer()
    follower_locations = get_followers(raw_json)
    if follower_locations == 404:
        return 404
    custom_map = append_marker_layer(custom_map, follower_locations)
    custom_map.save('templates/{}custom_map.html'.format(nickname))


if __name__ == '__main__':
    generate_map('@dartydeedsdone')
