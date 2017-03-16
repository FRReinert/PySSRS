#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
from SSRS import SSRS

RS     = SSRS(d._service, d._execution, d._user, d._psw)
result = RS.Find(text='Lote', objtype='Report')

if result:
    print(
        '''
        This method will search for any property value that matches with the parameter <text>
        It'll match if any property value of the object CONTAINS the <text> value
        
        You can also specify the type of the object by using the <objtype> parameter as a string
        
        Types accepted:
            -> Component 
            -> DataSource 
            -> Folder
            -> Model
            -> LinkedReport
            -> Report
            -> Resource
            -> DataSet
            -> Site
            -> Unknown
            
        if you leave the <text> parameter blank it'll retrieve all objects (respecting the <objtype> parameter)
        '''
    )
    
    for key, value in result.items() :
        print('ID:', key)
        
        for key2, value2 in value.items():
            print(key2,':', value2)
        
        print('\n')