#!/usr/bin/env python

import csv
import datetime
import json
import os

from bs4 import BeautifulSoup
import requests

from clerk import utils


class BaseObject(object):

    # Maps SCOTUS justice codes to SCDB justicenames.
    JUSTICE_DECISION_MAP = {
        "A": "SAAlito",
        "AS": "AScalia",
        "B": "SGBreyer",
        "D": None,
        "DS": "DHSouter",
        "G": "RBGinsburg",
        "JS": "JPStevens",
        "K": "AMKennedy",
        "PC": None,
        "R": "JGRoberts",
        "T": "CThomas",
        "SS": "SSotomayor",
        "EK": "EKagan",
    }

    ARGUMENTS_BASE_URL = 'http://www.supremecourt.gov/oral_arguments/argument_transcript/%(term)s'
    AUDIO_BASE_URL = 'http://www.supremecourt.gov/oral_arguments/argument_audio/%(term)s'
    OPINIONS_BASE_URL = 'http://www.supremecourt.gov/opinions/slipopinion/%(term)s'

    ARGUMENTS_TERMS = range(2000, int(utils.current_term()) + 1)
    AUDIO_TERMS = range(2010, int(utils.current_term()) + 1)
    OPINIONS_TERMS = range(2006, int(utils.current_term()) + 1)

    DATA_DIRECTORY = os.path.join(os.path.realpath(__file__).split(__file__.split('/')[-1])[0], 'data')

    def set_data_directory(self):
        if not os.path.exists(self.DATA_DIRECTORY):
            os.system('mkdir -p %s' % self.DATA_DIRECTORY)

    def set_fields(self, **kwargs):
        fieldnames = self.__dict__.keys()
        for k,v in kwargs.items():
            k = k.lower().strip()
            v = unicode(v.decode('latin-1'))
            if k in fieldnames:
                setattr(self, k, v)

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class MeritsCase(BaseObject):

    def __init__(self, **kwargs):
        self.term = None
        self.docket = None
        self.short_name = None
        self.opinion_pdf_url = None
        self.argument_pdf = []
        self.audio_mp3 = []

        self.set_fields(**kwargs)

        def __unicode__(self):
            return "%s (%s)" % (self.short_name, self.term)


