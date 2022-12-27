from dotenv import find_dotenv, load_dotenv
from flask import session
import json, requests
from os import environ as env
from requests.exceptions import RequestException, HTTPError, URLRequired
import re
from urllib.parse import quote

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

class Auth0Data:
    def __init__(self):
        self.client = Auth0MgmtApi()

    def get_applications(self):
        apps = self.client.get_applications()
        return [{
                'name': a['name'],
                'type': a['app_type'],
                'client_id': a['client_id']
            } for a in apps if a.get('app_type')]

    def get_actions(self):
        return [{
                'name': a['name'],
                'app': self.detect_app(a['code']),
                'trigger': ", ".join(f"{t['id']} ({t['version']})" for t in a['supported_triggers']),
                'id': a['id'],
                'created': a['created_at']
            } for a in self.client.get_actions()]

    def is_manager(self, uid):
        roles = self.client.get_roles(uid)
        return any([r for r in roles if r['name'].lower() == 'managers'])

    def detect_app(self, code):
        pat = re.compile('async \(event, api\) => {\n\s+if \(event\.client\.name (?P<condition>[!=])== "(?P<app_name>.*)"\)')
        m = pat.search(code)
        if m is None:
            return "All applicatoins"
        else:
            if m['condition'] == '=':
                return m['app_name']
            else:
                return f"All applicatoins except for {m['app_name']}"


class Auth0MgmtApi:
    def __init__(self):
        self.initialize_api()

    def initialize_api(self):
        self.access_token = ''
        self.set_config()

    def set_config(self):
        domain = env.get("AUTH0_DOMAIN")
        self.base_url = f"https://{domain}"
        self.audience = f'https://{domain}/api/v2/'
        self.client_id = env.get("AUTH0_CLIENT_ID"),
        self.client_secret = env.get("AUTH0_CLIENT_SECRET"),

    # Get an Access Token from Auth0
    def fetch_token(self):
        if session.get("access_token") is None:
            payload =  {
              'grant_type': "client_credentials", # OAuth 2.0 flow to use
              'client_id': self.client_id,
              'client_secret': self.client_secret,
              'audience': self.audience
            }
            response = requests.post(f'{self.base_url}/oauth/token', data=payload)
            oauth = response.json()
            session["access_token"] = oauth.get('access_token')
        return session["access_token"]

    def api_header(self):
        if len(self.access_token) == 0:
            token = self.fetch_token()
            if token is None:
                raise ValueError #TODO find better Error
            self.access_token = token
        return {
          'Authorization': f'Bearer {self.access_token}',
          'Content-Type': 'application/json'
        }

    def get_applications(self):
        return self.req_get(f'{self.base_url}/api/v2/clients')

    def get_actions(self):
        res = self.req_get(f'{self.base_url}/api/v2/actions/actions')
        return res.get('actions') if (res and 'actions' in res) else []

    def get_roles(self, uid):
        return self.req_get(f'{self.base_url}/api/v2/users/{quote(uid)}/roles')

    def req_get(self, url):
        try:
            res = requests.get(url, headers=self.api_header())
            res.raise_for_status()
            return res.json()
        except HTTPError as e:
            print(f'HTTPError: {str(e)}')
        except URLRequired as e:
            print(f'URLRequired: {str(e.reason)}')
        except RequestException as e:
            print(f'RequestException: {e}')
        except Exception as e:
            print(f'Generic Exception: {e}')


