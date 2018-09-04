#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-25
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp7](http://github.com/freezed/ocp7/) project.

 """
import json
import requests
from config import GOO_API, WIK_API


class Place:
    """
    Defines a place with the user query

    Gets geo data from Google geocode & static map API
    Gets information from Wikipedia API

    """

    def __init__(self, query):
        """
        Sets arguments
        """
        self.query = str(query)
        self.article_data = {'status': False}

        # Get geodata
        self.set_geo_data()
        self.set_article_data()

    def get_json(self, url, payload):
        """
        Request API
        """
        response = requests.get(url, payload)
        api_json = response.json()
        api_status = response.status_code

        if response.status_code == 200:
            return api_json

        else:
            return False

    def set_article_data(self):
        """
        Function documentation

        """
        payload = {'srsearch': self.query}
        # Adds basic API call parameters
        payload.update(**WIK_API['PARAM_SEARCH'])

        search_json = self.get_json(WIK_API['ROOT_URL'], payload)

        try:
            self.article_data['title'] = search_json['query']['search'][0]['title']
            self.article_data['pageid'] = search_json['query']['search'][0]['pageid']

        except TypeError:
            self.article_data['context'] = 'search TypeError'

        except IndexError:
            self.article_data['context'] = 'search IndexError'

        else:
            self.article_data['status'] = True
            payload = {'titles': self.article_data['title']}
            # Adds basic API call parameters
            payload.update(**WIK_API['PARAM_EXTRAC'])

            article_json = self.get_json(WIK_API['ROOT_URL'], payload)

            try:
                self.article_data['extract'] = article_json['query']['pages'][str(self.article_data['pageid'])]['extract']

            except TypeError:
                self.article_data['context'] = 'article'
                self.article_data['status'] = False

    def set_geo_data(self):
        """
        Calls Google geocode API with a string query & retrieve a Place

        Filter API's JSON to keep only useful data
        """
        # Build URL request
        payload = {
            'key': GOO_API['KEY'],
            'address': self.query,
            'region': GOO_API['COUNTRY'],
            'country': GOO_API['COUNTRY'],
        }

        geo_json = self.get_json(GOO_API['URL_GEO'], payload)

        self.geo_data = {'truncated_address': {}}

        for component in geo_json['results'][0]['address_components']:
            self.geo_data['truncated_address'].update(
                {component['types'][0]: component['long_name']}
            )

        try:
            self.geo_data['formatted_address'] = geo_json['results'][0]['formatted_address']
            self.geo_data['location'] = geo_json['results'][0]['geometry']['location']

        except TypeError:
            self.geo_data = {'error': 'no_data'}

        else:
            # No data if request ĥas less or more 1 result
            if len(geo_json['results']) > 1:
                self.geo_data['warning'] = 'no_single_geocode_result'

            elif len(geo_json['results']) == 0:
                self.geo_data = {'error': 'no_geocode_result'}

            # Adds locality in orginal query if missing for more appropriateness
            try:
                loc = self.geo_data['truncated_address']['locality'].replace(
                    "-", " "
                ).replace(
                    "'", " "
                ).lower()

                if loc not in self.query.lower():
                    self.query = "{} {}".format(
                        self.query,
                        self.geo_data['truncated_address']['locality']
                    )

            except KeyError:
                self.geo_data['query_update_exception'] = 'locality'

    def get_static_map_url(self):
        """
        Return url of a static maps using Google Static Maps API
        """
        coord = "{},{}".format(
            self.geo_data['location']['lat'],
            self.geo_data['location']['lng'],
        )

        payload = {
            'key': GOO_API['KEY'],
            'center': coord,
            'markers': coord,
            'size': "{}x{}".format(*GOO_API['MAP_SIZE']),
        }

        response = requests.get(
            GOO_API['URL_MAP'],
            payload,
        )

        return response.url
