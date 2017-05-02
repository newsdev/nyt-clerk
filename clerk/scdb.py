#!/usr/bin/env python

from collections import OrderedDict
import codecs
import csv
import datetime
import json
import os

import requests

from clerk import maps
from clerk import utils


class Case(object):

    def __init__(self, **kwargs):
        self.caseid = kwargs.get('caseId', None)
        self.docketid = kwargs.get('docketId', None)
        self.caseissuesid = kwargs.get('caseIssuesId', None)
        self.datedecision = kwargs.get('dateDecision', None)
        self.decisiontype = kwargs.get('decisionType', None)
        self.uscite = kwargs.get('usCite', None)
        self.sctcite = kwargs.get('sctCite', None)
        self.ledcite = kwargs.get('ledCite', None)
        self.lexiscite = kwargs.get('lexisCite', None)
        self.term = kwargs.get('term', None)
        self.naturalcourt = kwargs.get('naturalCourt', None)
        self.chief = kwargs.get('chief', None)
        self.docket = kwargs.get('docket', None)
        self.casename = kwargs.get('caseName', None)
        self.dateargument = kwargs.get('dateArgument', None)
        self.datereargument = kwargs.get('dateRearg', None)
        self.petitioner = kwargs.get('petitioner', None)
        self.petitionerstate = kwargs.get('petitionerState', None)
        self.respondent = kwargs.get('respondent', None)
        self.respondentstate = kwargs.get('respondentState', None)
        self.jurisdiction = kwargs.get('jurisdiction', None)
        self.adminaction = kwargs.get('adminAction', None)
        self.adminactionstate = kwargs.get('adminActionState', None)
        self.threejudgefdc = kwargs.get('threeJudgeFdc', None)
        self.caseorigin = kwargs.get('caseOrigin', None)
        self.caseoriginstate = kwargs.get('caseOriginState', None)
        self.casesource = kwargs.get('caseSource', None)
        self.casesourcestate = kwargs.get('caseSourceState', None)
        self.lcdisagreement = kwargs.get('lcDisagreement', None)
        self.certreason = kwargs.get('certReason', None)
        self.lcdisposition = kwargs.get('lcDisposition', None)
        self.lcdispositiondirection = kwargs.get('lcDispositionDirection', None)
        self.declarationuncon = kwargs.get('declarationUncon', None)
        self.casedisposition = kwargs.get('caseDisposition', None)
        self.casedispositionunusual = kwargs.get('caseDispositionUnusual', None)
        self.partywinning = kwargs.get('partyWinning', None)
        self.precedentalteration = kwargs.get('precedentAlteration', None)
        self.voteunclear = kwargs.get('voteUnclear', None)
        self.issue = kwargs.get('issue', None)
        self.issuearea = kwargs.get('issueArea', None)
        self.decisiondirection = kwargs.get('decisionDirection', None)
        self.decisiondirectiondissent = kwargs.get('decisionDirectionDissent', None)
        self.authoritydecision1 = kwargs.get('authorityDecision1', None)
        self.authoritydecision2 = kwargs.get('authorityDecision2', None)
        self.lawtype = kwargs.get('lawType', None)
        self.lawsupp = kwargs.get('lawSupp', None)
        self.lawminor = kwargs.get('lawMinor', None)
        self.majopinwriter = kwargs.get('majOpinWriter', None)
        self.majopinassigner = kwargs.get('majOpinAssigner', None)
        self.splitvote = kwargs.get('splitVote', None)
        self.majvotes = kwargs.get('majVotes', None)
        self.minvotes = kwargs.get('minVotes', None)
        self.weighted_majvotes = 0

        try:
            self.majvotes = int(self.majvotes)
        except ValueError:
            self.majvotes = 0

        try:
            self.minvotes = int(self.minvotes)
        except ValueError:
            self.minvotes = 0

        def weight_majvotes(obj):
            if ((int(self.majvotes) + int(self.minvotes)) < 9):
                """
                We assume missing justices voted with the majority.
                4 minority votes = 0 weighted votes.
                """
                WEIGHTED_VOTES = (9,8,7,6,0)
                return WEIGHTED_VOTES[int(self.minvotes)]
            return int(self.majvotes)

        if self.decisiondirection == "1":
            self.weighted_majvotes = weight_majvotes(self)
        elif self.decisiondirection == "2":
            self.weighted_majvotes = weight_majvotes(self) * -1
        elif self.decisiondirection == "3":
            self.weighted_majvotes = 0

    def __unicode__(self):
        return "%s" % self.case

    def serialize(self):
        return OrderedDict((
            ('caseid', self.caseid),
            ('docketid', self.docketid),
            ('caseissuesid', self.caseissuesid),
            ('datedecision', self.datedecision),
            ('decisiontype', self.decisiontype),
            ('uscite', self.uscite),
            ('sctcite', self.sctcite),
            ('ledcite', self.ledcite),
            ('lexiscite', self.lexiscite),
            ('term', self.term),
            ('naturalcourt', self.naturalcourt),
            ('chief', self.chief),
            ('docket', self.docket),
            ('casename', self.casename),
            ('dateargument', self.dateargument),
            ('datereargument', self.datereargument),
            ('petitioner', self.petitioner),
            ('petitionerstate', self.petitionerstate),
            ('respondent', self.respondent),
            ('respondentstate', self.respondentstate),
            ('jurisdiction', self.jurisdiction),
            ('adminaction', self.adminaction),
            ('adminactionstate', self.adminactionstate),
            ('threejudgefdc', self.threejudgefdc),
            ('caseorigin', self.caseorigin),
            ('caseoriginstate', self.caseoriginstate),
            ('casesource', self.casesource),
            ('casesourcestate', self.casesourcestate),
            ('lcdisagreement', self.lcdisagreement),
            ('certreason', self.certreason),
            ('lcdisposition', self.lcdisposition),
            ('lcdispositiondirection', self.lcdispositiondirection),
            ('declarationuncon', self.declarationuncon),
            ('casedisposition', self.casedisposition),
            ('casedispositionunusual', self.casedispositionunusual),
            ('partywinning', self.partywinning),
            ('precedentalteration', self.precedentalteration),
            ('voteunclear', self.voteunclear),
            ('issue', self.issue),
            ('issuearea', self.issuearea),
            ('decisiondirection', self.decisiondirection),
            ('decisiondirectiondissent', self.decisiondirectiondissent),
            ('authoritydecision1', self.authoritydecision1),
            ('authoritydecision2', self.authoritydecision2),
            ('lawtype', self.lawtype),
            ('lawsupp', self.lawsupp),
            ('lawminor', self.lawminor),
            ('majopinwriter', self.majopinwriter),
            ('majopinassigner', self.majopinassigner),
            ('splitvote', self.splitvote),
            ('majvotes', self.majvotes),
            ('minvotes', self.minvotes),
            ('weighted_majvotes', self.weighted_majvotes)
        ))

