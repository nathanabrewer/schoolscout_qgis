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

import fileinput
import sys, os, json, requests
import qgis;

from PyQt4.QtCore import *
from qgis.core import *
from qgis.utils import *
from requests.auth import HTTPBasicAuth


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
        self.uploadNow.clicked.connect(self.doUpload)
      
        print "OK, here we go...."
     

    def doUpload(self):
        print "Ah, do the upload!"
       
    def lookupActive(self): 
        layer = iface.activeLayer()
        features = layer.selectedFeatures()   
        
        self.selectedFeaturesListWidget.clear()

        for index, feature in enumerate(features, start=0):
            geom = feature.geometry()
            print "Feature ID %d: " % feature.id()

            # show some information about the feature
            if geom.type() == QGis.Point:
              x = geom.asPoint()
              print "Point: " + str(x)
            elif geom.type() == QGis.Line:
              x = geom.asPolyline()
              print "Line: %d points" % len(x)
            elif geom.type() == QGis.Polygon:
              x = geom.asPolygon()
              numPts = 0
              for ring in x:
                numPts += len(ring)
              print "Polygon: %d rings with %d points" % (len(x), numPts)
            else:
              print "Unknown"

            # fetch attributes
            attrs = feature.attributes()
            print attrs   

            text = attrs[1]+"\t\t"+str(attrs[0])
            self.selectedFeaturesListWidget.insertItem(index, text)
