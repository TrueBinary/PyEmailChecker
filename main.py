#!/usr/bin/python3
#coding: utf-8

# Networkx fará um gráfico interativo com conexões do e-mail alvo com as redes sociais e outros dados
import networkx as nx #para criação de gráfico
import matplotlib.pyplot as plt

# Google search
from googlesearch import search

import argparse as args 
import dns.resolver
import smtplib
import webbrowser

# huepy é para cores (bold = negrito, red = vermelho etc.)
from huepy import *

import requests
import json

email_example = 'bill@microsoft.com'
parser = args.ArgumentParser()
parser.add_argument("-e","--email",required=True,type=str, help=f"Você precisa colocar um email igual a esse {email_example}")
parsed = parser.parse_args()

email = parsed.email

# Iniciando gráfico
graph = nx.Graph()

def github(email):
    user_email = email.split('@')[0]

    # Para pegar dados básicos (localização, blog, nome, seguidores, seguindo e bio)
    github_api_1 = requests.get(f'https://api.github.com/users/{user_email}')
    print(github_api_1.status_code)

    if github_api_1.status_code == 200:
        # adicionar no do github
        graph.add_node(f'Github: {user_email}')

        # conectar no do github ao email
        graph.add_edges_from([(email, f'Github: {user_email}')])

        github_js_1 = json.loads(github_api_1.text)

        bio = github_js_1['bio']
        company = github_js_1['company']
        name = github_js_1['name']
        followers = github_js_1['followers']
        following = github_js_1['following']
        location = github_js_1['location']
        login = github_js_1['login']
    else:
        pass

global functions
functions = [github]

# Caso seja diferente desses provedores, o script procurará o domínio para relação entre usuario e dominio
common_providers = ['hotmail.com', 
                    'gmail.com', 
                    'protonmail.com', 
                    'protonmail.ch', 
                    'outlook.com',
                    'tutanota.com',
                    'keemail.me']

def emailrep(email):
    ''' 
    a função emailrep (de emailrep.io) faz uma única requisição para a API.
    Após recolher as redes sociais que o e-mail está cadastrado, o script inicia funções
    para cada rede social correspondente
    '''

    r = requests.get(f'https://emailrep.io/{email}')

    javaScript = json.loads(r.text)

    profiles = javaScript['details']['profiles']

    graph.add_node(email)

    for profile, function, provider in zip(profiles, functions, common_providers):
        domain = email.split('@')[-1]
        if profile == function:
            try:
                function(email)
            except Exception as e:
                print(bold(bad('ERROR: ') + str(e)))
                pass
            finally:
                show_nodes(email)
        if domain not in common_providers:
            try:
                email_verifier(email)
                search_data_leak(email)
            except Exception as e:
                print(bold(red('ERROR: ') + str(e)))
            finally:
                show_nodes(email)
        else:
            try:
                search_data_leak(email)
                function(email)
            except Exception as e:
                print(bold(bad('ERROR 1: ') + str(e)))
            finally:
            	show_nodes(email)

def email_verifier(email):
    # email verification
    domain = email.split('@')[-1]

    try:
        records = dns.resolver.query(domain,"MX")
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        server = smtplib.SMTP()
        server.set_debuglevel(0)

        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(email)
        code, message = server.rcpt(str(email))
        server.quit()

        if code == 250:
            print("O DNS do email foi encontrado")
        else:
            print("Foi Impossivel de encontrar o dns deste email!")
    except Exception as e:
        print(bold(bad('E-MAIL VERIFICATION ERROR: ') + str(e)))
        pass

def search_data_leak(email):
    # Google -> vazamentos de dados do pastebin
    
    domain = email.split('@')[-1]
    username = email.split('@')[0]

    try:
        pastebin = search(f'intext:"{email}" site:pastebin.com intext:"leak"')

        for result in pastebin:
            # adiciona nó de resultado no grafico
            graph.add_node(f'Data leaked: {result}')

            # conectar o nó ao e-mail
            graph.add_edges_from([(email, f'Data leaked: {result}')])
    except Exception as e:
        print(bold(bad('GOOGLE ERROR: ') + str(e)))
        pass

def show_nodes(email):
    pos = nx.spring_layout(graph)

    # criar grafico
    nx.draw(graph, 
            with_labels=True, 
            k=0.15, 
            node_size=5000,
            node_color='blue')

    # salvar grafico em png
    plt.savefig(email + '_connections.png')

    # mostrar grafico
    plt.show()

def linkedin(email):
    ''' Usa o LinkedIn para recolher o nome e o estado '''
    print("O Seu Navegador ira se abrir para conferir se o email tem um perfil no linkedin")
    webbrowser.open(f'https://www.linkedin.com/sales/gmail/profile/viewByEmail/{email}')
    pass

def main():
    emailrep(email)
if __name__ == '__main__':
    main()
