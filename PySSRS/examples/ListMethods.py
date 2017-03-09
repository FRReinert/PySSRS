#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import ListDir

import connection as con

RS = SSRS(host=con._host, user=con._user, key_password=con._psw)

# Listing Methods

print(
    '''
    List of RPC Methods available on this SSRS version 
    Please see the MS docs to find out their usability
    '''
    )

Methods = RS.ListMethods()

for i in Methods:
    
    print('>> ', i)
