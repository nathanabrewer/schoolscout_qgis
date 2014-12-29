# -*- coding: utf-8 -*-
"""
/***************************************************************************

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
import ss_request

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'schoolscout_api_browser.ui'))


class SchoolScoutApiBrowser(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(SchoolScoutApiBrowser, self).__init__(parent)

        self.setupUi(self)

        self.boundaryLayer = None

        self.stateProvider = ss_request.StateList()
        self.countyProvider = ss_request.CountyList()
        self.districtProvider = ss_request.DistrictList()
        self.schoolProvider = ss_request.SchoolList()
        self.geometryProvider = ss_request.GeometryList()

        #define data handler for whenever we do an update like a fetch() or a fetchNext()
        self.stateProvider.setDataHandler(self.updateStateList)
        self.countyProvider.setDataHandler(self.updateCountyList)
        self.districtProvider.setDataHandler(self.updateDistrictList)
        self.schoolProvider.setDataHandler(self.updateSchoolList)
        self.geometryProvider.setDataHandler(self.updateGeometryList)

        self.stateNext.clicked.connect(self.stateProvider.fetchNext)
        self.statePrev.clicked.connect(self.stateProvider.fetchPrev)

        self.countyNext.clicked.connect(self.countyProvider.fetchNext)
        self.countyPrev.clicked.connect(self.countyProvider.fetchPrev)

        self.districtNext.clicked.connect(self.districtProvider.fetchNext)
        self.districtPrev.clicked.connect(self.districtProvider.fetchPrev)

        self.schoolNext.clicked.connect(self.schoolProvider.fetchNext)
        self.schoolPrev.clicked.connect(self.schoolProvider.fetchPrev)

        self.geometryNext.clicked.connect(self.geometryProvider.fetchNext)
        self.geometryPrev.clicked.connect(self.geometryProvider.fetchPrev)

        #only bring in a few states to make it snappy.
        #self.stateProvider.setSearchParameter('id', [4,5,6])
        self.stateProvider.fetch()


        #setup other click events
        self.stateListWidget.itemSelectionChanged.connect(self.stateSelected)
        self.countyListWidget.itemSelectionChanged.connect(self.countySelected)
        self.districtListWidget.itemSelectionChanged.connect(self.districtSelected)
        self.schoolListWidget.itemSelectionChanged.connect(self.schoolSelected)
        self.geometryListWidget.itemSelectionChanged.connect(self.geometrySelected)

    def stateSelected(self):
        item = self.stateListWidget.currentItem()
        print "stateSelected() - "+item.text()

        self.countyStatus.setText("Loading...")
        self.countyListWidget.clear()
        self.districtListWidget.clear()
        self.schoolListWidget.clear()

        state_id = item.data(1001)
        self.countyProvider.setSearchParameter('state_id', state_id)
        self.countyProvider.fetch()

    def countySelected(self):
        item = self.countyListWidget.currentItem()
        print "countySelected() - "+item.text()

        self.districtStatus.setText("Loading...")
        self.districtListWidget.clear()
        self.schoolListWidget.clear()

        county_id = item.data(1001)
        self.districtProvider.setSearchParameter('county_id', county_id)
        self.districtProvider.fetch()

    def districtSelected(self):

        self.schoolStatus.setText("Loading...")
        self.schoolListWidget.clear()

        items = self.districtListWidget.selectedItems()
        district_ids = []
        for item in items:
            district_id = item.data(1001)
            district_ids.append(district_id)

        #avoid error if this is empty... and just continue
        if(len(district_ids) < 1):
            return
        self.schoolProvider.setSearchParameter('district_id', district_ids)
        self.schoolProvider.fetch()

    def schoolSelected(self):
        items = self.schoolListWidget.selectedItems()
        school_ids = []
        for item in items:
            school_id = item.data(1001)
            school_ids.append( school_id )

        #avoid error if this is empty... and just continue
        if(len(school_ids) < 1):
            return

        self.geometryProvider.setSearchParameter('school_id', school_ids)
        self.geometryProvider.fetch()
        
    def geometrySelected(self):
        items = self.geometryListWidget.selectedItems()
        self.loadGeometryPreview(items)
        

    def updateStateList(self, data):
        self.stateListWidget.clear()
        for record in data:
            item = QListWidgetItem(self.stateListWidget)
            item.setText(record["name"])
            item.setData(1001, record["id"])   

        provider = self.stateProvider
        text = "Page "+provider.currentPage()+" / "+provider.totalPages()
        self.statePageStatus.setText(text)

        text = "Showing"+ provider.totalRecords()+" of " +provider.getTotal()
        self.stateStatus.setText(text)

    def updateCountyList(self, data):
        self.countyListWidget.clear()
        for record in data:
            item = QListWidgetItem(self.countyListWidget)
            item.setText(record["name"])
            item.setData(1001, record["id"]) 
            
        provider = self.countyProvider
        text = "Page "+provider.currentPage()+" / "+provider.totalPages()
        self.countyPageStatus.setText(text)

        text = "Showing"+ provider.totalRecords()+" of " +provider.getTotal()
        self.countyStatus.setText(text)              

    def updateDistrictList(self, data):
        self.districtListWidget.clear()
        for record in data:
            item = QListWidgetItem(self.districtListWidget)
            item.setText(record["name"])
            item.setData(1001, record["id"])  
            
        provider = self.districtProvider
        text = "Page "+provider.currentPage()+" / "+provider.totalPages()
        self.districtPageStatus.setText(text)

        text = "Showing"+ provider.totalRecords()+" of " +provider.getTotal()
        self.districtStatus.setText(text)             

    def updateSchoolList(self, data):
        self.schoolListWidget.clear()
        for record in data:
            item = QListWidgetItem(self.schoolListWidget)
            item.setText(record["name"])
            item.setData(1001, record["id"])   
            
        provider = self.schoolProvider
        text = "Page "+provider.currentPage()+" / "+provider.totalPages()
        self.schoolPageStatus.setText(text)

        text = "Showing"+ provider.totalRecords()+" of " +provider.getTotal()
        self.schoolStatus.setText(text)                                             

    def updateGeometryList(self, data):
        self.geometryListWidget.clear()
        for record in data:
            item = QListWidgetItem(self.geometryListWidget)
            name = record["name"]
            if(record["active"] == 1):
                name = "[PRODUCTION] - "+name

            item.setText(name)
            item.setData(1001, record["id"])   
            item.setData(1002, record["active"]) 
            item.setData(1003, record["school_id"]) 
            item.setData(1004, record["district_id"]) 
            item.setData(1005, record["wkt"]) 
        
        provider = self.geometryProvider

        text = "Page "+provider.currentPage()+" / "+provider.totalPages()
        self.geometryPageStatus.setText(text)

        text = "Showing"+ provider.totalRecords()+" of " +provider.getTotal()
        self.geometryStatus.setText(text) 

        
        #stateList.fetch()
        #stateList.fetchNext()
        #stateList.summary()
        #stateList.listSummary()

    def loadGeometryPreview(self, geometryItems): 
        
        map = QgsMapLayerRegistry.instance()
        
        if(self.boundaryLayer != None):
            map.removeMapLayers( [self.boundaryLayer.id()] )
            self.boundaryLayer = None
        
        if(len(geometryItems) == 0):
            return

        self.boundaryLayer = QgsVectorLayer("Polygon?crs=EPSG:4326", "Temporary Layer", 'memory')

        dataProvider = self.boundaryLayer.dataProvider()
        dataProvider.addAttributes([ QgsField("geometry_id", QVariant.Int), QgsField("description", QVariant.String), QgsField("active", QVariant.Int), QgsField("school_id", QVariant.Int), QgsField("district_id", QVariant.Int)])

        #start Editing
        self.boundaryLayer.startEditing()

        for geometryItem in geometryItems:
            geometry_id = geometryItem.data(1001)
            description = geometryItem.text()
            geometry_active = geometryItem.data(1002)
            geometry_school_id = geometryItem.data(1003)
            geometry_district_id = geometryItem.data(1004)
            wkt = geometryItem.data(1005)

            tempFeature = QgsFeature()    
            tempFeature.setGeometry(QgsGeometry.fromWkt(wkt))        
            tempFeature.setAttributes([geometry_id, description, geometry_active, geometry_school_id, geometry_district_id])

            self.boundaryLayer.addFeature(tempFeature)

             
        #stop Editing, commit changes to layer
        self.boundaryLayer.commitChanges()
        self.boundaryLayer.setLayerTransparency(50)

        
        map.addMapLayer(self.boundaryLayer)

        iface.mapCanvas().setExtent(self.boundaryLayer.extent())    
