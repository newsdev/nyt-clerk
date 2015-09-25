#!/usr/bin/env python

import csv
import datetime
import json
import os

from nameparser import HumanName
import requests

from clerk import utils


class BaseObject(object):

    def set_data_directory(self):
        if not os.path.exists(self.DATA_DIRECTORY):
            os.system('mkdir -p %s' % self.DATA_DIRECTORY)

    def set_fields(self, **kwargs):
        fieldnames = self.__dict__.keys()
        for k,v in kwargs.items():
            k = k.lower().strip()
            v = unicode(v.decode('utf-8'))
            if k in fieldnames:
                setattr(self, k, v)

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class CourtTerm(BaseObject):

    def __init__(self, **kwargs):
        self.term = None
        self.martin_quinn_score = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return "%s" % (self.term)


class JusticeTerm(BaseObject):

    def __init__(self, **kwargs):
        self.justice = None
        self.term = None
        self.martin_quinn_score = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return "%s (%s)" % (self.justice, self.term)


class Justice(BaseObject):

    def __init__(self, **kwargs):
        self.justice = None
        self.full_name = None
        self.first_name = None
        self.last_name = None
        self.segal_cover_ideology_score = None
        self.segal_cover_qualification_score = None

        self.set_fields(**kwargs)

    def __unicode__(self):
        return self.justice


class Load(BaseObject):

    def __init__(self, **kwargs):
        self.MQ_JUSTICES_URL = 'http://mqscores.berkeley.edu/media/2014/justices.csv'
        self.MQ_COURTS_URL = 'http://mqscores.berkeley.edu/media/2014/court.csv'
        self.SC_JUSTICES_URL = 'https://gist.githubusercontent.com/jeremyjbowers/f36efe6db30056b1a587/raw/0700af18dc3f0a14bf1a011d0cc2e24ebb36576d/segal_cover_scores.csv'
        self.DATA_DIRECTORY = os.path.join(os.path.realpath(__file__).split(__file__.split('/')[-1])[0], 'data')

        self.justices = []
        self.courtterms = []
        self.justiceterms = []
        self.start = datetime.datetime.now()
        self.set_data_directory()

    def download(self):
        for filename in [self.MQ_JUSTICES_URL, self.MQ_COURTS_URL, self.SC_JUSTICES_URL]:
            r = requests.get(filename)
            with open(self.DATA_DIRECTORY + '/' + filename.split('/')[-1], 'w') as writefile:
                writefile.write(r.content)

    def load(self):
        with open(self.DATA_DIRECTORY + '/' + self.MQ_JUSTICES_URL.split('/')[-1], 'r') as readfile:
            justice_terms = list(csv.DictReader(readfile))

        for score in justice_terms:
            score_dict = {}
            score_dict['martin_quinn_score'] = score['post_mn']
            score_dict['justice'] = score['justice']
            score_dict['term'] = score['term']
            self.justiceterms.append(JusticeTerm(**score_dict))

        with open(self.DATA_DIRECTORY + '/' + self.MQ_COURTS_URL.split('/')[-1], 'r') as readfile:
            court_scores = list(csv.DictReader(readfile))

        for score in court_scores:
            score_dict = {}
            score_dict['term'] = score['term']
            score_dict['martin_quinn_score'] = score['med']
            score_dict['median_justice'] = score['justice']
            self.courtterms.append(CourtTerm(**score_dict))

        with open(self.DATA_DIRECTORY + '/' + self.SC_JUSTICES_URL.split('/')[-1], 'r') as readfile:
            justice_scores = list(csv.DictReader(readfile))

        for score in justice_scores:
            if score['justice']:
                score_dict = {}
                score_dict['justice'] = score['justice']
                score_dict['full_name'] = unicode(score['full_name'].decode('utf-8')).strip()
                score_dict['last_name'] = HumanName(score_dict['full_name']).last
                score_dict['first_name'] = HumanName(score_dict['full_name']).first
                score_dict['segal_cover_ideology_score'] = score['ideology_score']
                score_dict['segal_cover_qualification_score'] = score['qualifications_score']
                self.justices.append(Justice(**score_dict))

    def write(self):
        with open('%s/scores_justiceterms.json' % (self.DATA_DIRECTORY), 'w') as writefile:
            writefile.write(json.dumps([c.__dict__ for c in self.justiceterms]))

        with open('%s/scores_justices.json' % (self.DATA_DIRECTORY), 'w') as writefile:
            writefile.write(json.dumps([j.__dict__ for j in self.justices]))

        with open('%s/scores_courtterms.json' % (self.DATA_DIRECTORY), 'w') as writefile:
            writefile.write(json.dumps([v.__dict__ for v in self.courtterms]))

    def clean(self):
        for filename in [self.MQ_JUSTICES_URL, self.MQ_COURTS_URL, self.SC_JUSTICES_URL]:
            os.system('rm -f %s/%s' % (self.DATA_DIRECTORY, filename.split('/')[-1]))

if __name__ == "__main__":
    l = Load()
    print l.start

    l.download()
    l.load()
    l.write()
    l.clean()

    l.end = datetime.datetime.now()
    print l.end

    l.duration = l.end - l.start
    print "Took %s" % l.duration
