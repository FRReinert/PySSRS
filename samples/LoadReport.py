#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
import os
from SSRS import SSRS

RS = SSRS(d._service, d._execution, d._user, d._psw)

'''
Part 1
    This Section will load the report and it's data
    you can get parameters data, page size, and every info from it
'''
try:
    Report = RS.RequestReport(path='/Faturamento/Notas por Transportadora')

except BaseException as e:
    print('Error loadint report: %s' % str(e))


'''
Part 2
    This section will use the pre-loaded data to render the report
'''
try:
    # Put the parameters into a dictionary
    Parameters = {
        'Transp': -1,
        'Frete' : 'C' 
    }
    
    RenderedReport = RS.RenderReport(LoadedReport=Report, format='PDF', parameters=Parameters)

except BaseException as e:
    print('Error rendering report: %s' % str(e))


# This block will return all the information that SSRS can handle
for k, v in RenderedReport.items():
    if k == 'Result':
        pass
    
    else:
        print(k,': ',v)

'''
This block will render the report into a file
But you can use it in Django/Flask Request, for example...
    
    <> IMPORTANT - If you want to render a file <>
    Compiled files like PDF, Word, Excel should use "wb" on the file opening
    Text based files (xml, html...) are "OK" to use the "w" mode 
'''
        
filename = os.path.join(os.path.dirname(__file__),'report'+ '.' + RenderedReport['Extension'])
fopen = open(filename, 'wb')
fopen.write(RenderedReport['Result'])
    
    
