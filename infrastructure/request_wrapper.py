class RequestsWrapper:
    def __init__(self, requests):
        self.requests = requests

    def post(self, url , json):
        self.requests.post(url, json=json)