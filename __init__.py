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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SchoolScout class from file SchoolScout.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .schoolscout import SchoolScout
    return SchoolScout(iface)
