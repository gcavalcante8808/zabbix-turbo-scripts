#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este módulo contém validadores comuns que podem ser reutilizados em outros
módulos.
"""
import argparse
import getpass
import re


class PasswordPromptAction(argparse.Action):
    """
    Utiliza GetPass para pegar a senha a partir do prompt e insere no atributo
    do password do argparse.
    """

    def __call__(self, parser, args, values, option_strings=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


class URLValidatorAction(argparse.Action):
    """
    Verifica se o valor recebido é uma URL válida.
    """

    def __call__(self, parser, args, values, option_strings=None):
        url_re = re.compile(r"https?:\/\/\w{2,30}\.\w{2,30}\.[\w.]*")

        if url_re.match(values):
            setattr(args, self.dest, values)
        else:
            raise ValueError("URL Inválida '{0}'".format(values))
