import os.path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


_FOLDER = 'XXXXX'


def _authenticate():
    client_secret = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
    credentials = os.path.join(os.path.dirname(__file__), 'credentials.json')

    gauth = GoogleAuth()
    gauth.settings['client_config_file'] = client_secret

    gauth.LoadCredentialsFile(credentials)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()

    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(credentials)

    return gauth


def post_picture(filepath):
    authorization = _authenticate()
    drive = GoogleDrive(authorization)
    gfile = drive.CreateFile({
        'title': os.path.basename(filepath),
        'mimeType': 'image/jpg',
        'parents': [{
            'kind': 'drive#fileLink',
            'id': _FOLDER
        }]
    })
    gfile.SetContentFile(filepath)
    gfile.Upload()
