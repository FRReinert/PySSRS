# -*- coding: utf-8 -*-

from suds.client import Client
from suds.sax.text import Text
from suds.sax.element import Element
from suds.transport.http import HttpAuthenticated
from  . import schemas
import base64
import logging as log
import codecs
import uuid
import sys
import os
from _ast import Load

class SSRS():
    '''
    Create a SOAP connection to a SSRS (Microsoft Reporting Services)

    Example of usage on SSRS 2008:
        RS = SSRS(ReportService   = 'http://localhost/ReportinServices/ReportService2010.asmx?wsdl', 
                  ReportExecution = 'http://myserver/reportserver/ReportExecution2005.asmx?wsdl',
                  user            = 'user@domain.com', 
                  key_password    = 'myfreakingpassword'
                )

    '''

    def __init__(self, ReportService, ReportExecution, user, key_password, verbose=True):
        
        self.verbose = verbose
        
        service_cred    = dict(username=user, password=key_password)          
        service_cred    = HttpAuthenticated(**service_cred)
        
        exec_cred       = dict(username=user, password=key_password)
        exec_cred       = HttpAuthenticated(**exec_cred)
        
        log.basicConfig(filename='SSRS.log', level=log.INFO)
        
        try:
            self.ServiceClient      = Client(ReportService, transport=service_cred)
            self.ExecutionClient    = Client(ReportExecution, transport=exec_cred)
        
        except BaseException as e:        
           
            msg = "Error during connection: %s" % e.fault.faultstring
            log.error(msg)          
        
            if self.verbose:            
                print(msg)
                
            exit() 
                
            
    def ListMethods(self):
        '''
        Return the list of methods available for your SSRS version
        '''
        try:
            list_of_methods = [method for method in self.ServiceClient.wsdl.services[0].ports[0].methods]
            return list_of_methods

        except BaseException as e:

            msg = "ListMethod() Could not retrieve the methods: %s" % e.fault.faultstring      
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
            it = self.ServiceClient.service.ListChildren(dir, recursive)
            it = it.CatalogItem

        except BaseException as e:
            msg = "ListDirItems() Could not retrieve the Objects: %s" % e.fault.faultstring
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

        except BaseException as e:
            msg = "Find() Could not retrieve the Objects: %s" % e.fault.faultstring
            log.error(msg)
            
            if self.verbose:     
                print(msg)  
                
            return
        
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
            it = self.ServiceClient.service.GetItemParameters(path, None, True, None, None)

        except BaseException as e:
            msg = "GetParameters() Could not retrieve the parameters: %s" % e.fault.faultstring
            log.error(msg)
            if self.verbose:
                print(msg)
                return
              
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
    
    
    def RequestReport(self, path):
        try:
            execInfo = self.ExecutionClient.service.LoadReport(path, None)
            return execInfo
        except BaseException as e:
            msg = "Could not Load the Report: %s" % e.fault.faultstring
            log.error(msg)
            
            if self.verbose:     
                print(msg)
            
            return
    
    def RenderReport(self, LoadedReport, format, **parameters):
        '''
        Render an already executed Report
        '''
        
        # check if format is valid
        available_formats = ['XML','NULL','CSV','IMAGE','PDF','HTML4.0','HTML3.2','MHTML','EXCEL','Word']
        if format not in available_formats:
            msg = "Format is not valid: %s" % format
            log.error(msg)
            
            if self.verbose:     
                print(msg)
            
            return
        
        # Set parameters
        params = ''
        for k, v in parameters['parameters'].items():
            params =  params +'''
            <rep:ParameterValue>
               <rep:Name>%s</rep:Name>
               <rep:Value>%s</rep:Value>
            </rep:ParameterValue>
            ''' % (k, v)
        
        param_xml = schemas.xml_Execute_Report_Parameter  
        param_xml = param_xml.format(LoadedReport.ExecutionID, params)
        
        try:
            setparam = self.ExecutionClient.service.SetExecutionParameters(__inject={'msg': param_xml})
        except BaseException as e:
            msg = "Could not Send Parameters: %s" % e.fault.faultstring
            log.error(msg)
            
            if self.verbose:     
                print(msg) 
            
            return
        
        # Default XML Schema | SUDS Factory doesent worked very well in this case
        xml = schemas.xml_Render_Report.format(LoadedReport.ExecutionID, format)
        
        # Render the report by its ExecutionID
        try:
            result = self.ExecutionClient.service.Render(__inject={'msg': xml})
        
        except BaseException as e:
            msg = "Could not Render the Report: %s" % e.fault.faultstring
            log.error(msg)
            
            if self.verbose:     
                print(msg) 
            
            return
        
        # Data to be sended
        Data= {}
        for k, v in result:
            if k == 'Result':
                 Data['Result'] = base64.b64decode(result.Result)
            
            else:
                Data[k] = v
        
        return Data
        
        
        