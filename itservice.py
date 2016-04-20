#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Esse módulo é responsável por criar IT Services dentro do Zabbix a partir dos
hosts e triggers cadastradas dentro do Mesmo.

Utiliza-se do módulo util para iniciar a conexão um servidor Zabbix e requer
que as bibliotecas presentes no arquivo requirements.txt esteja instalada.

Adicionalmente, este módulo é compatível com as versões 2 e 3 do Python.
"""
import pdb
import re
import argparse
from util.core import connect
from util.validators import PasswordPromptAction, URLValidatorAction


TRIGGER_RE = re.compile(r'{\w+}|{\w+[.]\w+}')


class ITServiceManager:
    """
    Contém os métodos de gerenciamento dos serviços de TI do Zabbix.
    Neste momento contém suporte a criação da árvore e posteriormente também
    possuíra suporte a remoção completa desta.
    """
    def __init__(self, server, user, password, http_auth):
        self.zapi = connect(server=server, user=user, password=password,
                            http_auth=http_auth)
        self.services = None

    def populate_tree(self):
        """
        Recupera todas as informações necessárias do ambiente zabbix
        e utiliza os demais métodos para inserir registros na árvore
        de IT Services do Zabbix.
        """
        triggers = self.zapi.trigger.get(min_severity=5, active=True,
                                         output=['triggerid', 'description'],
                                         selectHosts=['host', 'name'],
                                         selectGroups=['name'])

        # Mapeamento dos valores para facilitar o tratamento
        # posterior dos dados.
        info = ({'trigger': TRIGGER_RE.sub(trigger['hosts'][0]['host'],
                                           trigger['description']),
                 'triggerid':trigger['triggerid'],
                 'groups': trigger['groups'],
                 'name': '{0} - {1}'.format(trigger['hosts'][0]['host'],
                                            trigger['hosts'][0]['name'])
                }
                for trigger in triggers)

        self.services = self.get_services()

        # Criação dos serviços propriamente ditos.
        for item in info:
            for group in item['groups']:
                if not self.search_service(group['name']):
                    self.create_service(name=group['name'])

                if not self.search_service(item['name']):
                    parentid = self.search_service(group['name'])

                    if isinstance(parentid, dict):
                        self.create_service(name=item['name'],
                                            parentid=parentid['serviceid'])


            parentid = self.search_service(item['name'])
            result = self.search_service(item['trigger'], parentid['serviceid'])

            if not result and isinstance(parentid, dict):
                self.create_service(name=item['trigger'],
                                    parentid=parentid['serviceid'],
                                    triggerid=item['triggerid'])

    def get_services(self):
        """
        Retorna os serviços de TI presentes no Zabbix
        """
        return self.zapi.service.get(output=['name', 'triggerid'],
                                     selectParent=['parentid'])


    def create_service(self, name, parentid=None, triggerid=0):
        """
        Recebe um hostgroup ou host e cria um filho correspondente nos
        serviços de TI do Zabbix.

        name: String - Nome do Serviço TI
        parentid: Integer - Id do Pai do serviço a ser adicionado.
        triggerid: 0 por padrão, se não houver trigger.
        """
        if not parentid and not triggerid:
            result = self.zapi.service.create(name=name, showsla=1,
                                              sortorder=1, algorithm=1,
                                              goodsla=99.9)

        elif parentid and triggerid == 0:
            result = self.zapi.service.create(name=name,
                                              parentid=parentid,
                                              showsla=1, sortorder=1,
                                              algorithm=1, goodsla=99.9)

        else:
            result = self.zapi.service.create(name=name,
                                              parentid=parentid,
                                              showsla=1, sortorder=1,
                                              algorithm=1, goodsla=99.9,
                                              triggerid=triggerid)

        if parentid:
            self.services.append({'name':name, 'triggerid': triggerid,
                                  'parent': {'serviceid': parentid},
                                  'serviceid': result['serviceids'][0]})
        else:
            self.services.append({'name':name, 'triggerid': triggerid,
                                  'parent': [],
                                  'serviceid': result['serviceids'][0]})


    def search_service(self, name, parentid=None):
        """
        Verify if a service already exists on the service variable.
        """
        if parentid:
            match = (x for x in self.services if x.get('name') == name and
                     isinstance(x['parent'], dict) and
                     x['parent']['serviceid'] == parentid)
        else:
            match = (x for x in self.services if x.get('name') == name)

        try:
            first_item = next(match)
            return first_item
        except(StopIteration,):
            return False


    def purge_tree(self):
        """
        Purge all or specific leafs from the it service tree.
        """
        services = self.get_services()
        while True:

            header_ids = (x['serviceid'] for x in services
                          if not x['parent'])
            for header in header_ids:
                self.zapi.service.deletedependencies(header)
                self.zapi.service.delete(header)

            #TODO: Usar services interno apenas.
            services = self.get_services()

            if not services:
                break


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="""Módulo de Criação automática
    de ávores para ITServices no Zabbix.""")
    PARSER.add_argument('-s', dest='server', type=str, required=True,
                        action=URLValidatorAction)

    PARSER.add_argument('-u', dest='user', type=str, required=True)

    PASS_GROUP = PARSER.add_mutually_exclusive_group(required=True)
    PASS_GROUP.add_argument('-p', dest='password', type=str,
                            action=PasswordPromptAction)
    PASS_GROUP.add_argument('--passfile', type=argparse.FileType('r'))

    PARSER.add_argument('--httpauth', dest='http_auth', type=bool, required=False)
    PARSER.add_argument('--purge', dest='purge_tree', type=bool, required=False)

    ARGS = PARSER.parse_args()
    SERVER = ARGS.server
    USER = ARGS.user
    HTTP_AUTH = ARGS.http_auth or False

    if ARGS.passfile:
        PASSWORD = ARGS.passfile.read()
    else:
        PASSWORD = ARGS.password

    ITS = ITServiceManager(SERVER, USER, PASSWORD, HTTP_AUTH)

    if ARGS.purge_tree:
        ITS.purge_tree()
    else:
        ITS.populate_tree()
