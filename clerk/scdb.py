#!/usr/bin/env python

from collections import OrderedDict
import csv
import datetime
import json
import os

import requests

from clerk import maps
from clerk import utils


class Case(object):

    def __init__(self, **kwargs):
        self.caseid = kwargs.get('caseId', None).decode('latin-1')
        self.docketid = kwargs.get('docketId', None).decode('latin-1')
        self.caseissuesid = kwargs.get('caseIssuesId', None).decode('latin-1')
        self.datedecision = kwargs.get('dateDecision', None).decode('latin-1')
        self.decisiontype = kwargs.get('decisionType', None).decode('latin-1')
        self.uscite = kwargs.get('usCite', None).decode('latin-1')
        self.sctcite = kwargs.get('sctCite', None).decode('latin-1')
        self.ledcite = kwargs.get('ledCite', None).decode('latin-1')
        self.lexiscite = kwargs.get('lexisCite', None).decode('latin-1')
        self.term = kwargs.get('term', None).decode('latin-1')
        self.naturalcourt = kwargs.get('naturalCourt', None).decode('latin-1')
        self.chief = kwargs.get('chief', None).decode('latin-1')
        self.docket = kwargs.get('docket', None).decode('latin-1')
        self.casename = kwargs.get('caseName', None).decode('latin-1')
        self.dateargument = kwargs.get('dateArgument', None).decode('latin-1')
        self.datereargument = kwargs.get('dateRearg', None).decode('latin-1')
        self.petitioner = kwargs.get('petitioner', None).decode('latin-1')
        self.petitionerstate = kwargs.get('petitionerState', None).decode('latin-1')
        self.respondent = kwargs.get('respondent', None).decode('latin-1')
        self.respondentstate = kwargs.get('respondentState', None).decode('latin-1')
        self.jurisdiction = kwargs.get('jurisdiction', None).decode('latin-1')
        self.adminaction = kwargs.get('adminAction', None).decode('latin-1')
        self.adminactionstate = kwargs.get('adminActionState', None).decode('latin-1')
        self.threejudgefdc = kwargs.get('threeJudgeFdc', None).decode('latin-1')
        self.caseorigin = kwargs.get('caseOrigin', None).decode('latin-1')
        self.caseoriginstate = kwargs.get('caseOriginState', None).decode('latin-1')
        self.casesource = kwargs.get('caseSource', None).decode('latin-1')
        self.casesourcestate = kwargs.get('caseSourceState', None).decode('latin-1')
        self.lcdisagreement = kwargs.get('lcDisagreement', None).decode('latin-1')
        self.certreason = kwargs.get('certReason', None).decode('latin-1')
        self.lcdisposition = kwargs.get('lcDisposition', None).decode('latin-1')
        self.lcdispositiondirection = kwargs.get('lcDispositionDirection', None).decode('latin-1')
        self.declarationuncon = kwargs.get('declarationUncon', None).decode('latin-1')
        self.casedisposition = kwargs.get('caseDisposition', None).decode('latin-1')
        self.casedispositionunusual = kwargs.get('caseDispositionUnusual', None).decode('latin-1')
        self.partywinning = kwargs.get('partyWinning', None).decode('latin-1')
        self.precedentalteration = kwargs.get('precedentAlteration', None).decode('latin-1')
        self.voteunclear = kwargs.get('voteUnclear', None).decode('latin-1')
        self.issue = kwargs.get('issue', None).decode('latin-1')
        self.issuearea = kwargs.get('issueArea', None).decode('latin-1')
        self.decisiondirection = kwargs.get('decisionDirection', None).decode('latin-1')
        self.decisiondirectiondissent = kwargs.get('decisionDirectionDissent', None).decode('latin-1')
        self.authoritydecision1 = kwargs.get('authorityDecision1', None).decode('latin-1')
        self.authoritydecision2 = kwargs.get('authorityDecision2', None).decode('latin-1')
        self.lawtype = kwargs.get('lawType', None).decode('latin-1')
        self.lawsupp = kwargs.get('lawSupp', None).decode('latin-1')
        self.lawminor = kwargs.get('lawMinor', None).decode('latin-1')
        self.majopinwriter = kwargs.get('majOpinWriter', None).decode('latin-1')
        self.majopinassigner = kwargs.get('majOpinAssigner', None).decode('latin-1')
        self.splitvote = kwargs.get('splitVote', None).decode('latin-1')
        self.majvotes = kwargs.get('majVotes', None).decode('latin-1')
        self.minvotes = kwargs.get('minVotes', None).decode('latin-1')
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
        self.caseid = kwargs['caseId'].decode('latin-1')
        self.docketid = kwargs['docketId'].decode('latin-1')
        self.caseissuesid = kwargs['caseIssuesId'].decode('latin-1')
        self.voteid = kwargs['voteId'].decode('latin-1')
        self.datedecision = kwargs['dateDecision'].decode('latin-1')
        self.decisiontype = kwargs['decisionType'].decode('latin-1')
        self.uscite = kwargs['usCite'].decode('latin-1')
        self.sctcite = kwargs['sctCite'].decode('latin-1')
        self.ledcite = kwargs['ledCite'].decode('latin-1')
        self.lexiscite = kwargs['lexisCite'].decode('latin-1')
        self.term = kwargs['term'].decode('latin-1')
        self.naturalcourt = kwargs['naturalCourt'].decode('latin-1')
        self.chief = kwargs['chief'].decode('latin-1')
        self.docket = kwargs['docket'].decode('latin-1')
        self.casename = kwargs['caseName'].decode('latin-1')
        self.dateargument = kwargs['dateArgument'].decode('latin-1')
        self.datereargument = kwargs['dateRearg'].decode('latin-1')
        self.petitioner = kwargs['petitioner'].decode('latin-1')
        self.petitionerstate = kwargs['petitionerState'].decode('latin-1')
        self.respondent = kwargs['respondent'].decode('latin-1')
        self.respondentstate = kwargs['respondentState'].decode('latin-1')
        self.jurisdiction = kwargs['jurisdiction'].decode('latin-1')
        self.adminaction = kwargs['adminAction'].decode('latin-1')
        self.adminactionstate = kwargs['adminActionState'].decode('latin-1')
        self.threejudgefdc = kwargs['threeJudgeFdc'].decode('latin-1')
        self.caseorigin = kwargs['caseOrigin'].decode('latin-1')
        self.caseoriginstate = kwargs['caseOriginState'].decode('latin-1')
        self.casesource = kwargs['caseSource'].decode('latin-1')
        self.casesourcestate = kwargs['caseSourceState'].decode('latin-1')
        self.lcdisagreement = kwargs['lcDisagreement'].decode('latin-1')
        self.certreason = kwargs['certReason'].decode('latin-1')
        self.lcdisposition = kwargs['lcDisposition'].decode('latin-1')
        self.lcdispositiondirection = kwargs['lcDispositionDirection'].decode('latin-1')
        self.declarationuncon = kwargs['declarationUncon'].decode('latin-1')
        self.casedisposition = kwargs['caseDisposition'].decode('latin-1')
        self.casedispositionunusual = kwargs['caseDispositionUnusual'].decode('latin-1')
        self.partywinning = kwargs['partyWinning'].decode('latin-1')
        self.precedentalteration = kwargs['precedentAlteration'].decode('latin-1')
        self.voteunclear = kwargs['voteUnclear'].decode('latin-1')
        self.issue = kwargs['issue'].decode('latin-1')
        self.issuearea = kwargs['issueArea'].decode('latin-1')
        self.decisiondirection = kwargs['decisionDirection'].decode('latin-1')
        self.decisiondirectiondissent = kwargs['decisionDirectionDissent'].decode('latin-1')
        self.authoritydecision1 = kwargs['authorityDecision1'].decode('latin-1')
        self.authoritydecision2 = kwargs['authorityDecision2'].decode('latin-1')
        self.lawtype = kwargs['lawType'].decode('latin-1')
        self.lawsupp = kwargs['lawSupp'].decode('latin-1')
        self.lawminor = kwargs['lawMinor'].decode('latin-1')
        self.majopinwriter = kwargs['majOpinWriter'].decode('latin-1')
        self.majopinassigner = kwargs['majOpinAssigner'].decode('latin-1')
        self.splitvote = kwargs['splitVote'].decode('latin-1')
        self.majvotes = kwargs['majVotes'].decode('latin-1')
        self.minvotes = kwargs['minVotes'].decode('latin-1')
        self.justice = kwargs['justice'].decode('latin-1')
        self.justicename = kwargs['justiceName'].decode('latin-1')
        self.vote = kwargs['vote'].decode('latin-1')
        self.opinion = kwargs['opinion'].decode('latin-1')
        self.direction = kwargs['direction'].decode('latin-1')
        self.majority = kwargs['majority'].decode('latin-1')
        self.firstagreement = kwargs['firstAgreement'].decode('latin-1')
        self.secondagreement = kwargs['secondAgreement'].decode('latin-1')
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
       'votes': {
            'url': 'http://scdb.wustl.edu/_brickFiles/Legacy_01/SCDB_Legacy_01_justiceCentered_Citation.csv.zip',
            'filename': 'SCDB_Legacy_01_justiceCentered_Citation'
        },
        'cases': {
            'url': 'http://scdb.wustl.edu/_brickFiles/Legacy_01/SCDB_Legacy_01_caseCentered_Citation.csv.zip',
            'filename': 'SCDB_Legacy_01_caseCentered_Citation'
        }
    }

    def __init__(self, **kwargs):
        self.data_directory = kwargs.get('data_directory', '/tmp')
        self.votes = []
        self.cases = []

    def download(self):
        for data_type in ['votes', 'cases']:
            file_path = '%s/%s.csv.zip' % (
                self.data_directory,
                self.DATA_MAP[data_type]['filename']
            )
            if not os.path.isfile(file_path):
                r = requests.get(self.DATA_MAP[data_type]['url'])
                with open(file_path, 'w') as writefile:
                    writefile.write(r.content)

    def unzip(self):
        for data_type in ['votes', 'cases']:
            file_path = '%s/%s.csv' % (
                self.data_directory,
                self.DATA_MAP[data_type]['filename']
            )
            if not os.path.isfile(file_path):
                os.system('unzip %s -d %s' % (file_path, self.data_directory))

    def load(self, data_type):
            file_path = '%s/%s.csv' % (
                self.data_directory,
                self.DATA_MAP[data_type]['filename']
            )
            if os.path.isfile(file_path):
                with open(file_path, 'rU') as readfile:
                    if data_type == 'votes':
                        self.votes = list([
                            Vote(**r) for r in list([v for v in csv.DictReader(readfile) if v['voteId'].strip() != '' and v['voteId'].strip() != 'NULL'])
                        ])
                        self.votes = [v for v in self.votes if v.voteid]
                    if data_type == 'cases':
                        self.cases = list([
                            Case(**r) for r in list([c for c in csv.DictReader(readfile) if c['caseId'].strip() != '' and c['caseId'].strip() != 'NULL'])
                        ])

    def clean(self):
        os.system('rm -f %s/SCDB_Legacy_01_*Centered_Citation.csv.zip' %
            self.data_directory)
