# -*- coding: utf-8 -*-
import json
import argparse
import os
import httplib2
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow


if __name__ == "__main__":
    CLIENT_ID = None
    CLIENT_SECRET = None
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    REDIRECT_URI = None
    # --
    parser = argparse.ArgumentParser(description='Google Drive API.')
    parser.add_argument('-k', '--key', help='input google drive api json key.')
    args = parser.parse_args()
    # parser key file
    key_file_path = args.key
    if os.path.isfile(key_file_path):
        print 'Accepted.'
        try:
            json_data = json.loads(open(key_file_path).read())
            # json.dumps(json_data, indent=4)
            CLIENT_ID = json_data['installed']['client_id']
            CLIENT_SECRET = json_data['installed']['client_secret']
            REDIRECT_URI = json_data['installed']['redirect_uris'][0]
            flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            http = httplib2.Http()
            http = credentials.authorize(http)
            drive_service = build('drive', 'v2', http=http)


        except:
            print 'exception'
    else:
        print 'Not Accepted.'