class Vote(object):

    def __init__(self, **kwargs):
        self.caseid = kwargs['caseId']
        self.docketid = kwargs['docketId']
        self.caseissuesid = kwargs['caseIssuesId']
        self.voteid = kwargs['voteId']
        self.datedecision = kwargs['dateDecision']
        self.decisiontype = kwargs['decisionType']
        self.uscite = kwargs['usCite']
        self.sctcite = kwargs['sctCite']
        self.ledcite = kwargs['ledCite']
        self.lexiscite = kwargs['lexisCite']
        self.term = kwargs['term']
        self.naturalcourt = kwargs['naturalCourt']
        self.chief = kwargs['chief']
        self.docket = kwargs['docket']
        self.casename = kwargs['caseName']
        self.dateargument = kwargs['dateArgument']
        self.datereargument = kwargs['dateRearg']
        self.petitioner = kwargs['petitioner']
        self.petitionerstate = kwargs['petitionerState']
        self.respondent = kwargs['respondent']
        self.respondentstate = kwargs['respondentState']
        self.jurisdiction = kwargs['jurisdiction']
        self.adminaction = kwargs['adminAction']
        self.adminactionstate = kwargs['adminActionState']
        self.threejudgefdc = kwargs['threeJudgeFdc']
        self.caseorigin = kwargs['caseOrigin']
        self.caseoriginstate = kwargs['caseOriginState']
        self.casesource = kwargs['caseSource']
        self.casesourcestate = kwargs['caseSourceState']
        self.lcdisagreement = kwargs['lcDisagreement']
        self.certreason = kwargs['certReason']
        self.lcdisposition = kwargs['lcDisposition']
        self.lcdispositiondirection = kwargs['lcDispositionDirection']
        self.declarationuncon = kwargs['declarationUncon']
        self.casedisposition = kwargs['caseDisposition']
        self.casedispositionunusual = kwargs['caseDispositionUnusual']
        self.partywinning = kwargs['partyWinning']
        self.precedentalteration = kwargs['precedentAlteration']
        self.voteunclear = kwargs['voteUnclear']
        self.issue = kwargs['issue']
        self.issuearea = kwargs['issueArea']
        self.decisiondirection = kwargs['decisionDirection']
        self.decisiondirectiondissent = kwargs['decisionDirectionDissent']
        self.authoritydecision1 = kwargs['authorityDecision1']
        self.authoritydecision2 = kwargs['authorityDecision2']
        self.lawtype = kwargs['lawType']
        self.lawsupp = kwargs['lawSupp']
        self.lawminor = kwargs['lawMinor']
        self.majopinwriter = kwargs['majOpinWriter']
        self.majopinassigner = kwargs['majOpinAssigner']
        self.splitvote = kwargs['splitVote']
        self.majvotes = kwargs['majVotes']
        self.minvotes = kwargs['minVotes']
        self.justice = kwargs['justice']
        self.justicename = kwargs['justiceName']
        self.vote = kwargs['vote']
        self.opinion = kwargs['opinion']
        self.direction = kwargs['direction']
        self.majority = kwargs['majority']
        self.firstagreement = kwargs['firstAgreement']
        self.secondagreement = kwargs['secondAgreement']
        self.weighted_majvotes = 0

        try:
            self.majvotes = int(self.majvotes)
        except ValueError:
            self.majvotes = 0

        try:
            self.minvotes = int(self.minvotes)
        except ValueError:
            self.minvotes = 0

        def weight_majvotes(obj):
            if ((int(self.majvotes) + int(self.minvotes)) < 9):
                """
                We assume missing justices voted with the majority.
                4 minority votes = 0 weighted votes.
                """
                WEIGHTED_VOTES = (9,8,7,6,0)
                return WEIGHTED_VOTES[int(self.minvotes)]
            return int(self.majvotes)

        if self.decisiondirection == "1":
            self.weighted_majvotes = weight_majvotes(self)
        elif self.decisiondirection == "2":
            self.weighted_majvotes = weight_majvotes(self) * -1
        elif self.decisiondirection == "3":
            self.weighted_majvotes = 0

    def __unicode__(self):
        return "%s, %s" % (self.justice, self.case)

    def serialize(self):
        return OrderedDict((
            ('caseid', self.caseid),
            ('docketid', self.docketid),
            ('caseissuesid', self.caseissuesid),
            ('voteid', self.voteid),
            ('datedecision', self.datedecision),
            ('decisiontype', self.decisiontype),
            ('uscite', self.uscite),
            ('sctcite', self.sctcite),
            ('ledcite', self.ledcite),
            ('lexiscite', self.lexiscite),
            ('term', self.term),
            ('naturalcourt', self.naturalcourt),
            ('chief', self.chief),
            ('docket', self.docket),
            ('casename', self.casename),
            ('dateargument', self.dateargument),
            ('datereargument', self.datereargument),
            ('petitioner', self.petitioner),
            ('petitionerstate', self.petitionerstate),
            ('respondent', self.respondent),
            ('respondentstate', self.respondentstate),
            ('jurisdiction', self.jurisdiction),
            ('adminaction', self.adminaction),
            ('adminactionstate', self.adminactionstate),
            ('threejudgefdc', self.threejudgefdc),
            ('caseorigin', self.caseorigin),
            ('caseoriginstate', self.caseoriginstate),
            ('casesource', self.casesource),
            ('casesourcestate', self.casesourcestate),
            ('lcdisagreement', self.lcdisagreement),
            ('certreason', self.certreason),
            ('lcdisposition', self.lcdisposition),
            ('lcdispositiondirection', self.lcdispositiondirection),
            ('declarationuncon', self.declarationuncon),
            ('casedisposition', self.casedisposition),
            ('casedispositionunusual', self.casedispositionunusual),
            ('partywinning', self.partywinning),
            ('precedentalteration', self.precedentalteration),
            ('voteunclear', self.voteunclear),
            ('issue', self.issue),
            ('issuearea', self.issuearea),
            ('decisiondirection', self.decisiondirection),
            ('decisiondirectiondissent', self.decisiondirectiondissent),
            ('authoritydecision1', self.authoritydecision1),
            ('authoritydecision2', self.authoritydecision2),
            ('lawtype', self.lawtype),
            ('lawsupp', self.lawsupp),
            ('lawminor', self.lawminor),
            ('majopinwriter', self.majopinwriter),
            ('majopinassigner', self.majopinassigner),
            ('splitvote', self.splitvote),
            ('majvotes', self.majvotes),
            ('minvotes', self.minvotes),
            ('justice', self.justice),
            ('justicename', self.justicename),
            ('vote', self.vote),
            ('opinion', self.opinion),
            ('direction', self.direction),
            ('majority', self.majority),
            ('firstagreement', self.firstagreement),
            ('secondagreement', self.secondagreement),
            ('weighted_majvotes', self.weighted_majvotes)
        ))


