# -*- coding: utf-8 -*-

from suds.client import Client
from suds.sax.text import Text
from suds.transport.http import HttpAuthenticated
import logging as log
import sys

class SSRS():
    '''
    Create a SOAP connection to a SSRS (Microsoft Reporting Services)

    Example of usage on SSRS 2008:
        RS = SSRS(host='http://localhost/ReportinServices/ReportService2010.asmx?wsdl', user:'user@domain.com', key_password='myfreakingpassword')

    '''

    def __init__(self, host='http://localhost/reportserver/ReportService2010.asmx?wsdl', user='SEPTODONT\admin', key_password='admin', verbose=True):
        
        self.verbose = verbose 
        credentials  = dict(username=user, password=key_password)          
        credentials  = HttpAuthenticated(**credentials)
        log.basicConfig(filename='SSRS.log', level=log.INFO)
        
        try:
            self.client = Client(host, transport=credentials)
        
        except BaseException as e:        
           
            msg = "Could not connect to %s with user %s: %s" % (host, user, str(e))
            log.error(msg)          
        
            if self.verbose:            
                print(msg)
                
            exit() 
                
            
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
            
            if self.verbose:                
                print(msg)
                
            return False

    
    def ListDirItems(self, dir=r'/', recursive=False):
        '''
        List all itens in a folder. 
        if specified the <recursive> parameter, subfolders will be scanned too
        '''

        try:
            it = self.client.service.ListChildren(dir, recursive)
            it = it.CatalogItem

        except BaseException as e:
            msg = "ListDirItems() Could not retrieve the Objects: %s" % (str(e))    
            log.error(msg)
            
            if self.verbose:     
                print(msg)
                
            return False

        catalog_dict = {}
        
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
        
    
    def Find(self, text, objtype=None):       
        '''
        Find objects on SSRS 
        '''
        
        try: 
            it = self.ListDirItems(recursive=True)
            if isinstance(it, Text):
                return dict(it)
                
        
        except BaseException as e:
            msg = "Find() Could not retrieve the Objects: %s" % (str(e))    
            log.error(msg)
            
            if self.verbose:     
                print(msg)  
                
            return False
        
        catalog_dict = {}
        for key, value in it.items() :
            for word in value.values():
                if text in str(word):
                    if objtype == None:
                        catalog_dict[key] = value
                        
                    else:
                        if it[key]['TypeName'] == objtype:
                            catalog_dict[key] = value
        
        return catalog_dict
    
    
    def GetParameters(self, path):
        '''
        Retrieve parameters from an SSRS Report
        '''
        
        try:
            it = self.client.service.GetItemParameters(path, None, True, None, None)
            if isinstance(it, Text):
                return dict(it)
            
        except BaseException as e:
            msg = "GetParameters() Could not retrieve the parameters: %s" % str(e)    
            log.error(msg)
            
            if self.verbose:     
                print(msg)  
                
            return False        
       
        param_dict = {}
        for item in it.ItemParameter:
            param_dict[item['Name']] = {
                 'ParameterTypeName'        : item['ParameterTypeName'],
                 'Nullable'                 : item['Nullable'],
                 'AllowBlank'               : item['AllowBlank'],
                 'MultiValue'               : item['MultiValue'],
                 'QueryParameter'           : item['QueryParameter'],
                 'Prompt'                   : item['Prompt'],
                 'PromptUser'               : item['PromptUser'],
                 'ValidValuesQueryBased'    : item['ValidValuesQueryBased'],
                 'DefaultValuesQueryBased'  : item['DefaultValuesQueryBased'],
            }
        
        return param_dict

        
        
        
        