#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: [freezed](https://gitlab.com/free_zed) 2018-08-23
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of project [grandpy](https://gitlab.com/free_zed/grandpy/).
"""
from os import environ

PORT = 1664
# HOST = 'localhost'
HOST = '192.168.1.70'
# HOST = '192.168.46.64'
APP = {
    'NAME': 'GrandPy Bot',
    'BASELINE': 'Le paPy qui paPotte ',
    'REPO_URL': 'https://gitlab.com/free_zed/grandpy/',
    'DEBUG': True,
    'MAP_LINK': 'https://opentopomap.org/#map=17/{lat}/{lng}',
}
GOO_API = {
    'URL_GEO': 'https://maps.googleapis.com/maps/api/geocode/json',
    'URL_MAP': 'https://maps.googleapis.com/maps/api/staticmap',
    'KEY': environ['GOO_API_KEY'],
    'MAP_SIZE': (600,300),
    'COUNTRY': 'FR',
    'MIN_QUERY_LEN': 5,
}
WIK_API = {
    'ROOT_URL': 'https://fr.wikipedia.org/w/api.php',
    'PARAM_SEARCH': {
        'action':'query',
        'utf8':True,
        'format':'json',
        'list':'search',
    },
    'PARAM_EXTRAC': {
        'action':'query',
        'utf8':True,
        'format':'json',
        'prop':'extracts',
        'exlimit':1,
        'explaintext':True,
        # 'exsentences':3,
        'exsectionformat':'plain',
        'exintro':True,
    }
}
HOME = {
    'INPUT_PO': "Salut GrandPy connais tu l'adresse d'OpenClassrooms",
    'INPUT_SIZE': 42,
    'INPUT_LABEL': "Questionne GrandPy au sujet d'un lieu",
    '': "",
}
