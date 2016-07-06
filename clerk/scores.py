#!/usr/bin/env python

from collections import OrderedDict
import csv
import datetime
import json
import os

from nameparser import HumanName
import requests

from clerk import utils


class CourtTerm(object):

    def __init__(self, **kwargs):
        self.term = kwargs.get('term', None)
        self.med = kwargs.get('med', None)
        self.med_sd = kwargs.get('med_sd', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.justice = kwargs.get('justice', None)
        self.just_pr = kwargs.get('just_pr', None)
        self.harlan = kwargs.get('Harlan', None)
        self.black = kwargs.get('Black', None)
        self.douglas = kwargs.get('Douglas', None)
        self.stewart = kwargs.get('Stewart', None)
        self.marshall = kwargs.get('Marshall', None)
        self.brennan = kwargs.get('Brennan', None)
        self.white = kwargs.get('White', None)
        self.warren = kwargs.get('Warren', None)
        self.clark = kwargs.get('Clark', None)
        self.frankfurter = kwargs.get('Frankfurter', None)
        self.whittaker = kwargs.get('Whittaker', None)
        self.burton = kwargs.get('Burton', None)
        self.reed = kwargs.get('Reed', None)
        self.fortas = kwargs.get('Fortas', None)
        self.goldberg = kwargs.get('Goldberg', None)
        self.minton = kwargs.get('Minton', None)
        self.jackson = kwargs.get('Jackson', None)
        self.burger = kwargs.get('Burger', None)
        self.blackmun = kwargs.get('Blackmun', None)
        self.powell = kwargs.get('Powell', None)
        self.rehnquist = kwargs.get('Rehnquist', None)
        self.stevens = kwargs.get('Stevens', None)
        self.oconnor = kwargs.get('OConnor', None)
        self.scalia = kwargs.get('Scalia', None)
        self.kennedy = kwargs.get('Kennedy', None)
        self.souter = kwargs.get('Souter', None)
        self.thomas = kwargs.get('Thomas', None)
        self.ginsburg = kwargs.get('Ginsburg', None)
        self.breyer = kwargs.get('Breyer', None)
        self.rutledge = kwargs.get('Rutledge', None)
        self.murphy = kwargs.get('Murphy', None)
        self.vinson = kwargs.get('Vinson', None)
        self.byrnes = kwargs.get('Byrnes', None)
        self.sutherland = kwargs.get('Sutherland', None)
        self.cardozo = kwargs.get('Cardozo', None)
        self.brandeis = kwargs.get('Brandeis', None)
        self.butler = kwargs.get('Butler', None)
        self.mcreynolds = kwargs.get('McReynolds', None)
        self.hughes = kwargs.get('Hughes', None)
        self.oroberts = kwargs.get('ORoberts', None)
        self.stone = kwargs.get('Stone', None)
        self.roberts = kwargs.get('Roberts', None)
        self.alito = kwargs.get('Alito', None)
        self.sotomayor = kwargs.get('Sotomayor', None)
        self.kagan = kwargs.get('Kagan', None)

    def __unicode__(self):
        return "%s" % (self.term)

    def serialize(self):
        return OrderedDict((
            ('term', self.term),
            ('med', self.med),
            ('med_sd', self.med_sd),
            ('min', self.min),
            ('max', self.max),
            ('justice', self.justice),
            ('just_pr', self.just_pr),
            ('harlan', self.harlan),
            ('black', self.black),
            ('douglas', self.douglas),
            ('stewart', self.stewart),
            ('marshall', self.marshall),
            ('brennan', self.brennan),
            ('white', self.white),
            ('warren', self.warren),
            ('clark', self.clark),
            ('frankfurter', self.frankfurter),
            ('whittaker', self.whittaker),
            ('burton', self.burton),
            ('reed', self.reed),
            ('fortas', self.fortas),
            ('goldberg', self.goldberg),
            ('minton', self.minton),
            ('jackson', self.jackson),
            ('burger', self.burger),
            ('blackmun', self.blackmun),
            ('powell', self.powell),
            ('rehnquist', self.rehnquist),
            ('stevens', self.stevens),
            ('oconnor', self.oconnor),
            ('scalia', self.scalia),
            ('kennedy', self.kennedy),
            ('souter', self.souter),
            ('thomas', self.thomas),
            ('ginsburg', self.ginsburg),
            ('breyer', self.breyer),
            ('rutledge', self.rutledge),
            ('murphy', self.murphy),
            ('vinson', self.vinson),
            ('byrnes', self.byrnes),
            ('sutherland', self.sutherland),
            ('cardozo', self.cardozo),
            ('brandeis', self.brandeis),
            ('butler', self.butler),
            ('mcreynolds', self.mcreynolds),
            ('hughes', self.hughes),
            ('oroberts', self.oroberts),
            ('stone', self.stone),
            ('roberts', self.roberts),
            ('alito', self.alito),
            ('sotomayor', self.sotomayor),
            ('kagan', self.kagan),
        ))

class JusticeTerm(object):

    def __init__(self, **kwargs):
        self.term = kwargs.get('term', None)
        self.justice = kwargs.get('justice', None)
        self.justicename = kwargs.get('justiceName', None)
        self.justiceterm = "%s-%s" % (self.term, self.justice)
        self.code = kwargs.get('code', None)
        self.post_mn = kwargs.get('post_mn', None)
        self.post_sd = kwargs.get('post_sd', None)
        self.post_med = kwargs.get('post_med', None)
        self.post_025 = kwargs.get('post_025', None)
        self.post_975 = kwargs.get('post_975', None)

    def __unicode__(self):
        return "%s" % (self.justicename, self.term)

    def serialize(self):
        return OrderedDict((
            ('term', self.term),
            ('justice', self.justice),
            ('justicename', self.justicename),
            ('justiceterm', self.justiceterm),
            ('code', self.code),
            ('post_mn', self.post_mn),
            ('post_sd', self.post_sd),
            ('post_med', self.post_med),
            ('post_025', self.post_025),
            ('post_975', self.post_975),
        ))


class Justice(object):

    def __init__(self, **kwargs):
        self.justice = kwargs.get('justice', None)
        self.full_name = kwargs.get('full_name', None)
        self.chief_justice = kwargs.get('chief_justice', None)
        self.confirmation_votes_for = kwargs.get('confirmation_votes_for', None)
        self.confirmation_votes_against = kwargs.get('confirmation_votes_against', None)
        self.qualifications_score = kwargs.get('qualifications_score', None)
        self.ideology_score = kwargs.get('ideology_score', None)

    def __unicode__(self):
        return self.justice

    def serialize(self):
        return OrderedDict((
            ('justice', self.justice),
            ('full_name', self.full_name),
            ('chief_justice', self.chief_justice),
            ('confirmation_votes_for', self.confirmation_votes_for),
            ('confirmation_votes_against', self.confirmation_votes_against),
            ('qualifications_score', self.qualifications_score),
            ('ideology_score', self.ideology_score),
        ))

class Load(object):

    def __init__(self, **kwargs):
        self.MQ_JUSTICES_URL = 'http://mqscores.berkeley.edu/media/2014/justices.csv'
        self.MQ_COURTS_URL = 'http://mqscores.berkeley.edu/media/2014/court.csv'
        self.SC_JUSTICES_URL = 'https://gist.githubusercontent.com/jeremyjbowers/f36efe6db30056b1a587/raw/12c06863f944515bbd3122ac7f0461219c424edd/segal_cover_scores.csv'
        self.SCDB_JUSTICES_URL = 'https://gist.githubusercontent.com/jeremyjbowers/f36efe6db30056b1a587/raw/12c06863f944515bbd3122ac7f0461219c424edd/scdb_justices.csv'
        self.DATA_DIRECTORY = '/tmp'

        self.justices = []
        self.courts = []
        self.justice_terms = []

    def download(self):
        for filename in [
            self.MQ_JUSTICES_URL,
            self.MQ_COURTS_URL,
            self.SC_JUSTICES_URL,
            self.SCDB_JUSTICES_URL
        ]:
            r = requests.get(filename)
            filepath = self.DATA_DIRECTORY + '/' + filename.split('/')[-1]
            if not os.path.isfile(filepath):
                with open(filepath, 'w') as writefile:
                    writefile.write(r.content)

    def load(self, data_type):
        if data_type == 'justice_terms':
            with open(self.DATA_DIRECTORY + '/' + self.MQ_JUSTICES_URL.split('/')[-1], 'r') as readfile:
                for score in csv.DictReader(readfile):
                    self.justice_terms.append(JusticeTerm(**score))

        if data_type == 'justices':
            with open(self.DATA_DIRECTORY + '/' + self.SC_JUSTICES_URL.split('/')[-1], 'r') as readfile:
                for score in csv.DictReader(readfile):
                    self.justices.append(Justice(**score))

        if data_type == 'courts':
            with open(self.DATA_DIRECTORY + '/' + self.MQ_COURTS_URL.split('/')[-1], 'r') as readfile:
                for score in csv.DictReader(readfile):
                    self.courts.append(CourtTerm(**score))


    def clean(self):
        for filename in [
            self.MQ_JUSTICES_URL,
            self.MQ_COURTS_URL,
            self.SC_JUSTICES_URL,
            self.SCDB_JUSTICES_URL
        ]:
            os.system('rm -f %s/%s' % (self.DATA_DIRECTORY, filename.split('/')[-1]))
