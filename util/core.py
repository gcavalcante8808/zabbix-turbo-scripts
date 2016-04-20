#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este modulo contém as principais funções a serem utilizadas em outros
módulo, como conexão ao Zabbix e escrita em arquivos.
"""

import json
import re
import requests
from pyzabbix import ZabbixAPI


def connect(user, password, server, http_auth=False):
    """
    Realiza a conexão com o servidor Zabbix Alvo e retorna o objeto
    utilizado nas operações.
    """
    zapi = ZabbixAPI(server)

    zapi.session.verify = False
    requests.packages.urllib3.disable_warnings()

    if http_auth:
        zapi.session.auth = (user,password)
        zapi.login(user,)
    else:
        zapi.login(user,password)

    return zapi


def write_results(filename, results):
    """
    Recebe um nome de arquivo e os resultados e escreve em formato JSON.
    """
    with open(filename, "w") as rfile:
        rfile.write(json.dumps(results, sort_keys=True, indent=2))

