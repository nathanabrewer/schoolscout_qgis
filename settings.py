# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SchoolScoutDialog
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


from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings.ui'))


class SchoolScoutSettings(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(SchoolScoutSettings, self).__init__(parent)

        self.setupUi(self)
        settings = QSettings()
        
        apiendpoint = settings.value("schoolscout/apiendpoint")
        apiusername = settings.value("schoolscout/apiusername")
        apitoken = settings.value("schoolscout/apitoken")

        if(apiendpoint == None):
            apiendpoint = "http://ss-dev.dftz.org"
        if(apiusername == None):
            apiusername = "your_username@schoolscout.com"
        if(apitoken == None):
            apitoken = "No API Token Set"
        
        self.apiendpoint.setText(apiendpoint)
        self.apiusername.setText(apiusername)
        self.apitoken.setText(apitoken)

    
    