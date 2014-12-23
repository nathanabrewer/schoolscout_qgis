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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
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


class SchoolScoutDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SchoolScoutDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.searchType.clear()
        self.searchType.addItem("Search for District", "district_name")
        self.searchType.addItem("Search for School", "school_name")
        self.searchType.addItem("Search for County", "district_name")
        self.searchPushButton.clicked.connect(self.doSearch)
        self.pushButton.clicked.connect(self.loadSelectedResults)
    def doSearch(self):
        print "doSearch()"
        print self.searchType.currentText()

        searchValue = self.searchText.text()

        print "searchDistrict('"+searchValue+"')"
        searchResults = self.searchDistrict(searchValue)
        self.results = searchResults['districts']

        #make way for new search results
        self.listWidget.clear()
        for index, district in enumerate(self.results, start=0):
            text = district["district_name"]
            self.listWidget.insertItem(index, text)

    def searchDistrict(self, district_name):
        url = "http://schoolscout.local/qgis/search/"

        header = {'content-type': 'application/json'}
        request = { "district_name": district_name}

        print "running post request to "+url
        jsondata = json.dumps(request)
        jsonresp = requests.post(url = url, data = jsondata, headers = header)

        if jsonresp.status_code == 200:
            pyresp = json.loads(jsonresp.text)
            return pyresp
        else:
            raise Exception("Web error " + str(jsonresp.status_code))

    def loadSelectedResults(self):
        print "OK, Load Selected Results...."
        if (len(self.listWidget.selectedItems()) > 1):
            print self.listWidget.selectedItems()
            for index, item in enumerate(self.listWidget.selectedItems(), start=0):
                print "looping index "+str(index)+" "+item.text()
                print self.results[index]
        else:
            QMessageBox.about(self, "Nothing Selected", "You need to select at least one thing from the list")