import requests
import TMDB_api_key

API_KEY = TMDB_api_key.API_KEY

def get_id(name):

    url = f'https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&language=en-US&page=1&query={name}'
    response = requests.get(url)
    json = response.json()
    if json['results']:
        id = json['results'][0]['id']
        return id



def fetcher(name):
    id = get_id(name)
    if id:
        url = f'https://api.themoviedb.org/3/tv/{id}?api_key={API_KEY}'
        response = requests.get(url)
        json = response.json()
        episode = json['next_episode_to_air']
        result = {
                'date': episode['air_date'],
                'episode_number': episode['episode_number'],
                'name': episode['name']
                }
        return result

