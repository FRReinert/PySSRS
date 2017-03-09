#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SSRS

import connection as con

RS = PySSRS.SSRS(host=con._host, user=con._user, key_password=con._psw)

print(
    '''
    List of Objects in the root container (/)
    
    -> To check other directorys use the <dir> parameter
    -> To retrieve the directory and subdirectory's objects use <recursive=True> as a param
    
    Examples of usage:
        BaseDirObjects = RS.ListDirItems()
        BaseDirObjects = RS.ListDirItems(dir='/Customers')
        BaseDirObjects = RS.ListDirItems(recursive=True)
    '''
    )

BaseDirObjects = RS.ListDirItems()

for key, value in BaseDirObjects.items() :

    print('ID:', key)

    for key2, value2 in value.items():

        print(key2,':', value2)