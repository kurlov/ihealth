__author__ = 'Alexandr Kurlov'
from flask import request, redirect
import requests
import json
import config as cfg

class iHealth():
    """ A basic class of iHealth API handler """

    def __init__(self, client_id, client_secret, redirect_uri):
        self.access_token = ''
        self.refresh_token = ''
        self.user_id = ''
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = cfg.AUTH_URL
        self.user_url = cfg.USER_DATA_URL
        self.app_url = cfg.ALL_DATA_URL
        self.response_type = 'code'  # default value for response_type
        self.APIName = 'OpenApiBP OpenApiWeight OpenApiActivity OpenApiBG OpenApiSleep OpenApiSpO2 OpenApiUserInfo'  # an array of target API
        self.RequiredAPIName = 'OpenApiBP OpenApiWeight OpenApiActivity OpenApiBG OpenApiSleep OpenApiSpO2 OpenApiUserInfo'  # it is must be selected for the authentication page
        self.IsNew = 'true'  # the system will be auto redirected to the sign up page

    def authorize(self):
        payload = {'client_id': self.client_id, 'response_type': self.response_type,
                   'redirect_uri': self.redirect_uri, 'APIName': self.APIName,
                   'RequiredAPIName': self.RequiredAPIName, 'IsNew': self.IsNew}
        r = requests.get(self.auth_url, params=payload)
        return r

    def callback(self):
        code = self.get_code()
        grant_type = 'authorization_code'   # is currently the only supported value
        payload = {'code': code, 'client_id': self.client_id, 'grant_type': grant_type,
                   'client_secret': self.client_secret, 'redirect_uri': self.redirect_uri}
        r = requests.get(self.auth_url, params=payload)
        self.access_token, self.refresh_token = self.get_tokens(r.text)
        self.user_id = self.get_user_id(r.text)
        return r.text

    def get_code(self):
        if 'code' not in request.args:
            return None
        return request.args['code']

    def get_tokens(self, data):
        resp = json.loads(data)
        if resp['AccessToken'] and resp['RefreshToken']:
            return resp['AccessToken'], resp['RefreshToken']
        else:
            return None, None # this should be handled as an error

    def get_user_id(self, data):
        resp = json.loads(data)
        if resp['UserID']:
            return resp['UserID']
        else:
            return None

    def get_blood_pressure(self):
        base_url = self.user_url+str(self.user_id)+'/bp/'
        BP = cfg.DATA_TYPES['OpenApiBP']
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': BP['sc'], 'sv': BP['sv']}
        r = requests.get(base_url, params=payload)
        return r.text

    def get_weight(self):
        base_url = self.user_url+str(self.user_id)+'/weight/'
        Weight = cfg.DATA_TYPES['OpenApiWeight']
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': Weight['sc'], 'sv': Weight['sv']}
        r = requests.get(base_url, params=payload)
        return r.text

    def get_bg(self):
        base_url = self.user_url+str(self.user_id)+'/glucose/'
        BG = cfg.DATA_TYPES['OpenApiBG']
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': BG['sc'], 'sv': BG['sv']}
        r = requests.get(base_url, params=payload)
        return r.text

    def get_blood_oxygen(self):
        base_url = self.user_url+str(self.user_id)+'/spo2/'
        SpO2 = cfg.DATA_TYPES['OpenApiSpO2']
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': SpO2['sc'], 'sv': SpO2['sv']}
        r = requests.get(base_url, params=payload)
        return r.text

    def get_activity_report(self):
        base_url = self.user_url+str(self.user_id)+'/activity/'
        Activity = cfg.DATA_TYPES['OpenApiActivity']
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
                   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
                   'sc': Activity['sc'], 'sv': Activity['sv']}
        r = requests.get(base_url, params=payload)
        return r.text

    def get_sleep_report(self):
        pass

    def get_food(self):
        pass

    def get_sport_report(self):
        pass

