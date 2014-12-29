# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SchoolScout




    .setSearchParameter()
    .fetch()
    .fetchNext()
    .fetchPrevious()
    .currentPage()
    .totalRecords()


 ***************************************************************************/

"""

import json, requests, logging
from PyQt4.QtCore import QSettings
from requests.auth import HTTPBasicAuth

class SSRequest():
    
    username = ""
    token = ""
    apiEndpoint = ""

    def __init__(self, parent=None):
        """Constructor."""
        settings = QSettings()
        
        self.apiEndpoint = settings.value("schoolscout/apiendpoint")
        self.username = settings.value("schoolscout/apiusername")
        self.token = settings.value("schoolscout/apitoken")
        #logging.basicConfig(level=logging.DEBUG)

    def SSRequestHeader(self):
        return {'content-type': 'application/json', 'auth': self.token }

    def SSPostRequest(self, target, payload):
        url = self.apiEndpoint+target
        jsondata = json.dumps(payload)
        jsonresp = requests.post(url = url, data = jsondata, headers = self.SSRequestHeader())
        if jsonresp.status_code == 200:
            print "Response 200 - "+url
            pyresp = json.loads(jsonresp.text)
            return pyresp
        else:
            print jsonresp.status_code
            print jsonresp
            raise Exception("SSPostRequest Web Request Error")

    def SSGetRequest(self, target, payload):
        url = self.apiEndpoint+target
        jsondata = json.dumps(payload)
        jsonresp = requests.get(url = url, data = jsondata, headers = self.SSRequestHeader())
        if jsonresp.status_code == 200:
            print "Response 200 - "+url
            pyresp = json.loads(jsonresp.text)
            return pyresp
        else:
            print jsonresp.status_code
            print jsonresp            
            raise Exception("SSGetRequest Web Request Error ")           





class SSRequestList(SSRequest):
    def __init__(self):
        SSRequest.__init__(self)
        self.current_page = 1
        self.requestParameters={}
        self.data = {}

    def setSearchParameter(self, field, value):
        self.requestParameters[field] = value
    
    def setDataHandler(self, func):
        self.dataHandler = func

    def fetch(self):
        if(self.api_object == None):
            raise Exception("API Object not specified when attempting fetch() with SSRequestList type Object")

        lastRequest = self.SSGetRequest(self.api_object, self.requestParameters)
        
        self.data = lastRequest['data']

        self.count = lastRequest['meta']['pagination']['count']
        self.total = lastRequest['meta']['pagination']['total']
        self.current_page = lastRequest['meta']['pagination']['current_page']
        self.total_pages = lastRequest['meta']['pagination']['total_pages']

        try :
            self.next = lastRequest['meta']['pagination']['links']['next']
        except:
            self.next = None

        try :
            self.previous = lastRequest['meta']['pagination']['links']['previous']
        except: 
            self.previous = None

        if(hasattr(self.dataHandler, '__call__')):
            self.dataHandler(self.data)
    
    def fetchNext(self):
        if(self.current_page < self.total_pages):
            self.current_page+=1
            self.requestParameters['page'] = self.current_page
            self.fetch()

    def fetchPrev(self):
        if(self.current_page > 1):
            self.current_page-=1
            self.requestParameters['page'] = self.current_page
            self.fetch()   

    def currentPage(self):
        return str(self.current_page)
    def totalPages(self):
        return str(self.total_pages)
    def totalRecords(self):
        return str(len(self.data))
    def getCount(self):
        return str(self.count)        
    def getTotal(self):
        return str(self.total)             

    def summary(self):
        print self.api_object+" -=-=-=-=-=-=-=-=-=-=-=-="

        print "summary()"
        print "Total of "+self.getTotal()+" Records"
        print "Currently on Page "+self.currentPage()+" of "+self.totalPages()
        print "This Page Contains "+self.getCount()+" Records"

        print "-=-=-=-=-=-=-=-=-=-=-=-="

    def listSummary(self):
        print self.api_object+" -=-=-=-=-=-=-=-=-=-=-=-="

        print "listSummary() [COUNT: "+self.getTotal()+" ]"
        for county in self.data:
            print county['name']+" (County ID "+str(county['id'])+" )"

        print "-=-=-=-=-=-=-=-=-=-=-=-="




class CountyList(SSRequestList):
    def __init__(self):
        SSRequestList.__init__(self)
        self.api_object = "counties"

class StateList(SSRequestList):
    def __init__(self):
        SSRequestList.__init__(self)
        self.api_object = "states"

class DistrictList(SSRequestList):
    def __init__(self):
        SSRequestList.__init__(self)
        self.api_object = "districts"

class SchoolList(SSRequestList):
    def __init__(self):
        SSRequestList.__init__(self)
        self.api_object = "schools"

class GeometryList(SSRequestList):
    def __init__(self):
        SSRequestList.__init__(self)
        self.api_object = "geometries"                


