import requests
import hashlib
import pandas as pd

from time import sleep
from datetime import datetime

SITES = ['https://g1.globo.com/',
         'https://noticias.uol.com.br/',
         'https://www.r7.com/',
         'https://www.cnnbrasil.com.br/']

MONITORING_INTERVAL = 2
MONITORING_COUNT_TARGET = 5

HEADERS = {'User-Agent': 'Mozilla/5.0'}

class HashComparer:
    def __init__(self):
        self.previous = None
        self.latest = None

    def update(self, new_hash):
        self.previous = self.latest
        self.latest = new_hash   

    def did_change(self):
        if self.previous is not None and self.latest is not None:
            return self.previous != self.latest
        return False

class SiteMonitor:
    def __init__(self):
        self._data = pd.DataFrame(columns = ['timestamp', 'attempt', 'url', 'changed', 'latest', 'previous'])
    
    def monitor(self, site: str):
        
        hash_comparer = HashComparer()

        for count in range(MONITORING_COUNT_TARGET): # Count from 0 to TARGET

            response = requests.get(
                site,
                headers = HEADERS
            )

            utf8_content = repr(response.text).encode('utf-8')
            response_hash = hashlib.sha224(utf8_content).hexdigest()

            hash_comparer.update(response_hash)

            self._data = pd.concat([self._data, pd.DataFrame({
                'timestamp': [datetime.now()],
                'attempt': [count],
                'url': [site],
                'changed': [hash_comparer.did_change()],
                'latest': [hash_comparer.latest],
                'previous': [hash_comparer.previous]
            })], ignore_index=True)

            print(f'[{datetime.now()}] Monitoring attempt: ({count}) Url: {site} Did change?: {hash_comparer.did_change()} | Hashes latest: {hash_comparer.latest} VS. previous: {hash_comparer.previous}')

            sleep(MONITORING_INTERVAL)