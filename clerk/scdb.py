#!/usr/bin/env python

import csv
import datetime
import json
import os

import requests

from clerk import maps
from clerk import utils


class BaseObject(object):
    SCDB_URL = 'http://scdb.wustl.edu/_brickFiles/2015_01/SCDB_2015_01_justiceCentered_Citation.csv.zip'
    SCDB_FILENAME = SCDB_URL.split('/')[-1].split('.')[0]
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


class NaturalCourt(BaseObject):
    def __init__(self, **kwargs):
        self.naturalcourt = None
        self.common_name = None
        self.start_date = None
        self.end_date = None

        self.set_fields(**kwargs)

        def __unicode__(self):
            return self.common_name


class Vote(BaseObject):

    def __init__(self, **kwargs):
        self.justice = None
        self.justicename = None
        self.caseid = None
        self.docketid = None
        self.caseissuesid = None
        self.casename = None
        self.vote = None
        self.opinion = None
        self.direction = None
        self.majority = None
        self.firstagreement = None
        self.secondagreement = None
        self.voteid = None
        self.term = None
        self.naturalcourt = None
        self.majvotes = None
        self.minvotes = None
        self.decisiondirection = None
        self.nyt_weighted_majvotes = None
        self.decisiontype = None
        self.majvotes = None
        self.minvotes = None
        self.datedecision = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return "%s, %s" % (self.justice, self.case)


class Justice(BaseObject):

    def __init__(self, **kwargs):
        self.justice = None
        self.justicename = None
        self.current = False
        self.first_name = None
        self.last_name = None
        self.active_terms = None
        self.nominated = None
        self.confirmed = None
        self.sworn_in = None
        self.was_chief = False
        self.first_term = None
        self.last_term = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return self.justicename

class MeritsCase(BaseObject):

    def __init__(self, **kwargs):
        self.term = None
        self.docket = None
        self.caseid = None
        self.docketid = None
        self.caseissuesid = None
        self.uscite = None
        self.sctcite = None
        self.ledcite = None
        self.lexiscite = None
        self.chief = None
        self.casename = None
        self.lawminor = None
        self.majopinwriter = None
        self.majopinassigner = None
        self.majvotes = None
        self.minvotes = None
        self.datedecision = None
        self.dateargument = None
        self.daterearg = None
        self.decisiontype = None
        self.naturalcourt = None
        self.petitioner = None
        self.petitionerstate = None
        self.respondent = None
        self.respondentstate = None
        self.jurisdiction = None
        self.adminaction = None
        self.adminactionstate = None
        self.threejudgefdc = None
        self.caseorigin = None
        self.caseoriginstate = None
        self.casesource = None
        self.casesourcestate = None
        self.certreason = None
        self.lcdisagreement = None
        self.lcdisposition = None
        self.lcdispositiondirection = None
        self.lcdecisiondirection = None
        self.declarationuncon = None
        self.casedisposition = None
        self.casedispositionunusual = None
        self.partywinning = None
        self.precedentalteration = None
        self.voteunclear = None
        self.issue = None
        self.issuearea = None
        self.decisiondirection = None
        self.decisiondirectiondissent = None
        self.authoritydecision1 = None
        self.authoritydecision2 = None
        self.lawtype = None
        self.lawsupp = None
        self.splitvote = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return "(%s) %s" % (self.term, self.casename)

class Load(BaseObject):

    def __init__(self, **kwargs):
        self.file_path = self.DATA_DIRECTORY + '/' + self.SCDB_FILENAME + '.csv'
        self.cases = []
        self.justices = []
        self.naturalcourts = []
        self.votes = []
        self.start = datetime.datetime.now()
        self.set_data_directory()

    def download(self):
        r = requests.get(self.SCDB_URL)

        with open('%s/%s.csv.zip' % (self.DATA_DIRECTORY, self.SCDB_FILENAME), 'w') as writefile:
            writefile.write(r.content)

        os.system('unzip %s/%s.csv.zip -d %s' % (self.DATA_DIRECTORY, self.SCDB_FILENAME, self.DATA_DIRECTORY))

    def load(self):
        with open(self.file_path, 'rU') as readfile:
            rows = list(csv.DictReader(readfile))

        processed_cases = []
        processed_naturalcourts = []
        processed_justices = []

        for row in rows:
            v = Vote(**row)
            v = utils.set_weighted_majvotes(v)
            self.votes.append(v)

            if row['docketId'] not in processed_cases:
                m = MeritsCase(**row)
                m = utils.set_weighted_majvotes(m)
                self.cases.append(m)
                processed_cases.append(row['docketId'])

            if row['justice'] not in processed_justices:
                self.justices.append(Justice(**row))
                processed_justices.append(row['justice'])

            if row['naturalCourt'] not in processed_naturalcourts:
                n = NaturalCourt(**row)
                for court in maps.NATURAL_COURT_CHOICES:
                    if court[0] == n.naturalcourt:
                        n.common_name = court[1]
                n.start_date = n.common_name.split(":")[1].split(' - ')[0].strip()
                try:
                    n.end_date = n.common_name.split(":")[1].split(' - ')[1].strip()
                except:
                    n.end_date = None

                self.naturalcourts.append(n)
                processed_naturalcourts.append(row['naturalCourt'])


    def clean(self):
        os.system('rm -f %s/%s.*' % (self.DATA_DIRECTORY, self.SCDB_FILENAME))

if __name__ == "__main__":
    l = Load()
    print l.start

    l.download()
    l.load()
    l.clean()

    l.end = datetime.datetime.now()
    print l.end

    l.duration = l.end - l.start
    print "Took %s" % l.duration
