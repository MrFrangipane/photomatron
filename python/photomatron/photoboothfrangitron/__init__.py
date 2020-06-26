import os
import json
import requests


credentials_filepath = os.path.join(os.path.dirname(__file__), 'credentials.json')
with open(credentials_filepath, 'r') as f_credentials:
    cred = json.load(f_credentials)

URL = 'https://photobooth.frangitron.com/'
LOGIN = cred['email']
PASSWORD = cred['password']


def post_image(image_filepath):
    session = requests.Session()
    session.get(URL)

    session.post(
        URL + 'login',
        data={
            'csrf_token': session.cookies['CSRF-TOKEN'],
            'email': LOGIN,
            'password': PASSWORD
        }
    )

    response = session.post(
        URL,
        data={
            'csrf_token': session.cookies['CSRF-TOKEN']
        },
        files={'picture': open(image_filepath, 'rb')}
    )

    return response.ok
