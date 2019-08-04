#!/usr/bin/python3
#coding: utf-8

# BeautifulSoup será usado para verificar se o perfil da rede social realmente existe
from bs4 import BeautifulSoup as bs

# Networkx fará um gráfico interativo com conexões do e-mail alvo com as redes sociais e outros dados
import networkx as nx #para criação de gráfico

import argparse as args 

import webbrowser

# huepy é para cores (bold = negrito, red = vermelho etc.)
from huepy import *

# para permutar
from itertools import permutations

import requests
import json

parser = args.ArgumentParser()
parser.add_argument("-e","--email",required=True,help="Put the email you'll check")
parsed = parser.parse_args()



email_example = 'bill@microsoft.com'
email = parsed.email

def emailrep(email, functions):
    ''' 
    a função emailrep (de emailrep.io) faz uma única requisição para a API.
    Após recolher as redes sociais que o e-mail está cadastrado, o script inicia funções
    para cada rede social correspondente
    '''

    r = requests.get(f'https://emailrep.io/{email}')

    js = json.loads(r.text)

    profiles = js['details']['profiles']

    for profile in profiles:
        for function in functions:
            if profile == function:
                try:
                    function(email)
                except Exception as e:
                    print(bold(red('ERROR: ') + str(e)))

functions = ['linkedin',
            'flickr',
            'instagram',
            'pinterest',
            'tumblr',
            'twitter']

# Iniciar gráfico
G = nx.Graph()

def linkedin(email):
    ''' Usa o LinkedIn para recolher o nome e o estado '''
    print("O Seu Navegador ira se abrir para conferir se o email tem um perfil no linkedin")
    webbrowser.open(f'https://www.linkedin.com/sales/gmail/profile/viewByEmail/{email}')
    pass

def github(email):
    user = email.split('@')[0]

    # Para pegar dados básicos (localização, blog, nome, seguidores, seguindo e bio)
    github_api_1 = requests.get(f'https://api.github.com/users/{user}')

    if github_api_1.status_code == 200:


        github_js_1 = json.loads(github_api_1.text)

        bio = github_js_1['bio']
        company = github_js_1['company']
        name = github_js_1['name']
        followers = github_js_1['followers']
        following = github_js_1['following']
        location = github_js_1['location']
        login = github_js_1['login']

        # adicionar nós
    else:
        pass