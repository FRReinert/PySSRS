#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
from SSRS import SSRS

RS      = SSRS(d._service, d._execution, d._user, d._psw)
BaseDirObjects = RS.ListDirItems()

if BaseDirObjects:
    print(
        '''           
        List of Objects in the root container (/)
        
        -> To check other directorys use the <dir> parameter
        -> To retrieve the directory and subdirectory's objects use <recursive=True> as a param
        
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

        Examples of usage:
            BaseDirObjects = RS.ListDirItems()
            BaseDirObjects = RS.ListDirItems(dir='/Customers')
            BaseDirObjects = RS.ListDirItems(recursive=True)
        '''
    )
    for key, value in BaseDirObjects.items() :
        print('ID:', key)
    
        for key2, value2 in value.items():
            print(key2,':', value2)