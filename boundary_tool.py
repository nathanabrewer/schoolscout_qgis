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
from qgis.gui import QgsMapTool


from PyQt4 import QtGui, uic

class SchoolScoutBoundaryTool(QgsMapTool):   
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas    
        self.iface = iface

    def canvasPressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.selectNow(point)
        #print "canvasPressEvent() inside SchoolScoutBoundaryTool"
        #print point
        #print x
        #print y

    def selectNow(self, point):
        layer = self.iface.activeLayer()
        if not layer or layer.type() != QgsMapLayer.VectorLayer:
             QMessageBox.warning(None, "No!", "Sorry, you need to have a vector layer selected")
             return

        width = self.iface.mapCanvas().mapUnitsPerPixel() * 2
        rect = QgsRectangle(point.x() - width,
                              point.y() - width,
                              point.x() + width,
                              point.y() + width)
        rect = self.iface.mapCanvas().mapRenderer().mapToLayerCoordinates(layer, rect)
        layer.removeSelection()
        layer.select(rect, True)

        features = layer.selectedFeatures()
        for feature in features:
            attr = feature.attributes()
            QMessageBox.warning(None, "Selected Boundary", "You selected the boundary "+str(attr[0])+ ". A single point selection map tool with custom edit/options form not connected yet. Just a proof/Concept")
        

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def canvasReleaseEvent(self, event):
        #Get the click
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True