from config import BASE_URI
from utils.request import APIRequest
from clients.base_client import BaseClient
import json


class MatchBookClient(BaseClient):

    def __init__(self):
        super().__init__()

        self.base_url = BASE_URI
        self.request = APIRequest()

    def login(self, login_data):
        login_url = f'{BASE_URI}/bpapi/rest/security/session'
        response = self.request.post(login_url, json.dumps(login_data), self.headers)
        return response
