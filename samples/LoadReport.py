#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
import os
from SSRS import SSRS

RS = SSRS(d._service, d._execution, d._user, d._psw)

Parameters = {
    'Transp': -1,
    'Frete' : 'C' 
    }

Report = RS.RequestReport(path='/Faturamento/Notas por Transportadora', format='PDF', parameters=Parameters)

if Report:
   
    for k, v in Report.items():
        if k == 'Result':
            pass
        
        else:
            print(k,': ',v)
    
    filename = os.path.join(os.path.dirname(__file__),'report'+ '.' + Report['Extension'])
    fopen = open(filename, 'wb')
    fopen.write(Report['Result'])
    
    
