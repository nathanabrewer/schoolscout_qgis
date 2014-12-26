# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SchoolScout
                                 A QGIS plugin
 Schoolscout Plugin
                              -------------------
        begin                : 2014-12-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Nathan Brewer
        email                : nathan.a.brewer@dftz.org
 ***************************************************************************/

"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
# Initialize Qt resources from file resources.py
import resources_rc, qgis

# Import the code for the dialog
from schoolscout_dialog import SchoolScoutDialog
from schoolscout_upload import SchoolScoutUpload
from settings import SchoolScoutSettings
from boundary_tool import SchoolScoutBoundaryTool
import os.path


class SchoolScout:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SchoolScout_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SchoolScoutDialog()
        self.uploadDlg = SchoolScoutUpload()
        self.settingsDlg = SchoolScoutSettings()

        self.boundaryTool = SchoolScoutBoundaryTool(iface.mapCanvas())

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Schoolscout')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SchoolScout')
        self.toolbar.setObjectName(u'SchoolScout')

    # translation stuff we dont need really
    def tr(self, message):
        return QCoreApplication.translate('SchoolScout', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        
        self.add_action(
            ':/plugins/SchoolScout/images/Magnifier.png',
            text=self.tr(u'School/District/County Search'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/SchoolScout/images/CheckMark.png',
            text=self.tr(u'Checkin Selected Features'),
            callback=self.runUpload,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/SchoolScout/images/Tools.png',
            text=self.tr(u'Settings'),
            callback=self.openSettings,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/SchoolScout/images/Web.png',
            text=self.tr(u'Activate Boundary Map Tool'),
            callback=self.activateBoundaryMapTool,
            parent=self.iface.mainWindow())


    def activateBoundaryMapTool(self):
        self.iface.mapCanvas().setMapTool(self.boundaryTool)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Schoolscout'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):

        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def runUpload(self):

        activecount = self.uploadDlg.lookupActive()
        #if we dont have any selected features on the current layer, we don't need to display the form.
        if ( activecount < 1):
            QMessageBox.about(None,"Nothing Selected", "Active layer needs at least one Feature Selected to use this tool")
        else:
            self.uploadDlg.show()
            result = self.uploadDlg.exec_()
            # See if OK was pressed
            if result:
                # Do something useful here - delete the line containing pass and
                # substitute with your code.
                pass

    def openSettings(self):
        
        self.settingsDlg.show()
        result = self.settingsDlg.exec_()

        if result:
            print "Save settings"            
            QSettings().setValue('schoolscout/apiendpoint', self.settingsDlg.apiendpoint.text())
            QSettings().setValue('schoolscout/apiusername', self.settingsDlg.apiusername.text())
            QSettings().setValue('schoolscout/apitoken', self.settingsDlg.apitoken.text())
            
        else:
            print "Do not save settings"