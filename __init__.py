# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SchoolScout
                                 A QGIS plugin
 Schoolscout Plugin
                             -------------------
        begin                : 2014-12-23
        copyright            : (C) 2014 by Nathan Brewer
        email                : nathan.a.brewer@dftz.org
        git sha              : $Format:%H$
 ***************************************************************************/

"""

# 
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SchoolScout class from file SchoolScout.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .schoolscout import SchoolScout
    return SchoolScout(iface)
