# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SchoolScoutWebConnect
                                 A QGIS plugin
 Schoolscout Plugin
                             -------------------
        begin                : 2014-12-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Nathan Brewer
        email                : nathan.a.brewer@dftz.org
 ***************************************************************************/

"""


import sys, os, json, requests, fileinput
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from requests.auth import HTTPBasicAuth

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'schoolscout_dialog_base.ui'))


class SchoolScoutWebConnect():
    
    username = ""
    token = ""
    apiEndpoint = ""

    def __init__(self, parent=None):
        """Constructor."""
        settings = QSettings()
        
        self.apiEndpoint = settings.value("schoolscout/apiendpoint")
        self.username = settings.value("schoolscout/apiusername")
        self.token = settings.value("schoolscout/apitoken")

    def SSRequestHeader(self):
        return {'content-type': 'application/json', 'X-AUTH-TOKEN': self.token }

    def SSPostRequest(self, target, payload):
        url = self.apiEndpoint+target
        jsondata = json.dumps(payload)
        jsonresp = requests.post(url = url, data = jsondata, headers = self.SSRequestHeader())
        if jsonresp.status_code == 200:
            print "Response 200 - "+url
            pyresp = json.loads(jsonresp.text)
            return pyresp
        else:
            raise Exception("SSPostRequest Web Request Error " + str(jsonresp.status_code))

    def searchDistrict(self, district_name):
        url = "qgis/search/"
        request = { "district_name": district_name}
        return self.SSPostRequest(url, request)
      
    def searchDistrictByCountyId(self, county_id):
        url = "qgis/search/"
        request = { "county_id": county_id}
        return self.SSPostRequest(url, request)

    def getSchoolBoundariesByDistrict(self, district_id):
        url = "qgis/district/"+str(district_id)
        request = { "district_id": district_id}
        return self.SSPostRequest(url, request)
