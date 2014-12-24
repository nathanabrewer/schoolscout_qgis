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
from requests.auth import HTTPBasicAuth
from schoolscout_webconnect import SchoolScoutWebConnect

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'schoolscout_dialog_base.ui'))


class SchoolScoutDialog(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(SchoolScoutDialog, self).__init__(parent)

        self.setupUi(self)

        self.searchType.clear()
        self.searchType.addItem("Search for District", "district_name")
        self.searchType.addItem("Search for School", "school_name")
        self.searchType.addItem("Search for County", "district_name")
        self.searchPushButton.clicked.connect(self.doSearch)
        self.pushButton.clicked.connect(self.loadSelectedResults)
    
    def doSearch(self):
        searchValue = self.searchText.text()

        
        searchResults = SchoolScoutWebConnect().searchDistrict(searchValue)
        self.results = searchResults['districts']

        #make way for new search results
        self.listWidget.clear()
        for index, district in enumerate(self.results, start=0):
            text = district["district_name"]
            self.listWidget.insertItem(index, text)



    def loadSelectedResults(self):
        print "OK, Load Selected Results...."
        if (len(self.listWidget.selectedItems()) > 0):
            print self.listWidget.selectedItems()
            for index, item in enumerate(self.listWidget.selectedItems(), start=0):
                print "looping index "+str(index)+" "+item.text()
                print self.results[index]
                self.loadDistricts(self.results[index]["id"])
        else:
            QMessageBox.about(self, "Nothing Selected", "You need to select at least one thing from the list")





 
         
    def loadDistricts(self, district_id):
        
        print "Ok, attempint web service request to get data"
        

        jsonresponse = SchoolScoutWebConnect().getSchoolBoundariesByDistrict(district_id)
 
        print "Loading "+ jsonresponse['district_name']

        boundaryLayer = QgsVectorLayer("Polygon?crs=EPSG:4326", jsonresponse['district_name']+"__Boundary", 'memory')
        pointLayer = QgsVectorLayer("Point?crs=EPSG:4326", jsonresponse['district_name']+"__Point", 'memory')

        boundaryDataProvider = boundaryLayer.dataProvider()
        boundaryDataProvider.addAttributes([ QgsField("id", QVariant.Int), QgsField("school_name", QVariant.String), QgsField("cdscode",QVariant.String),QgsField("NCESSCH",QVariant.String)])

        pointDataProvider = pointLayer.dataProvider()
        pointDataProvider.addAttributes([ QgsField("id", QVariant.Int), QgsField("school_name", QVariant.String), QgsField("cdscode",QVariant.String),QgsField("NCESSCH",QVariant.String)])

        boundaryLayer.startEditing()
        pointLayer.startEditing()


        # Loop through school responses, create a point in the point layer, and a polygon in the boundary layer
        count=0

        for school in jsonresponse['schools']:
            count+=1
            
            if school['point'] != None:  
                outFeat = QgsFeature()    
                outFeat.setGeometry(QgsGeometry.fromWkt(school['point']))

                outFeat.setAttributes([int(school['fields']["id"]), school['fields']["school_name"], school['fields']["cdscode"], school['fields']["NCESSCH"]])
                
                pointLayer.addFeature(outFeat)
            
            if school['boundary'] != None:  
                outFeat = QgsFeature()    
                outFeat.setGeometry(QgsGeometry.fromWkt(school['boundary']))
                
                outFeat.setAttributes([int(school['fields']["id"]), school['fields']["school_name"], school['fields']["cdscode"], school['fields']["NCESSCH"]])
                
                boundaryLayer.addFeature(outFeat)
            else:
                print school['fields']['school_name']+" had None type for boundary, skipping"
             

        boundaryLayer.commitChanges()
        pointLayer.commitChanges()


        print pointLayer

        map = QgsMapLayerRegistry.instance()
        boundaryLayer.setLayerTransparency(50)

        #trying to find a way to do the symbol level alpha/transparency
        #properties = {'size':'5.0','color':'255,0,0,100'}
        #symbol_layer = QgsSimpleMarkerSymbolLayerV2.create(properties)
        #print boundaryLayer.renderer
        #print boundaryLayer.rendererV2.symbols()
        #boundaryLayer.rendererV2.symbols()[0].changeSymbolLayer(0,symbol_layer)


        map.addMapLayer(boundaryLayer)
        map.addMapLayer(pointLayer)

        iface.mapCanvas().setExtent(boundaryLayer.extent())            