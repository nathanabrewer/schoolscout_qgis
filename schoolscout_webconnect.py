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
    
    token = ""

    def SSRequestHeader(self):
        return {'content-type': 'application/json', 'X-AUTH-TOKEN': self.token }

    def SSPostRequest(self, url, payload):
        jsondata = json.dumps(payload)
        jsonresp = requests.post(url = url, data = jsondata, headers = self.SSRequestHeader())
        if jsonresp.status_code == 200:
            print "Response 200 - "+url
            pyresp = json.loads(jsonresp.text)
            return pyresp
        else:
            raise Exception("SSPostRequest Web Request Error " + str(jsonresp.status_code))

    def searchDistrict(self, district_name):
        url = "http://schoolscout.local/qgis/search/"
        request = { "district_name": district_name}
        return self.SSPostRequest(url, request)
      

    def getSchoolBoundariesByDistrict(self, district_id):
        url = "http://ss-dev.dftz.org/qgis/district/"+str(district_id)
        request = { "district_id": district_id}
        return self.SSPostRequest(url, request)
