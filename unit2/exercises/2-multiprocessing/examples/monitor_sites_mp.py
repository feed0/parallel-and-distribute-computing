import multiprocessing
from time import sleep
from random import randint
from datetime import datetime
import random
import requests
import hashlib


def monitorar(url):
    p = multiprocessing.current_process()

    proxies = {
      'http': 'http://bronze2.fapemig.br:3128',
      'https': 'http://bronze2.fapemig.br:3128'
    }

    mudancas = 0

    cont = 5
    intervalo = random.randint(1, 5)

    for i in range(cont):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, proxies=proxies)
        conteudo = repr(r.text).encode('utf-8')

        hash_site = hashlib.sha224(conteudo).hexdigest()
        print('[' + str(datetime.now()) + '] Processo : ' + str(p.pid) + ' Url : ' + url + ' Hash: ' + str(hash_site))

        if i == 0:
            old_hash_site = hash_site
        else:
            if old_hash_site != hash_site:
                mudancas += 1
                old_hash_site = hash_site

        sleep(intervalo)
    print('[' + str(datetime.now()) + '] FINALIZADO - Processo : ' + str(p.pid) + ' Url : ' + url + ' Mudancas : ' + str(mudancas))



if __name__ == '__main__':
    sites = ['https://g1.globo.com/', 'https://noticias.uol.com.br/', 'https://www.r7.com/', 'https://www.cnnbrasil.com.br/']

    p = multiprocessing.Pool(3)
    p.map(monitorar, sites)