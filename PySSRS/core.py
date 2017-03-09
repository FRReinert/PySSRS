# -*- coding: utf-8 -*-

from suds.client import Client
from suds.transport.http import HttpAuthenticated
import logging as log
import sys


class SSRS:

    '''
    Create a SOAP connection to a SSRS (Microsoft Reporting Services)

    Example of usage on SSRS 2008:
        RS = SSRS(host='http://localhost/ReportinServices/ReportService2010.asmx?wsdl', user:'user@domain.com', key_password='myfreakingpassword')

    '''

    def __init__(self, host='http://localhost/reportserver/ReportService2010.asmx?wsdl', user='SEPTODONT\admin', key_password='admin', verbose=True):

        credentials = dict(username=user, password=key_password)
            
        c = HttpAuthenticated(**credentials)
        
        log.basicConfig(filename='SSRS.log', level=log.INFO)

        try:

            self.client = Client(host, transport=c)

        except BaseException as e:
            
            msg = "Could not connect to %s with user %s: %s" % (host, user, str(e))
            
            log.error(msg)
            
            if verbose:
                
                print(msg)
            
            
    def ListMethods(self):

        '''
        Return the list of methods available for your SSRS version

        '''

        try:

            list_of_methods = [method for method in self.client.wsdl.services[0].ports[0].methods]

            return list_of_methods

        except BaseException as e:

            msg = "ListMethod() Could not retrieve the methods: %s" % (str(e))
            
            log.error(msg)
            
            if verbose:
                
                print(msg)

    def ListDirItems(self, dir='/', recursive=False):

        '''
        Available information:
           ID 
           Name 
           Path
           TypeName
           CreationDate
           ModifiedDate
           CreatedBy
           ModifiedBy
           ItemMetadata

        Example of usage:
            RS = SSRS(host='http://localhost/reportserver/ReportService2010.asmx?wsdl', user='Administrator', key_password='TrUmPiSaCuNt')

            Objects = RS.ListDirItems()

            for key, value in Objects.items() :

                print('ID:', key)

                for key2, value2 in value.items():

                    print(key2,':', value2)

                print('\n')
                
        '''


        try:

            it = self.client.service.ListChildren(dir, recursive)

            it = it.CatalogItem

        except BaseException as e:

            msg = "ListDirItems() Could not retrieve the Objects: %s" % (str(e))
            
            log.error(msg)
            
            if verbose:
                
                print(msg)

        catalog_dict    = {}
        
        for item in it:

            catalog_dict[item['ID']] = {

                    'Name'          : item['Name'],

                    'Path'          : item['Path'],

                    'TypeName'      : item['TypeName'],

                    'CreationDate'  : item['CreationDate'],

                    'ModifiedDate'  : item['ModifiedDate'],

                    'CreatedBy'     : item['CreatedBy'],

                    'ModifiedBy'    : item['ModifiedBy'],

                    'ItemMetadata'  : item['ItemMetadata'],

                }

        return catalog_dict

        
    def Find(self, Folder='/', BooleanOperator='AND', SearchOptions={'Recusive': True}, SearchConditions=''):
        
        '''
        Find an item into SSRS
        
        '''
        
        items = self.client.service.FindItems(Folder, BooleanOperator, SearchOptions, SearchConditions)
        
        result = []
        
        for i in items:
            
            result.append(i)
        
        return result
        