class Load(object):
    DATA_MAP = {
       'votes': [
            {
                'url': 'http://scdb.wustl.edu/_brickFiles/Legacy_03/SCDB_Legacy_03_justiceCentered_Citation.csv.zip',
                'filename': 'SCDB_Legacy_03_justiceCentered_Citation'
            },
            {
                'url': 'http://scdb.wustl.edu/_brickFiles/2016_01/SCDB_2016_01_justiceCentered_Citation.csv.zip',
                'filename': 'SCDB_2016_01_justiceCentered_Citation'
            },
        ],
        'cases': [
            {
                'url': 'http://scdb.wustl.edu/_brickFiles/Legacy_03/SCDB_Legacy_03_caseCentered_Citation.csv.zip',
                'filename': 'SCDB_Legacy_03_caseCentered_Citation'
            },
            {
                'url': 'http://scdb.wustl.edu/_brickFiles/2016_01/SCDB_2016_01_caseCentered_Citation.csv.zip',
                'filename': 'SCDB_2016_01_caseCentered_Citation'
            },
        ]
    }

    def __init__(self, **kwargs):
        self.data_directory = kwargs.get('data_directory', '/tmp')
        self.votes = []
        self.cases = []

    def download(self):
        for data_type in ['votes', 'cases']:
            for data_set in self.DATA_MAP[data_type]:
                file_path = '%s/%s.csv.zip' % (
                    self.data_directory,
                    data_set['filename']
                )
                if not os.path.isfile(file_path):
                    os.system('curl -o %s %s' % (file_path, data_set['url']))

    def unzip(self):
        for data_type in ['votes', 'cases']:
            for data_set in self.DATA_MAP[data_type]:
                file_path = '%s/%s.csv' % (
                    self.data_directory,
                    data_set['filename']
                )
                if not os.path.isfile(file_path):
                    os.system('unzip %s.zip -d %s' % (file_path, self.data_directory))

    def load(self, data_type):
        for data_set in self.DATA_MAP[data_type]:
            file_path = '%s/%s.csv' % (
                self.data_directory,
                data_set['filename']
            )
            if os.path.isfile(file_path):
                with open(file_path, 'rU', encoding='latin-1') as readfile:

                    if data_type == 'votes':
                        self.votes.extend(list([
                            Vote(**r) for r in list([v for v in csv.DictReader(readfile) if v['voteId'].strip() != '' and v['voteId'].strip() != 'NULL'])
                        ]))
                        self.votes = [v for v in self.votes if v.voteid]

                    if data_type == 'cases':
                        self.cases.extend(list([
                            Case(**r) for r in list([c for c in csv.DictReader(readfile) if c['caseId'].strip() != '' and c['caseId'].strip() != 'NULL'])
                        ]))
