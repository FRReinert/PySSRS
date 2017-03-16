#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
from SSRS import SSRS

RS      = SSRS(d._service, d._execution, d._user, d._psw)
Methods = RS.ListMethods()

if Methods:
    print(
        '''
        List of RPC Methods available on this SSRS version 
        Please see the MS docs to find out their usability
        '''
    )
    
    for i in Methods:
        print('>> ', i)
