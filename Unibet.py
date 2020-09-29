import requests

class Unibet:
    def __init__(self):
        self.headers = {
            'authority': 'pl.unibet-27.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en;q=0.9,pl;q=0.8'
            
        }


    def get_competition(self, url):
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_event_details(self, id):
        url = f"https://eu-offering.kambicdn.org/offering/v2018/ub/betoffer/event/{id}.json"
        response = requests.get(url, headers=self.headers)
        return response