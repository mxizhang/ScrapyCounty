# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
from __future__ import print_function
import httplib2
import os

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-f09bdc10eb52.json', scope)

http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
spreadsheet_id = '1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs'
requests = []

requests.append({
    'insertDimension': {
        'range': {'sheetId': 0, 'dimension': 1, 'startIndex': 1, 'endIndex': 5},
        "inheritFromBefore": 'false'
    }
})

batchUpdateRequest = {'requests': requests}
service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batchUpdateRequest).execute()