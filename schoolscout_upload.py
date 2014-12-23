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

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'schoolscout_dialog_upload.ui'))


class SchoolScoutUpload(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SchoolScoutUpload, self).__init__(parent)

        self.setupUi(self)

        #self.searchType.clear()
        #self.searchType.addItem("Search for District", "district_name")
        #self.searchType.addItem("Search for School", "school_name")
        #self.searchType.addItem("Search for County", "district_name")
        #self.searchText.textChanged.connect(self.doSearch)

    def doSearch(self, value):
        print "Ah, do search does"
        print self.searchType.currentText()
        #print self.searchText.text()
        print value

