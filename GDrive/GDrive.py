# -*- coding: utf-8 -*-
import json, argparse, os, httplib2
from apiclient.discovery import build
# Get Credentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import OAuth2Credentials
from oauth2client.file import Storage
# PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def create_oauth_authorize_file(json_key_file):
    if os.path.isfile(json_key_file):
        print 'Accepted... Loading JSON Key File.'
        try:
            # Get Secret Data from JSON File.
            json_data = json.loads(open(key_file_path).read())
            OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
            CLIENT_ID = json_data['installed']['client_id']
            CLIENT_SECRET = json_data['installed']['client_secret']
            REDIRECT_URI = json_data['installed']['redirect_uris'][0]
            # Get authorize file.
            flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            storage = Storage('credentials_file')
            storage.put(credentials)

        except:
            print 'exception'
    else:
        print 'Not Accepted, No Available File.'

def create_google_drive_session(path_to_credentials_file):
    try:
        storage = Storage(path_to_credentials_file)
        credentials = storage.get()
        http = credentials.authorize(httplib2.Http())
        service = build('drive', 'v2', http=http)
        response = service.files().list().execute()

    except:
        print 'Error'

if __name__ == "__main__":
    # --
    parser = argparse.ArgumentParser(description='Google Drive API.')
    parser.add_argument('-k', '--key', help='input google drive api json key.')

    args = parser.parse_args()
    # parser key file
    key_file_path = args.key
    if os.path.isfile('credentials_file'):
        print 'Find credentials file, now start service.'
        gauth = GoogleAuth()
        gauth.credentials= OAuth2Credentials.from_json(open('credentials_file').read())
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
        for file1 in file_list:
          print 'title: %s, id: %s' % (file1['title'], file1['id'])

    else:
        print 'No credentials file, now create one.'
        create_oauth_authorize_file(key_file_path)
