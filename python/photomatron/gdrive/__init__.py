import os.path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

_CREDENTIALS = 'credentials.json'
_FOLDER = '1PqrOLdovUMI5Yb_Hiz7tFS0Hywnn_bM-'


def _authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(_CREDENTIALS)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(_CREDENTIALS)

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
