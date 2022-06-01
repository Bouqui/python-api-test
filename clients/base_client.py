class BaseClient:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept': '*/*'
        }