class Load(BaseObject):

    def __init__(self, **kwargs):
        self.opinions_html = {}
        self.arguments_html = {}
        self.audio_html = {}
        self.cases = {}
        self.start = datetime.datetime.now()
        self.set_data_directory()

    def scrape_arguments(self):
        for term in self.ARGUMENTS_TERMS:
            self.arguments_html[str(term)] = requests.get(self.ARGUMENTS_BASE_URL % {'term': str(term)}).text

    def scrape_audio(self):
        for term in self.AUDIO_TERMS:
            self.audio_html[str(term)] = requests.get(self.AUDIO_BASE_URL % {'term': str(term)}).text

    def scrape_opinions(self):
        for term in self.OPINIONS_TERMS:
            self.opinions_html[str(term)] = requests.get(self.OPINIONS_BASE_URL % {'term': str(term)[2:4]}).content

    def parse_opinions(self):
        for term in self.OPINIONS_TERMS:
            soup = BeautifulSoup(self.opinions_html[str(term)], 'lxml')
            rows = soup.select('center')[0].select('table')[0].select('tr')[1:]

            for row in rows:
                case_dict = {}
                cells = row.select('td')
                case_dict['term'] = str(term)
                case_dict['docket'] = cells[2].text.strip()
                case_dict['short_name'] = cells[3].text.strip()
                case_dict['opinion_pdf_url'] = 'http://www.supremecourt.gov' + cells[3].select('a')[0].attrs['href'].strip()

                composite = case_dict['term'] + ' ' + case_dict['docket']
                if not self.cases.get(composite, None):
                    self.cases[composite] = {}
                self.cases[composite].update(case_dict)

    def parse_audio(self):
        for term in self.AUDIO_TERMS:
            soup = BeautifulSoup(self.audio_html[str(term)], 'lxml')
            rows = soup.select('table.datatables')[0].select('tr')[1:]

            for row in rows:

                cells = row.select('td')

                try:
                    case_dict = {}
                    case_dict['term'] = str(term)

                    # The oral audio page sometimes append text to the docket ID.
                    possible_docket = cells[0].select('a')[0].text.strip()

                    #  14-556-Question-2, 11-398-Monday
                    if "-" in possible_docket:
                        case_dict['docket'] = possible_docket.split('-')[0].strip() + '-' + possible_docket.split('-')[1].strip()

                    # 10-1491 (Reargued)
                    elif " " in possible_docket:
                        case_dict['docket'] = possible_docket.split(' ')[0].strip()

                    else:
                        case_dict['docket'] = possible_docket

                    detail_url = 'http://www.supremecourt.gov/oral_arguments' + cells[0].select('a')[0].attrs['href'].split('..')[1]

                    detail_html = requests.get(detail_url).content
                    soup = BeautifulSoup(detail_html, 'lxml')


                    case_dict['audio_mp3'] = []
                    case_dict['audio_mp3'].append(soup.select('div.datafield > table')[0].select('tr')[0].select('td')[1].select('a')[0].attrs['href'])

                    composite = case_dict['term'] + ' ' + case_dict['docket']
                    if not self.cases.get(composite, None):
                        self.cases[composite] = {}

                    # Deal with possibly multiple audio URLs.
                    if self.cases[composite].get('audio_mp3', None):
                        case_dict['audio_mp3'] = case_dict['audio_mp3'] + self.cases[composite]['audio_mp3']

                    self.cases[composite].update(case_dict)

                except IndexError:
                    pass

    def parse_arguments(self):
        for term in self.ARGUMENTS_TERMS:
            soup = BeautifulSoup(self.arguments_html[str(term)], 'lxml')
            rows = soup.select('table.datatables')[0].select('tr')[1:]
            for row in rows:

                cells = row.select('td')

                try:
                    case_dict = {}
                    case_dict['term'] = str(term)

                    # The arguments sometimes append text to the docket ID.
                    possible_docket = cells[0].select('a')[0].text.strip()

                    case_dict['docket'] = possible_docket

                    #  14-556-Question-2, 11-398-Monday
                    if "-" in possible_docket:
                        case_dict['docket'] = possible_docket.split('-')[0].strip() + '-' + possible_docket.split('-')[1].strip()

                    # 10-1491 (Reargued)
                    if " " in possible_docket:
                        case_dict['docket'] = possible_docket.split(' ')[0].strip()

                    if "." in possible_docket:
                        case_dict['docket'] = possible_docket.replace('.', '')

                    case_dict['argument_pdf'] = []
                    case_dict['argument_pdf'].append('http://www.supremecourt.gov/oral_arguments' + cells[0].select('a')[0]['href'].split('..')[1])

                    composite = case_dict['term'] + ' ' + case_dict['docket']
                    if not self.cases.get(composite, None):
                        self.cases[composite] = {}

                    # Deal with possibly multiple argument_pdf URLs.
                    if self.cases[composite].get('argument_pdf', None):
                        case_dict['argument_pdf'] = case_dict['argument_pdf'] + self.cases[composite]['argument_pdf']

                    self.cases[composite].update(case_dict)

                except IndexError:
                    pass

    def write(self):
        with open('%s/scotus_cases.json' % (self.DATA_DIRECTORY), 'w') as writefile:
            writefile.write(json.dumps([v for k,v in self.cases.items()]))

if __name__ == "__main__":
    l = Load()
    print l.start

    # Scrape
    l.scrape_opinions()
    l.scrape_audio()
    l.scrape_arguments()

    # Parse
    l.parse_opinions()
    l.parse_audio()
    l.parse_arguments()

    # Write
    l.write()

    l.end = datetime.datetime.now()
    print l.end

    l.duration = l.end - l.start
    print "Took %s" % l.duration
